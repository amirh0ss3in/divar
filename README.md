# Divar Scraper with Multithreading

This Python script allows you to scrape data from the Divar website, specifically for real estate listings in different categories and cities. It utilizes the Divar API to retrieve and store information about real estate listings in an Excel file.

## Table of Contents
- [Getting Started](#getting-started)
- [Usage](#usage)

## Important Note
The whole point of this scraping is to get to the tokens. When obtaining the tokens, we can access the webpage of that specific ad and then extract whatever further information we want. any link in divar can be accessed by its token like this:

      https://divar.ir/v/-/TOKEN
      
Example:

      https://divar.ir/v/-/AZ4LldV9

## Getting Started

To get started with this script, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/amirh0ss3in/divar.git
   ```
   
## Usage

2. Here is an example of how to use the script:

  ```python
  scrape(city_code=1,
         category="apartment-rent",
         date_time_str="2023-09-06 21:00:00",
         MAX_PAGES=2000,
         MAX_RETRY_ATTEMPTS=5)
  ```

- city_code: The code for the city you want to scrape data for.
- category: The specific real estate category you are interested in (e.g., "apartment-rent").
- date_time_str: The date and time from which you want to start scraping listings.
- MAX_PAGES: The maximum number of pages to scrape.
- MAX_RETRY_ATTEMPTS: The maximum number of retry attempts if an error occurs during scraping.

The scraped data will be saved in json files in the "Results" folder.
