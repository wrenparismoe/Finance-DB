from yahoo_fin import stock_info as si
import pandas as pd
import mysql_connector_python.mysql.connector as sqlconnection
import mysql_connector_python.mysql.connector.errorcode as errorcode
import os
import binascii
# hash generator with hashlib
import hashlib
# generate unique user id https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python
import uuid


pd.options.display.max_columns = 999
pd.options.display.width = 999

data = pd.read_csv("C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/S&P500.csv", names=["ticker", "stock_name", "sector"])

tickers = data["ticker"]

# date        open         high          low        close     adjclose      volume ticker
users = pd.read_csv("C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/usersimporttest.csv", names=["username", "password", "fname", "lname", "email", "subscriber"])
portfolio = pd.read_csv("C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/portfolioimporttest.csv", names=["portfolio_name"])
has_portfolio = pd.read_csv("C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/has_portfolioimporttest.csv", names=["login_id","portfolio_id"])
has_stock = pd.read_csv("C:/Users/wrenp/Documents/Spring 2019/Databases/Final Project/has_stockimporttest.csv", names=["portfolio_id", "ticker"])

# https://medium.com/@dwernychukjosh/sha256-encryption-with-python-bf216db497f9
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def str2boolint(str):
    test = True
    if str == test:
        return 1
    else:
        return 0

# date        open         high          low        close     adjclose      volume ticker


def createStockTables(tickers):
    conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    for x in tickers:
        createTable = ("Create Table " + x + "( "
                       "eod date not null, "
                       "open_price float, "
                       "high_price float, "
                       "low_price float, "
                       "close_price float, "
                       "adjclose float, "
                       "volume float, "
                       "ticker varchar(5) not null, "
                       "Primary Key(ticker, eod), "
                       "Foreign Key(ticker) references SP500(ticker));")

        try:
            print("Creating table: ", x)
            cursor.execute(createTable)
        except sqlconnection.Error as er:
            if er.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table already exists")
            else:
                print(er.msg)
        else:
            print("Table was successfully created")

    cursor.close()
    conn.close()


createStockTables(tickers)


def insertSP500(data):
    conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    insertSP500 = ("INSERT INTO SP500"
                      "(ticker, stock_name, sector) "
                      "VALUES (%s, %s, %s)")

    for x in range(data['ticker'].count()):
        stock_data = [data['ticker'].loc[x], data['stock_name'].loc[x], data['sector'].loc[x]]
        cursor.execute(insertSP500, stock_data)
        print("INSERT INTO SP500(ticker, stock_name, sector) VALUES " + str(stock_data))

    conn.commit()
    cursor.close()
    conn.close()


insertSP500(data)


