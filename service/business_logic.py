from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time, random, logging
from constants.constants import (
    ERROR_FETCHING_PAGE,
    SCRAPING_PRODUCT,
    SCRAPING_NEXT_PAGE,
    REQUEST_STATUS,
    NO_TITLE,
    NO_PRICE,
    NO_RATING,
    NO_IMAGE,
    NO_DESCRIPTION,
    HEADERS,
    SELECTORS,
    TIME_SLEEPED,
    HEADERS,
    DEFAULT_RETRIES,
    TIME_BETWEEN_RETRY,
    DEBUG_LEVEL
)
from colorama import Fore
from utils.timerize import timeit

logging.basicConfig(
    filename="logging/app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=DEBUG_LEVEL
)

custom_headers = HEADERS

visited_urls = set()

@timeit
def fetch_response(url, retries=DEFAULT_RETRIES):
    """
    Sends a GET request to the provided URL and returns the BeautifulSoup object
    of the response content if the status is 200. If the request fails, it logs an error 
    and retries the request up to a specified number of attempts.
    
    Parameters:
    url (str): The URL to request.
    retries (int): The number of times to retry the request if the status code is not 200. 
                   Defaults to DEFAULT_RETRIES.

    Returns:
    BeautifulSoup or None: Parsed HTML content if the request is successful (status code 200),
                           or None if all retries fail or if an error occurs.
    """
    time.sleep(TIME_SLEEPED + random.uniform(0, 2))
    for attempt in range(retries):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "lxml")
        print(Fore.RED + ERROR_FETCHING_PAGE.format(url) + f" Status Code: {response.status_code}. Retrying... ({attempt + 1}/{retries})")
        logging.info(f" Status Code: {response.status_code}. Retrying... ({attempt + 1}/{retries})")
        time.sleep(TIME_BETWEEN_RETRY)
    return None

@timeit
def extract_product_data(soup, url):
    """
    Extracts product details from the product page's BeautifulSoup object.
    
    Parameters:
    soup (BeautifulSoup): The parsed HTML content of the product page.
    url (str): The URL of the product.
    
    Returns:
    dict: A dictionary containing product information.
    """
    title = soup.select_one(SELECTORS['title'])
    price = soup.select_one(SELECTORS['price'])
    rating = soup.select_one(SELECTORS['rating'])
    image = soup.select_one(SELECTORS['image'])
    description = soup.select_one(SELECTORS['description'])
    result = {
        "title": title.text.strip() if title else NO_TITLE,
        "price": price.text if price else NO_PRICE,
        "rating": rating.attrs.get("title", NO_RATING).replace("out of 5 stars", "") if rating else NO_RATING,
        "image": image.attrs.get("src") if image else NO_IMAGE,
        "description": description.text.strip() if description else NO_DESCRIPTION,
        "url": url
    }
    logging.debug(f"row: {result}")
    return result

@timeit
def scrape_product(url):
    """
    Scrapes product information from a single product URL.
    
    Parameters:
    url (str): The product URL.
    
    Returns:
    dict or None: Dictionary with product information, or None if an error occurs.
    """
    if url in visited_urls:
        logging.warning(f"{url} was already visited")
        return None
    visited_urls.add(url)
    print(Fore.LIGHTGREEN_EX + SCRAPING_PRODUCT.format(url[:100]), flush=True)
    logging.info(SCRAPING_PRODUCT.format(url[:100]))
    soup = fetch_response(url)
    if not soup:
        return None

    return extract_product_data(soup, url)

@timeit
def handle_pagination(soup, listing_url):
    """
    Handles the pagination by checking if there's a next page, and recursively 
    scrapes the products from subsequent pages.
    
    Parameters:
    soup (BeautifulSoup): Parsed HTML content of the listing page.
    listing_url (str): The base URL for pagination.

    Returns:
    list: A list of product dictionaries from subsequent pages.
    """
    next_page_el = soup.select_one(SELECTORS['pagination_next'])
    if next_page_el:
        next_page_url = urljoin(listing_url, next_page_el.attrs.get('href'))
        time.sleep(TIME_SLEEPED + random.uniform(0, 2)) # To avoid that Amazon blockes your IP
        print(Fore.GREEN + SCRAPING_NEXT_PAGE.format(next_page_url), flush=True)
        logging.info(SCRAPING_NEXT_PAGE.format(next_page_url))
        return parse_listing(next_page_url)
    return []

@timeit
def parse_listing(listing_url):
    """
    Scrapes product data from an Amazon search results page.
    
    Parameters:
    listing_url (str): The URL of the search results page.
    
    Returns:
    list: A list of dictionaries with product information.
    """
    soup = fetch_response(listing_url)
    if not soup:
        print(Fore.RED + "Skipping this page due to fetch error.")
        logging.warning("Skipping this page due to fetch error.")
        return []

    print(Fore.YELLOW + REQUEST_STATUS.format(200))
    logging.info(REQUEST_STATUS.format(200))
    link_elements = soup.select(SELECTORS['product_link'])
    page_data = []

    for link in link_elements:
        full_url = urljoin(listing_url, link.attrs.get("href"))
        product_info = scrape_product(full_url)
        if product_info:
            page_data.append(product_info)

    try:
        page_data += handle_pagination(soup, listing_url)
    except Exception as e:
        print(Fore.RED + f"Error handling pagination: {str(e)}")
        logging.error(f"Error handling pagination: {str(e)}")
    return page_data