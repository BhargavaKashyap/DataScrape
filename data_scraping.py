import requests
from bs4 import BeautifulSoup
import psycopg2
import unicodedata
import re

# Database configuration
db_config = {
    'dbname': 'web_data',
    'user': 'postgres',
    'password': 'test123',
    'host': 'localhost',
    'port': '5432'
}

# Function to create tables if they do not exist
def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            quote TEXT,
            author TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id SERIAL PRIMARY KEY,
            name TEXT,
            symbol TEXT,
            price_usd NUMERIC
        )
        """
    ]
    conn = None
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        # Create table one by one
        for command in commands:
            cur.execute(command)
        # Commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# Function to store data in PostgreSQL
def store_data(query, data):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Data cleaning function for quotes
def clean_quote(text):
    # Remove unnecessary whitespace and quotes
    text = text.strip().strip('“”')
    # Remove special characters and normalize Unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

# Data cleaning function for authors
def clean_author(author):
    # Ensure proper capitalization
    author = author.title()
    # Remove special characters and normalize Unicode characters
    author = unicodedata.normalize('NFKD', author).encode('ascii', 'ignore').decode('ascii')
    # Remove special characters
    author = re.sub(r'[^\w\s]', '', author)
    # Normalize whitespace
    author = ' '.join(author.split())
    return author

# Scrape quotes from Quotes to Scrape
def scrape_quotes():
    url = 'http://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text

        # Clean the data
        text = clean_quote(text)
        author = clean_author(author)

        # Validate the data
        if text and author:
            data = (text, author)
            query = "INSERT INTO quotes (quote, author) VALUES (%s, %s)"
            store_data(query, data)

# Data cleaning function for cryptocurrency names
def clean_crypto_name(name):
    # Remove any extraneous characters
    name = re.sub(r'\W+', ' ', name).strip()
    # Normalize case
    name = name.title()
    # Normalize Unicode characters
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    # Normalize whitespace
    name = ' '.join(name.split())
    return name

# Data cleaning function for cryptocurrency symbols
def clean_crypto_symbol(symbol):
    # Ensure the symbol is uppercase
    symbol = symbol.upper()
    # Normalize Unicode characters
    symbol = unicodedata.normalize('NFKD', symbol).encode('ascii', 'ignore').decode('ascii')
    # Normalize whitespace
    symbol = ' '.join(symbol.split())
    return symbol

# Get cryptocurrency prices from CoinGecko API
def get_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 10, 'page': 1, 'sparkline': 'false'}
    response = requests.get(url, params=params)
    cryptos = response.json()

    for crypto in cryptos:
        name = crypto['name']
        symbol = crypto['symbol']
        price_usd = crypto['current_price']

        # Clean the data
        name = clean_crypto_name(name)
        symbol = clean_crypto_symbol(symbol)

        # Validate the data
        if name and symbol and price_usd is not None:
            data = (name, symbol, price_usd)
            query = "INSERT INTO crypto_prices (name, symbol, price_usd) VALUES (%s, %s, %s)"
            store_data(query, data)

# Main function
if __name__ == '__main__':
    # Create tables if they do not exist
    create_tables()
    # Scrape quotes and store in PostgreSQL
    scrape_quotes()
    # Get cryptocurrency prices and store in PostgreSQL
    get_crypto_prices()
    print("Data scraping, cleaning, and storing completed successfully!")
