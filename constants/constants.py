# constants.py

# Argument help texts
PRODUCT_ARG_HELP = "The product to search for on Amazon"
PATH_ARG_HELP = "Path to save the CSV file (optional)"
FORMAT_ARG_HELP = "Format to save the file (csv, xlsx, json). Default is csv."
TIME_SLEEPED = 3

# Supported formats
SUPPORTED_FORMATS = ["csv", "xlsx", "json"]

# Supported file formats and their corresponding saving functions
FILE_FORMAT_HANDLERS = {
    "csv": lambda df, path: df.to_csv(path, index=False),
    "xlsx": lambda df, path: df.to_excel(path, index=False),
    "json": lambda df, path: df.to_json(path, orient="records", indent=4),
}

# Logging and error messages
ERROR_FETCHING_PAGE = "Error in getting webpage: {}"
SCRAPING_PRODUCT = "Scrapping product from {}"
SCRAPING_NEXT_PAGE = "Scrapping next page: {}"
REQUEST_STATUS = "request-{}: Scrapping..."

# Default values for missing data
NO_TITLE = "N/A"
NO_PRICE = "N/A"
NO_RATING = "No Rating"
NO_IMAGE = "N/A"
NO_DESCRIPTION = "N/A"

# HTTP headers for requests
HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}

# HTML selectors for scraping
SELECTORS = {
    "title": "#productTitle",
    "price": "span.a-offscreen",
    "rating": "#acrPopover",
    "image": "#landingImage",
    "description": "#productDescription",
    "pagination_next": "a.s-pagination-next",
    "product_link": "[data-asin] h2 a"
}

# Supported Amazon regions (countries)
SUPPORTED_REGIONS = {
    "es": "https://www.amazon.es/s?k={}",
    "com": "https://www.amazon.com/s?k={}",
    "co.uk": "https://www.amazon.co.uk/s?k={}",
    "de": "https://www.amazon.de/s?k={}",
    "fr": "https://www.amazon.fr/s?k={}",
    "it": "https://www.amazon.it/s?k={}"
}

# Default region (Spain)
DEFAULT_REGION = "es"

# Error message for unsupported regions
ERROR_UNSUPPORTED_REGION = "Unsupported region '{}'. Supported regions are: {}"