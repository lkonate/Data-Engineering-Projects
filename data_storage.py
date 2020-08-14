# my_index.py
# Python Securities Markets Index EOD Data Retrieval & Storage
# Author: L. Konate
# Summer 2020

import time
import datetime # Python Library datetime manipulation functions
import requests
from bs4 import BeautifulSoup
import mysql.connector #MySQL Connector/Python - MySQL driver written in Python


def create_index_db():
    # Desc: Creates a single database along with subsequent tables and relationships

    # Input: None 
    # creates the exchange table
    cur.execute('create database '+ db+ ';')
    cur.execute('use ' +snp ';')
    cur.execute('create table exchange(\
    id int not null auto_increment,\
    abbrev varchar(32) not null,\
    name varchar(255) not null,\
    city varchar(255) null,\
    country varchar(255) null,\
    currency varchar(64) null,\
    timezone_offset time null,\
    created_date datetime not null,\
    last_updated_date datetime not null,\
    primary key(id));')
    #create data_vendor table
    cur.execute('create table data_vendor(\
    id int not null auto_increment,\
    name varchar(64) not null,\
    website_url varchar(255) null,\
    support_email varchar(255) null,\
    created_date datetime not null,\
    last_updated_date datetime not null,\
    primary key(id));')
    #create symbol table
    cur.execute('create table symbol(\
    id int not null auto_increment,\
    exchange_id int null,\
    ticker varchar(32) not null,\
    instrument varchar(64) not null,\
    name varchar(255) null,\
    sector varchar(255) null,\
    currency varchar(32) null,\
    created_date datetime not null,\
    last_updated_date datetime not null,\
    primary key(id),\
    foreign key (exchange_id) references exchange(id));')
    #create daily_price table
    cur.execute('create table daily_price(\
    id int not null auto_increment,\
    data_vendor_id int not null,\
    symbol_id int not null,\
    price_date datetime not null,\
    created_date datetime not null,\
    last_updated_date datetime not null,\
    open_price decimal(19,4) null,\
    high_price decimal(19,4) null,\
    low_price decimal(19,4) null,\
    close_price decimal(19,4) null,\
    adj_close_price decimal(19,4) null,\
    volume bigint null,\
    primary key(id),\
    foreign key (data_vendor_id) references data_vendor(id),\
    foreign key (symbol_id) references symbol(id));')
    
    print('Database successfully Created')
    return True

def retrieve_symbols_from_wiki():
    """
    Download and parse the Wikipedia list of snp500 index
    constituents using requests and BeautifulSoup.
    Returns a list of tuples to add to the database creted.
    """
    # Store the current time, for the created_at record
    now = datetime.datetime.utcnow()
    now = datetime.datetime.strftime(now,"%Y-%m-%d-%H:%M:%S")

    # Create the symbols list to hold the symbols that will be 
    # retrieved based upon the specified index
    symbols = []
    # Use requests and BeautifulSoup to download the
    # index companies specified and obtain the symbol table
    response = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(response.text, features='lxml')
    # This selects the first table, using CSS Selector syntax
    # and then ignores the header row ([1:])
    symbolslist = soup.select("table")[0].select("tr")[1:]
    # Obtain the symbol information for each
    # row in the S&P500 constituents table
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select("td")
        symbols.append(
        (tds[0].select("a")[0].text, # Ticker
        "stock", # this specifies that the securities is a stock
        tds[1].select("a")[0].text, # Name of the securities
        tds[3].text, # Sector
        "USD", now, now))
    
    #symbols_list = symbols    
    #insert_symbols_from_wiki_into_symbols_tbl(symbols_list)
    return symbols

def insert_symbols_from_wiki_into_symbols_tbl(sym):
    """
    Inserts the s&p500 constituents symbols retrieved into the symbols table.
    """

    # Create the insert statement strings
    symbols_tbl_column_names = """ticker, instrument, name, sector,
    currency, created_date, last_updated_date
    """
    symbols_tbl_column_values = ("%s, " * 7)[:-2]
    mysql_insert_statement = "insert into symbol (%s) values (%s);" % (symbols_tbl_column_names, symbols_tbl_column_values)
    
    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    cur.executemany(mysql_insert_statement, sym)
    con.commit()

