import argparse
from service.business_logic import parse_listing
from constants.constants import PRODUCT_ARG_HELP, PATH_ARG_HELP, FORMAT_ARG_HELP, SUPPORTED_FORMATS, FILE_FORMAT_HANDLERS, DEFAULT_REGION, ERROR_UNSUPPORTED_REGION, SUPPORTED_REGIONS
import pandas as pd
from colorama import Fore, init
from halo import Halo
from utils.timerize import timeit
import os, sys
import logging
from constants.constants import DEBUG_LEVEL

init(autoreset=True)
logging.basicConfig(
    filename="logging/app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=DEBUG_LEVEL
)


@timeit
def save_data(data, path, file_format):
    """
    Save the scraped data to the specified file format.

    Parameters:
    data (list): List of product information dictionaries.
    path (str): Path to save the file.
    file_format (str): The format to save the file in. Supported formats: 'csv', 'xlsx', 'json'.
    """
    df = pd.DataFrame(data)
    logging.debug(f"data from Amazon: {df}")
    
    if file_format in FILE_FORMAT_HANDLERS:
        logging.info(f"File format {file_format} is supported")
        FILE_FORMAT_HANDLERS[file_format](df, path)
    else:
        logging.error(f"Unsupported file format: {file_format}. Supported formats are {', '.join(SUPPORTED_FORMATS)}")
        raise ValueError(Fore.RED + f"Unsupported file format: {file_format}. Supported formats are {', '.join(SUPPORTED_FORMATS)}")

@timeit
def run_scrapper(product, path="amazon_products.csv", file_format="csv", location=DEFAULT_REGION):
    """
    Main function to coordinate the scrapping and exporting process.
    
    Parameters:
    product (str): Product to search on Amazon.
    path (str): Path to save the file (optional).
    file_format (str): File format to save the data (optional).
    """
    
    if location not in SUPPORTED_REGIONS:
            supported = ', '.join(SUPPORTED_REGIONS.keys())
            print(Fore.RED + ERROR_UNSUPPORTED_REGION.format(location, supported))
            logging.error(ERROR_UNSUPPORTED_REGION.format(location, supported))
            sys.exit(1)
    spinner = Halo(text=f"Scraping results for {product}...", spinner="dots", color="cyan")
    spinner.start()
    try:
        logging.info("Starting run_scrapper process")
        
        
        url = SUPPORTED_REGIONS[location].format(product.replace(' ', '+'))
        logging.debug(f"Accessing with url: {url}")
        data = parse_listing(url)
        
        _, file_extension = os.path.splitext(path)
        if not file_extension:
            path = f"{path}.{file_format}"
        logging.debug(f"path to save the file: {path}")
        
        save_data(data, path, file_format)
        spinner.succeed(Fore.GREEN + f"Data successfully saved to {path}")
    except ValueError as e:
        logging.error(str(e))
        spinner.fail(Fore.RED + str(e))
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        spinner.fail(Fore.RED + f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Amazon Product Scrapper")
    parser.add_argument("--product", required=True, help=PRODUCT_ARG_HELP)
    parser.add_argument("--path", default="amazon_products", help=PATH_ARG_HELP)
    parser.add_argument("--format", default="csv", help=FORMAT_ARG_HELP, choices=SUPPORTED_FORMATS)
    parser.add_argument("--location", default=DEFAULT_REGION, help="Amazon region (e.g., 'es', 'com', 'co.uk', 'de'). Default is 'es' for Spain.")
    
    args = parser.parse_args()
    logging.debug(f"arguments: {args.product=}, {args.path=}, {args.format=}, {args.location=}")
    run_scrapper(args.product, args.path, args.format, args.location)

