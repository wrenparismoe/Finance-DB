# finance-db
A basic financial analysis service to make stock data and evaluation techniques accessible and easier to understand for the average individual. Implemented as a website, this service allows anyone to analyze stock information of S&P 500 companies to better prepare themselves for making personal investments.
The service is built using an SQL database containing the complete stock history of the S&amp;P 500 with a basic web interface implemented in python and html for users to interact with financial data.

## Data Retreival Strategy

Yahoo Finance is an online platform used both by investment professionals and regular citizens to access accurate and updated financial and economic records. All data from Yahoo Finance can be accessed through packages in higher level programming languages such as R, Python, and Matlab. A single csv file with the tickers, stock names, and sectors of all S&P 500 companies is used as a basis to fill the database. This method uses the Python package “yahoo_fin” to pull data from https://finance.yahoo.com into a DataFrame for each stock in the csv file. Then, using the official MySQL/Python Connector, the data is sent from Python to the MySQL server to form each individual stock table. 
Code to import sample data from Yahoo Finance to Python:

```python
from yahoo_fin import stock_info as si

data = pd.read_csv("C:/.../S&P500.csv", names=["ticker", "stock_name", "sector"])
tickers = data["ticker"]
for x in tickers:
	stock_data = pd.DataFrame(si.get_data(x, index_as_date=False))
```

Implementing this code builds a 2-Dimensional DataFrame for all stocks listed in ‘tickers’, each with the attributes date, open price, high price, low price, close price, adjusted close, volume, and ticker. (Not shown) After the DataFrame is created it is exported to the MySQL Server before moving on to the next ticker.

# Implementation:

1. In SQLconnector.py and flaskWebsite.py: 
    Change all instances of :
    ```python
    conn = sqlconnection.connect(​user​=​'root'​, ​password​=​''​, ​host​=​'127.0.0.1'​, database​=​'financedb'​) 
    ```
    To: your username, password, and host for the MySQL database 
 
    Change all CSV paths:
    ```python
    data = pd.read_csv(​"C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/S&P500.csv"​, ​names​=[​"ticker"​, ​"stock_name"​, ​"sector"​]) 
  
    users = pd.read_csv(​"C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/usersimporttest.csv"​, ​names​=[​"username"​, ​"password"​, ​"fname"​, ​"lname"​, ​"email"​, "subscriber"​]) 
    portfolio = pd.read_csv(​"C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/portfolioimporttest.csv"​, ​names​=[​"portfolio_name"​]) 
    has_portfolio = pd.read_csv(​"C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/has_portfolioimporttest.csv"​, ​names​=[​"login_id"​,​"portfolio_id"​]) 
    has_stock = pd.read_csv(​"C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/has_stockimporttest.csv"​, ​names​=[​"portfolio_id"​, ​"ticker"​]) 
    ```
    To: your path for the CSVs -- (users, portfolio, has_portfolio, has_stock are only needed if inital test data is wanted in the database)
  
2. Install all needed external packages/modules listed at the top of SQLconnector.py and flaskWebsite.py using anaconda or pip into your environment such as: 

    pip install numpy 
    
    pip install yahoo_fin 
    
    pip install mysql_connector_python 
    
    Etc. 
  
3. Confirm the mysql_connector is connected and working 

4. Run setup code in this order to build Database (running SQLconnector.py before financedb.sql will result in errors) 

    a. Financedb.sql, then connect to the virtual server 
    
    b. SQLconnector.py 
    
    *Note, running the default SP500.csv (instead of SP500test.csv) can take up to 30 minutes or more to import all 4 million rows of stock data. There was no way around this. We tried.*
    
5. Place flaskWebsite.py, a ‘static’ folder, and a ‘templates’ folder in the same project folder 

6. Run flaskWebsite.py 

    a. If the database has not been updated with data from the latest stock market closing date, updateStockData() will run before the website application is initialized 
    
    b. Only run importUsers(users), importPortfolio(portfolio), importHas_Portfolio(has_portfolio), and importHas_Stock(has_stock) if initial test data is wanted
    
7. Visit ​http://127.0.0.1:5000/​ (unless your host address is different) to open the web application 

    Notes: 
    
      a. View Trading Strategy is for subscribers only 
      
      b. Specific features like viewing “Statistics and Metrics”, “Viewing trading strategy”, etc. can take a few seconds to load due to the sheer volume of data and lack of parallel processing power 