def processed_tickers():
    """
    Obtains list of ticker symbols for those tickers that were
    successfully retrieved from wiki and inserted into the symbols table.
    This function also calls retrieve_daily_historic_price_data() and
    insert_daily_historic_price_data_into_daily_price_tbl() for the ticker.
    If things work fine for a partcular ticker, processedCount is incremented
    otherwise errorCount is and an exception is thrown.
    """

    processedCount = 0
    errorCount = 0

    #cur = con.cursor()
    cur.execute("use " + db+ ";")
    cur.execute("select id, ticker from symbol;")
    data = cur.fetchall()
    for dd in data:
        try:
            # d[0] & d[1] represent the symbol id and ticker respectively
            dly_data = retrieve_daily_historic_price_data(dd[1])
            #insert_daily_historic_price_data_into_daily_price_tbl('1', processed)
        except Exception as e:
            print('Retrieval Failed for: '+ dd[1])
            errorCount += 1
        else:
            try:
                insert_daily_historic_price_data_into_daily_price_tbl(1, dd[0],dly_data)
            except Exception as e:
                print('Insertion Failed for: '+ dd[1])
                errorCount += 1
            else:
                processedCount += 1
    return ('Processed = ' +processedCount, ' Not Processed = ' + errorCount)

def retrieve_daily_historic_price_data(ticker, start_date='2015-01-01', end_date = '2019-12-31'):
    """
    Obtains data from tiingo and returns a list of tuples.
    
    Params:
    ticker: ticker symbol, e.g. "AAPL" for APPLE, Inc.
    start_date: string in the 'YYYY-MM-DD' format; default = '2015-01-01'
    end_date: string in the 'YYYY-MM-DD' format; default = '2019-12-31'
    """
    # ticker tuple to parse the tiingo web request
    ticker_tup = (ticker, start_date, end_date)
    # replace "YOURTOKEN" at the end of the following line with your tiingo token
    tii_url = "https://api.tiingo.com/tiingo/daily/%s/prices?startDate=%s&endDate=%s&token=YOURTOKEN"
    tii_url = tii_url%ticker_tup 
    price_list = []
    
    # Use the requests library to connect to tiingo and obtain the data for a ticker. 
    # Here, the response will be of json type with a dictionary. You could also use csv
    # if you plan to have it in an excel format. 
    # Please note that using a free tiingo account gives you a max of 500 requests per hour
    # Using a paid subscription allows you 20,000 requests per hour

    tii_data = requests.get(tii_url).json()
    for i in tii_data:
        price_list.append(
        (i['date'].strip('T00:00:00.000Z'), i['open'], i['high'], i['low'], i['close'], i['adjClose'], i['volume'])
        )
    
    return price_list

def insert_daily_historic_price_data_into_daily_price_tbl(data_vendor_id, symbol_id, daily_data):
    """
    Takes a list of tuples of daily data and adds it to the daily_price table.
    Appends the vendor ID and symbol ID to the data.

    Params:
    data_vendor_id: assigned data vendor id
    symbol_id: symbol_id assigned in the table. It goes from 1 to 505 = number of snp500 components
    daily_data: List of tuples of the OHLC data including adj_close and volume.
    """

    # Create the time now for created and updated times
    now = datetime.datetime.utcnow()
    # Amend the data input structure to include the vendor ID and symbol ID
    daily_data = [
    (data_vendor_id, symbol_id, d[0], now, now,
    d[1], d[2], d[3], d[4], d[5], d[6])
    for d in daily_data
    ]
    # Create the insert strings
    daily_price_tbl_column_names = """data_vendor_id, symbol_id, price_date, created_date,last_updated_date, open_price, high_price, low_price,
    close_price, adj_close_price, volume"""
    daily_price_tbl_column_values = ("%s, " * 11)[:-2]    
    mysql_insert_statement = "insert into daily_price (%s) values (%s);" % (daily_price_tbl_column_names, daily_price_tbl_column_values)
    
    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    cur.executemany(mysql_insert_statement, daily_data)
    con.commit()

if __name__ =='__main__':
    
    # S&P500 database to be created
    db = snp_db 
    # Define MySQL configuration parameters
    Config = {"host": "localhost","user": "yourmysql_user", "password": "yourmysql_password"}    

    try:
        # Connect to mysql connector 
        con = mysql.connector.connect(**Config)
    except ConnectionError as e:
        # log a mysql connection error 
        print('Connection to MySQL Failed: %s' %e)
    else:
        try:
            cur = con.cursor()
        except ConnectionError as e:
            print('Cursor Failed: %s' %e)
        else:
            #create_index_db()
            print('\tMysql Connection Successfully Established')

    time.sleep(5)
    create_index_db()
    time.sleep(5)
    symbol_list = retrieve_symbols_from_wiki()
    time.sleep(5)
    insert_symbols_from_wiki_into_symbols_tbl(symbol_list)
    time.sleep(5)
    processed_tickers()
