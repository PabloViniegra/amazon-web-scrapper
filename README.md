# Amazon Scraper Script

This script scrapes product information from Amazon Spain based on a search term provided by the user. It gathers information such as product title, price, rating, description, and image URL, and saves the results in CSV, XLSX, or JSON formats.

## Requirements

Before running the script, you need to have the following installed on your machine:

1. **Python 3.7+**: Make sure you have Python installed. You can check your Python version by running:

    ```bash
    python --version
    ```

2. **Pip**: Ensure that you have `pip` installed for managing Python packages. You can verify by running:

    ```bash
    pip --version
    ```

## Installing Dependencies

To install the necessary dependencies, follow these steps:

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/amazon-scraper.git
    cd amazon-scraper
    ```

2. Install the required Python packages by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

    This will install the following libraries:
    - `requests`: To make HTTP requests to Amazon.
    - `beautifulsoup4`: For parsing and scraping the HTML content.
    - `pandas`: For saving the scraped data in different formats.
    - `colorama`: For colored console outputs.
    - `halo`: For adding spinners and feedback during the scraping process.

## Usage

The script takes a product search term and scrapes Amazon Spain for results. You can run the script via the command line using the following format:

```bash
python scrapper.py --product "search_term" --path "output_file_path" --format "output_format"
```

### Examples

1. **Basic Usage**: Searching for a product on Amazon Spain and saving the results as a CSV file (default):

    ```bash
    python scrapper.py --product "laptop"
    ```

    **Expected output**:
    - The script will scrape Amazon Spain (`amazon.es`) for laptops.
    - It will save the results in a CSV file called `amazon_products.csv` in the current directory.
    - You will see colored logs and spinners indicating the progress of the scraping process.

2. **Scraping Amazon US**: Specify a different Amazon location using the `--location` option:

    ```bash
    python scrapper.py --product "smartphone" --location "com"
    ```

    **Expected output**:
    - The script will scrape Amazon US (`amazon.com`) for smartphones.
    - It will save the results in a CSV file called `amazon_products.csv`.

3. **Saving in XLSX format**: Specify a different output format using the `--format` option:

    ```bash
    python scrapper.py --product "smartphone" --format "xlsx"
    ```

    **Expected output**:
    - The script will scrape Amazon Spain for smartphones.
    - It will save the results in an Excel file (`amazon_products.xlsx`).

4. **Specifying a different output file path**: Save the results in a specific path and format:

    ```bash
    python scrapper.py --product "headphones" --path "./results/headphones_data.json" --format "json"
    ```

    **Expected output**:
    - The script will scrape Amazon Spain for headphones.
    - It will save the results in a JSON file at the specified path.

### Error Handling

If the user provides an invalid format (i.e., other than `csv`, `xlsx`, or `json`), the script will raise an error:

```bash
Error: Invalid format specified. Supported formats are: csv, xlsx, json.
```

Additionally, if there are issues with fetching product data from Amazon, the script will display a red error message indicating the problem. For example:

```bash
Error getting information: 503
```

This indicates that the request to Amazon failed with an HTTP 503 (Service Unavailable) error. The script will stop at this point and will not proceed to the next page of results.

### Expected Output

Depending on the format chosen, the script will save the scraped product data in one of the following file types:

- **.csv:** A comma-separated values file containing all product details.
- **.xlsx:** An Excel spreadsheet with product details.
- **.json:** A JSON file containing the scraped product information in key-value format.

Logs will be shown in the terminal with colored messages for each step, and spinners will indicate progress while fetching data from Amazon.
