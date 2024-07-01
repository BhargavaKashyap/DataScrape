# Web Scraping and Data Storing Project

This project scrapes quotes from a website and retrieves cryptocurrency prices from an API. The data is then cleaned and stored in a PostgreSQL database.

## Prerequisites

Ensure you have the following installed:

- Python 3.6+
- PostgreSQL
- Python libraries: `requests`, `beautifulsoup4`, `psycopg2`

You can install the necessary Python libraries using:

```bash
pip install requests beautifulsoup4 psycopg2
```

## Database Configuration

Update the `db_config` dictionary in the script with your PostgreSQL database credentials.

```python
db_config = {
    'dbname': 'web_data',
    'user': 'postgres',
    'password': 'test123',
    'host': 'localhost',
    'port': '5432'
}
```

## Project Structure

- `create_tables()`: Creates the necessary tables (`quotes` and `crypto_prices`) in the PostgreSQL database.
- `store_data(query, data)`: Stores the provided data in the PostgreSQL database using the specified query.
- `clean_quote(text)`: Cleans and normalizes quote text.
- `clean_author(author)`: Cleans and normalizes author names.
- `scrape_quotes()`: Scrapes quotes from [Quotes to Scrape](http://quotes.toscrape.com/) and stores them in the database.
- `clean_crypto_name(name)`: Cleans and normalizes cryptocurrency names.
- `clean_crypto_symbol(symbol)`: Cleans and normalizes cryptocurrency symbols.
- `get_crypto_prices()`: Retrieves cryptocurrency prices from the CoinGecko API and stores them in the database.

## Running the Project

To run the project, execute the script:

```bash
python script_name.py
```

This will:

1. Create the necessary tables if they do not exist.
2. Scrape quotes from the website and store them in the `quotes` table.
3. Retrieve cryptocurrency prices from the CoinGecko API and store them in the `crypto_prices` table.

Upon successful execution, you will see the message:

```
Data scraping, cleaning, and storing completed successfully!
```

## Acknowledgments

This project uses data from:

- [Quotes to Scrape](http://quotes.toscrape.com/)
- [CoinGecko API](https://www.coingecko.com/en/api)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.