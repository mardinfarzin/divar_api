# Documentation for `divar_api` Code

## Introduction
This code is designed to scrape and process advertisement data from the **Divar** website. It first retrieves the HTML content of the page using web scraping, then extracts key information from each ad such as title, image, location, price, and description. Additionally, it uses Divar's internal API to fetch more detailed descriptions of the ads.

## Code Structure

### 1. Function `get_page_content(url)`
This function is used to fetch the HTML content of a given URL.
- **Input**: 
  - `url`: The URL of the website from which to retrieve the HTML content.
- **Output**: HTML content as a string.
- **Error Handling**: Displays an error message if there is an issue with fetching the HTML content.

### 2. Function `get_api_data(token)`
This function is designed to retrieve ad descriptions from Divar's API using the ad's unique token.
- **Input**: 
  - `token`: The unique token corresponding to each ad.
- **Output**: The ad description or "No description available" if there is an issue.

### 3. Function `divar_api(url)`
The main function to parse HTML content and extract key ad information.
- **Input**: 
  - `url`: The URL of the Divar page containing the list of ads.
- **Output**: 
  - A list of ads with the following details:
    - `title`: The title of the ad.
    - `thumbnail`: The image of the ad.
    - `location`: The location of the ad.
    - `token`: The unique token for each ad.
    - `link`: The ad link on Divar's website.
    - `description`: The ad description retrieved via the API.
    - `price`: The price of the ad.

### Example Usage
```python
url = 'https://divar.ir/s/iran/restaurant-equipment?goods-business-type=personal'
print(divar_api(url))