def insertStockData(tickers):
    for x in tickers:
        conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
        cursor = conn.cursor()

        insertStockData = ("INSERT INTO " + x + " "
                           "(eod, open_price, high_price, low_price, close_price, adjclose, volume, ticker) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        try:
            data = pd.DataFrame(si.get_data(x, index_as_date=False))
            for y in range(data['ticker'].count()):
                print(y)
                stock_data = [data['date'].loc[y], float(data['open'].loc[y]), float(data['high'].loc[y]), float(data['low'].loc[y]), float(data['close'].loc[y]), float(data['adjclose'].loc[y]), float(data['volume'].loc[y]), data['ticker'].loc[y]]
                cursor.execute(insertStockData, stock_data)
                print("INSERT INTO " + x + " (eod, open_price, high_price, low_price, close_price, adjclose, volume, ticker) VALUES " + str(stock_data))


        except (KeyError, ValueError):
            print("No Stock Data Available For " + x)
            pass

        print("Done Inserting Data For " + x)

        conn.commit()
        cursor.close()
        conn.close()


insertStockData(tickers)


def getLatestDate(x):
    try:
        conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
        cursor = conn.cursor()

        selectDateQuery = ("Select eod "
                       "From " + x + " "
                       "Order By eod Desc Limit 1")

        cursor.execute(selectDateQuery)

        x = cursor.fetchone()
        lastDate = x[0]
    except:
        lastDate = None
        pass

    return(lastDate)

    cursor.close()
    conn.close()


def updateStockData(tickers):
    for x in tickers:
        conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
        cursor = conn.cursor()

        insertStockData = ("INSERT INTO " + x + " "
                           "(eod, open_price, high_price, low_price, close_price, adjclose, volume, ticker) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        try:
            # data['ticker'].count() - 2, 0, -1
            data = pd.DataFrame(si.get_data(x, start_date=getLatestDate(x), index_as_date=False))
            for y in range(data['ticker'].count()):
                print(y)
                stock_data = [data['date'].loc[y], float(data['open'].loc[y]), float(data['high'].loc[y]),
                              float(data['low'].loc[y]), float(data['close'].loc[y]), float(data['adjclose'].loc[y]),
                              float(data['volume'].loc[y]), data['ticker'].loc[y]]
                cursor.execute(insertStockData, stock_data)
                print(
                    "INSERT INTO " + x + " (eod, open_price, high_price, low_price, close_price, adjclose, volume, ticker) VALUES " + str(stock_data))


        except:
            # skipping the most recent date in stock_data table
            pass

        print("Done Inserting Data For " + x)

        conn.commit()
        cursor.close()
        conn.close()

#updateStockData(tickers)

def importUsers(users):
    conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    insertUsers = ("INSERT INTO USERS"
                      "(username, password_salt, password_hash, fname, lname, email, subscriber) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    for x in range(users['password'].count()):
        salt = int(binascii.hexlify(os.urandom(3)),16)
        print(users['password'].loc[x])
        guid = uuid.uuid4()

        sub = str2boolint(users['subscriber'].loc[x])
        print(guid)

        #names=["username", "password", "fname", "lname", "email", "subscriber"])
        user_data = [users['username'].loc[x], str(salt), encrypt_string(str(salt)+users['password'].loc[x]), users['fname'].loc[x], users['lname'].loc[x],
                     users['email'].loc[x], sub]
        cursor.execute(insertUsers, user_data)
        print("INSERT INTO USERS(variables) VALUES " + str(user_data))

    conn.commit()
    cursor.close()
    conn.close()


importUsers(users)


def importPortfolio(portfolio):
    conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    insertPortfolio = ("INSERT INTO PORTFOLIO"
                      "(portfolio_name) "
                      "VALUES (%s)")
    for x in range(portfolio['portfolio_name'].count()):

        portfolio_data = [portfolio['portfolio_name'].loc[x]]
        cursor.execute(insertPortfolio, portfolio_data)
        print("INSERT INTO PORTFOLIO(variables) VALUES " + str(portfolio_data))

    conn.commit()
    cursor.close()
    conn.close()


importPortfolio(portfolio)


def importHas_Portfolio(has_portfolio):
    conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    insertHas_Portfolio = ("INSERT INTO HAS_PORTFOLIO"
                      "(login_id , portfolio_id) "
                      "VALUES (%s, %s)")
    for x in range(has_portfolio['login_id'].count()):

        has_portfolio_data = [int(has_portfolio['login_id'].loc[x]), int(has_portfolio['portfolio_id'].loc[x])]
        cursor.execute(insertHas_Portfolio, has_portfolio_data)
        print("INSERT INTO HAS_PORTFOLIO(variables) VALUES " + str(has_portfolio_data))

    conn.commit()
    cursor.close()
    conn.close()
importHas_Portfolio(has_portfolio)

def importHas_Stock(has_stock):
   conn = sqlconnection.connect(user='root', password='', host='127.0.0.1', database='financedb')
   cursor = conn.cursor()

   insertHas_Stock = ("INSERT INTO HAS_STOCK"
                     "(portfolio_id, ticker) "
                     "VALUES (%s, %s)")
   for x in range(has_stock['portfolio_id'].count()):

       has_stock_data = [int(has_stock['portfolio_id'].loc[x]), has_stock['ticker'].loc[x]]
       cursor.execute(insertHas_Stock, has_stock_data)
       print("INSERT INTO HAS_STOCK(variables) VALUES " + str(has_stock_data))

   conn.commit()
   cursor.close()
   conn.close()
importHas_Stock(has_stock)