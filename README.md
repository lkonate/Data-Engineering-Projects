Data Platform Development with MySQL

Overview

In this project, we apply Data Modeling with MySQL and build an ETL pipeline using Python. A boutique trading firm wants to build a proprietary trading platform and a strategy using S&P500 EOD data for their activities. Here, we retrieve and store both the index components and their values using tiingo as the data open source and MySQL as the database system using Python.

Index Components

The components list is the most updated one as of January 1, 2021.
Sample Record :

Query:
Select * from symbol limit 10;

+-----------+--------+------------+----------------------------+------------------------+----------+---------------------+
| symbol_id | ticker | instrument | name                       | sector                 | currency | created_date        |
+-----------+--------+------------+----------------------------+------------------------+----------+---------------------+
|         1 | MMM    | stock      | 3M Company                 | Industrials            | USD      | 2021-01-24 19:45:47 |
|         2 | ABT    | stock      | Abbott Laboratories        | Health Care            | USD      | 2021-01-24 19:45:47 |
|         3 | ABBV   | stock      | AbbVie Inc.                | Health Care            | USD      | 2021-01-24 19:45:47 |
|         4 | ABMD   | stock      | ABIOMED Inc                | Health Care            | USD      | 2021-01-24 19:45:47 |
|         5 | ACN    | stock      | Accenture plc              | Information Technology | USD      | 2021-01-24 19:45:47 |
|         6 | ATVI   | stock      | Activision Blizzard        | Communication Services | USD      | 2021-01-24 19:45:47 |
|         7 | ADBE   | stock      | Adobe Inc.                 | Information Technology | USD      | 2021-01-24 19:45:47 |
|         8 | AMD    | stock      | Advanced Micro Devices Inc | Information Technology | USD      | 2021-01-24 19:45:47 |
|         9 | AAP    | stock      | Advance Auto Parts         | Consumer Discretionary | USD      | 2021-01-24 19:45:47 |
|        10 | AES    | stock      | AES Corp                   | Utilities              | USD      | 2021-01-24 19:45:47 |
+-----------+--------+------------+----------------------------+------------------------+----------+---------------------+

Index Dataset
EOD dataset of the S&P500 index as of January 24, 2021 using tiingo.

Sample Record :

Query:
select * from daily_price limit 10;

+----------------+-----------+---------------------+------------+------------+-----------+-------------+-----------------+---------+
| daily_price_id | symbol_id | price_date          | open_price | high_price | low_price | close_price | adj_close_price | volume  |
+----------------+-----------+---------------------+------------+------------+-----------+-------------+-----------------+---------+
|              1 |         1 | 2015-01-02 00:00:00 |   164.7100 |   165.0800 |  162.7300 |    164.0600 |        138.1253 | 2117562 |
|              2 |         1 | 2015-01-05 00:00:00 |   163.0000 |   163.6400 |  160.0800 |    160.3600 |        135.0102 | 3692901 |
|              3 |         1 | 2015-01-06 00:00:00 |   160.8200 |   161.3699 |  157.7440 |    158.6500 |        133.5705 | 3537144 |
|              4 |         1 | 2015-01-07 00:00:00 |   159.9000 |   160.2800 |  158.9400 |    159.8000 |        134.5387 | 3081291 |
|              5 |         1 | 2015-01-08 00:00:00 |   160.6500 |   163.6900 |  160.5200 |    163.6300 |        137.7633 | 3146333 |
|              6 |         1 | 2015-01-09 00:00:00 |   163.8500 |   164.0000 |  161.2700 |    161.6200 |        136.0710 | 2365485 |
|              7 |         1 | 2015-01-12 00:00:00 |   162.3900 |   162.3900 |  160.0200 |    160.7400 |        135.3302 | 2149230 |
|              8 |         1 | 2015-01-13 00:00:00 |   162.2300 |   164.3840 |  159.4500 |    160.6200 |        135.2291 | 2706698 |
|              9 |         1 | 2015-01-14 00:00:00 |   159.0400 |   160.5300 |  158.5000 |    159.8400 |        134.5724 | 1983535 |
|             10 |         1 | 2015-01-15 00:00:00 |   160.8900 |   161.4400 |  159.3675 |    159.6600 |        134.4209 | 1881406 |
+----------------+-----------+---------------------+------------+------------+-----------+-------------+-----------------+---------+


Index Dataset
EOD dataset of Abbot Laboratories as of January 24, 2021 using a MySQL query.

Query:
select dp.price_date, dp.open_price, dp.high_price, dp.low_price, dp.close_price, dp.adj_close_price, dp.volume from symbol as sym inner join daily_price as dp on dp.symbol_id = sym.symbol_id where sym.ticker = "ABT" limit 10;

Sample Record :

+---------------------+------------+------------+-----------+-------------+-----------------+---------+
| price_date          | open_price | high_price | low_price | close_price | adj_close_price | volume  |
+---------------------+------------+------------+-----------+-------------+-----------------+---------+
| 2015-01-02 00:00:00 |    45.2500 |    45.4501 |   44.6350 |     44.9000 |         39.7093 | 3217165 |
| 2015-01-05 00:00:00 |    44.8000 |    45.4000 |   44.6300 |     44.9100 |         39.7181 | 5735878 |
| 2015-01-06 00:00:00 |    44.9900 |    45.1100 |   43.9300 |     44.4000 |         39.2671 | 6589381 |
| 2015-01-07 00:00:00 |    44.7300 |    44.9400 |   44.3800 |     44.7600 |         39.5855 | 4609541 |
| 2015-01-08 00:00:00 |    45.1900 |    45.7850 |   45.0100 |     45.6800 |         40.3991 | 4890877 |
| 2015-01-09 00:00:00 |    45.7500 |    45.8700 |   45.1100 |     45.2000 |         39.9746 | 4727267 |
| 2015-01-12 00:00:00 |    45.3800 |    45.7600 |   44.9400 |     45.5800 |         40.3107 | 6178783 |
| 2015-01-13 00:00:00 |    45.3400 |    45.5300 |   44.2500 |     44.6100 |         39.6651 | 6744933 |
| 2015-01-14 00:00:00 |    44.2900 |    44.6600 |   43.9300 |     44.2800 |         39.3717 | 5865894 |
| 2015-01-15 00:00:00 |    44.5000 |    44.6700 |   43.9000 |     43.9500 |         39.0782 | 3920286 |
+---------------------+------------+------------+-----------+-------------+-----------------+---------+

Schema

Database Tables
symbol – repository of all S&P500 constituents. The list should be updated periodically to account for new entries and exits from the index. Columns of the table are:
symbol_id, ticker, instrument, name, sector, currency, and created_date

daily_price – repository of all S&P500 constituents end-of-day trading data for the past 6 years. The time span could be adjusted as needed, along with the list of the index constituents to account for new entries and exits. Columns of the table are:

daily_price_id, symbol_id, price_date, open_price, high_price, low_price, close_price, adj_close_price, volume
Project Files

database.py -> contains the code for setting up the database and tables. Running this file establishes the mysql conncection, sets up the database, and creates all the tables.

index.py -> contains the code for retrieving the desired index constituents, setting them in a table from the previously created database.
daily_price -> contains the historical daily price data retrieved using yfinance and inserted in some of the tables created by our database.

Environment

Python 3.7 or above
MySQL  9.5 or above
tiingo using either a free or paid subscription

How to run this code???

Run the drive program main.py as below.
python main.py

The create_databse.py and create_tables.py files can also be run independently as below:
python create_database.py 
python create_tables.py

Reference:
Python3 Documentaion
MySQL Documentation
Pandas Documentation
