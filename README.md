# Divar Scraper with Multithreading

This project allows you to scrape data from the Divar website, specifically for real estate listings in different categories and cities. It utilizes the Divar API to retrieve and store information about real estate listings in an Excel file. This module provides a command-line tool for scraping posts from a website. Below are the available options and how to use them:

1. **Category (Optional)**
   - Option: `--category`, `--cat`, `-c`
   - Default: `apartment-rent`
   - Description: Specify the category of posts to search for.

2. **City Code (Optional)**
   - Option: `--city-code`, `--city`, `--code`, `-z`
   - Default: `1`
   - Description: Specify the city code or identifier for the location you want to search in. Use the following city codes:

     | Code | City        |
     | ---- | ----------- |
     | 1    | تهران      |
     | 2    | کرج        |
     | 3    | مشهد       |
     | 4    | اصفهان     |
     | ...  | ...         |

3. **Result Directory (Optional)**
   - Option: `--result-directory`, `--directory`, `-d`
   - Default: `Results`
   - Description: Specify the directory where scraping results will be stored.

4. **Last Post Date (Optional)**
   - Option: `--last-post-date`, `--date`, `--time`, `-t`
   - Default: Current date and time
   - Description: Specify the date and time for the last post you want to scrape.

5. **Max Pages (Optional)**
   - Option: `--max-pages`, `--pages`, `-p`
   - Default: `4`
   - Description: Specify the maximum number of pages to scrape.

6. **Max Retries (Optional)**
   - Option: `--max-retries`, `--retries`, `-r`
   - Default: `5`
   - Description: Specify the maximum number of retries for failed downloads.

7. **Show City Codes**
   - Option: `--show-codes`
   - Description: Display a list of city codes and their corresponding city names and then exit. Use this option to see the available city codes for reference.

### Example Usage

Here is an example of how to use the module:

```bash
python divar.py --category apartment-rent --city-code 2 --result-directory Results --last-post-date "2023-09-12 14:30:00" --max-pages 10 --max-retries 3
