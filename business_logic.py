from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import time
from constants import (
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
    HEADERS
)
from colorama import Fore
from timerize import timeit

custom_headers = HEADERS

visited_urls = set()

@timeit
def fetch_response(url):
    """
    Sends a GET request to the provided URL and returns the BeautifulSoup object
    of the response content if the status is 200. Otherwise, it logs an error.
    
    Parameters:
    url (str): The URL to request.
    
    Returns:
    BeautifulSoup or None: Parsed HTML content or None in case of failure.
    """
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(Fore.RED + ERROR_FETCHING_PAGE.format(url) + response.content.text)
        return None
    return BeautifulSoup(response.text, "lxml")

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
    
    return {
        "title": title.text.strip() if title else NO_TITLE,
        "price": price.text if price else NO_PRICE,
        "rating": rating.attrs.get("title", NO_RATING).replace("out of 5 stars", "") if rating else NO_RATING,
        "image": image.attrs.get("src") if image else NO_IMAGE,
        "description": description.text.strip() if description else NO_DESCRIPTION,
        "url": url
    }

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
        return None
    visited_urls.add(url)
    print(Fore.LIGHTGREEN_EX + SCRAPING_PRODUCT.format(url[:100]), flush=True)

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
        time.sleep(TIME_SLEEPED)
        print(Fore.GREEN + SCRAPING_NEXT_PAGE.format(next_page_url), flush=True)
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
        raise ValueError("Failed to fetch the search results page.")

    print(Fore.YELLOW + REQUEST_STATUS.format(200))
    link_elements = soup.select(SELECTORS['product_link'])
    page_data = []

    for link in link_elements:
        full_url = urljoin(listing_url, link.attrs.get("href"))
        product_info = scrape_product(full_url)
        if product_info:
            page_data.append(product_info)

    page_data += handle_pagination(soup, listing_url)

    return page_data