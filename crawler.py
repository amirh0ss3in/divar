import json
import logging
import argparse
import concurrent.futures as parallel

from pathlib import Path
from datetime import datetime
from time import sleep, perf_counter
from functools import lru_cache

import requests
from requests.exceptions import BaseHTTPError, RequestException


POST_LOGGER = f'{__name__}.post'
WAIT_TIME_BETWEEN_RETRIES = 2.0  # API limits to 30 pages call per minutes


class Retry(requests.urllib3.Retry):
    def get_backoff_time(self):
        return WAIT_TIME_BETWEEN_RETRIES


@lru_cache(maxsize=1)
def getLogger():
    return logging.getLogger(__name__)


def build_api_url(*route, unparse=requests.utils.urlunparse):
    route = Path('/v8').joinpath(*route)
    return unparse(('https', 'api.divar.ir', route.as_posix(), '', '', ''))


def download_post(session, token, folder):
    logger = logging.getLogger(POST_LOGGER)
    destination = folder.joinpath(f'{token}.json')
    if destination.exists():
        logger.info("Skipping token %s: file already exists", token)
        return

    try:
        response = session.get(build_api_url('posts', token))
        response.raise_for_status()
        post = response.json()
    except RequestException as e:
        getLogger().error("Failed to fetch data for token %s: %s", token, e)
    except json.JSONDecodeError as e:
        getLogger().error("Failed to decode JSON for token %s: %s", token, e)
    else:
        with destination.open('w', encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=4)
            logger.info("Saved: %s", token)


def retrieve_page(session, url, payload):
    try:
        response = session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except (RequestException, BaseHTTPError) as e:
        getLogger().error("An error occurred: %s", e)


def extract_tokens(posts):
    for post in posts:
        try:
            token = post['data']['action']['payload']['token']
        except (TypeError, KeyError):
            pass
        else:
            yield token


def scrape(city_code, category, last_post_date, result_directory, max_pages, max_retries):
    search_url = build_api_url('search', str(city_code), category)
    last_post_date = int(last_post_date.timestamp() * 1_000_000)

    session = requests.Session()
    retries = Retry(total=max_retries, allowed_methods=['GET', 'POST'])
    adapter = requests.adapters.HTTPAdapter(max_retries=retries, pool_block=True)
    session.mount('https://api.divar.ir/', adapter)

    sleep_time = 0
    for page_count in range(1, max_pages + 1):
        sleep(sleep_time)
        json_payload = {
            'json_schema': {
                'category': {'value': category}
            },
            'last-post-date': last_post_date,
            'page': page_count
        }

        start_time = perf_counter()
        data = retrieve_page(session, search_url, json_payload)
        try:
            post_list = data['web_widgets']['post_list']
        except (TypeError, KeyError):
            break

        with parallel.ThreadPoolExecutor() as executor:
            futures = [
                    executor.submit(download_post, session, token, result_directory)
                    for token in extract_tokens(post_list)
            ]

            for future in parallel.as_completed(futures):
                # TODO I can add any post-level processing here if needed
                pass

        last_post_date = data['last_post_date']
        getLogger().info("Page %d scraped. Last post date is %d.", page_count, last_post_date)

        # Adjust sleep time dynamically based on response time
        elapsed_time = perf_counter() - start_time
        sleep_time = max(0.2, WAIT_TIME_BETWEEN_RETRIES - elapsed_time)


def command_line_parser():
    def date_parser(user_input):
        return datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--category', '--cat', '-c',
                        default='apartment-rent',
                        help='category of posts to search for')
    parser.add_argument('--city-code', '--city', '--code', '-z',
                        type=int, default=1,
                        help='...')
    parser.add_argument('--result-directory', '--directory', '-d',
                        type=Path, default=Path('Results'),
                        help='Directory in which to store scraping results')
    parser.add_argument('--last-post-date', '--date', '--time', '-t',
                        type=date_parser, default=datetime.now(),
                        help='...')
    parser.add_argument('--max-pages', '--pages', '-p',
                        type=int, default=4,
                        help='Amount of pages to scrape for')
    parser.add_argument('--max-retries', '--retries', '-r',
                        type=int, default=5,
                        help='Amount of time a request will be retried when a download fails')
    return parser


def main(argv=None):
    args = command_line_parser().parse_args(argv)

    folder = args.result_directory.joinpath(f'{args.category}/{args.city_code}/')
    folder.mkdir(parents=True, exist_ok=True)

    # Configure logging
    logging.basicConfig(
            filename=folder.joinpath('scrape_log.log').as_posix(),
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger(POST_LOGGER).addHandler(logging.StreamHandler())

    args = vars(args)
    args['result_directory'] = folder
    try:
        scrape(**args)
    except KeyboardInterrupt:
        getLogger().info("Scraping interrupted by user.")
    except Exception as e:
        getLogger().error("An unexpected error occurred: %s", e)
        raise


if __name__ == '__main__':
    main()