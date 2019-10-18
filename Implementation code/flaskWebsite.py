from flask import Flask, render_template
from flask import request, redirect, session, flash
import mysql_connector_python.mysql.connector as sqlconnection
from yahoo_fin import stock_info as si
import os
import binascii
import uuid
import hashlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from datetime import datetime
import datetime
import operator

app = Flask(__name__)
app.secret_key = os.urandom(12)
currentUser = ""
# creates a new website in a variable called app


def getLatestDate(x):
    try:
        conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
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



#############################################################################################################################################################################



def findBiggestPercentChange():
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()
    selectTickers = ("Select ticker "
                     "from SP500")

    cursor.execute(selectTickers)
    tickerlistparse = []

    for x in cursor:
        tickerlistparse.append(x[0])
    highlow = []
    tickerlist= []
    ndate = str(getLatestDate('GOOG'))

    for x in tickerlistparse:
        newdate = str(getLatestDate(x)).replace("-", "")

        #print(newdate)
        findQuery = ("Select ((adjclose - open_price) / open_price) * 100.0 From " + x +" Where eod = " + newdate)


        #print("Saving: ", x)
        cursor.execute(findQuery)

        y = cursor.fetchone()
        highlow.append(y)
        tickerlist.append(x)

    indexmax, valuemax = max(enumerate(highlow), key=operator.itemgetter(1))
    indexmin, valuemin = min(enumerate(highlow), key=operator.itemgetter(1))
    '''
    print(valuemax)
    print(indexmin)
    print(valuemin)

    print(tickerlist)
    print(highlow)
    '''
    valuemax = str(valuemax).replace("(", "")
    valuemax = str(valuemax).replace(")", "")
    valuemax = str(valuemax).replace(",", "")
    valuemin = str(valuemin).replace("(", "")
    valuemin = str(valuemin).replace(")", "")
    valuemin = str(valuemin).replace(",", "")
    #print("Max Percentage Change: " + str(tickerlist[indexmax]) + ": " + valuemax + "%")
    #print("Min Percentage Change: " + str(tickerlist[indexmin]) + ": " + valuemin + "%")

    findQuery = ("Select stock_name From SP500 Where ticker = '" + str(tickerlist[indexmax]) + "'")
    cursor.execute(findQuery)
    namemax = str(cursor.fetchone())
    namemax = str(namemax).replace("(", "")
    namemax = str(namemax).replace(")", "")
    namemax = str(namemax).replace(",", "")
    namemax = str(namemax).replace("'", "")

    findQuery = ("Select stock_name From SP500 Where ticker = '" + str(tickerlist[indexmin]) + "'")
    cursor.execute(findQuery)
    namemin = str(cursor.fetchone())
    namemin = str(namemin).replace("(", "")
    namemin = str(namemin).replace(")", "")
    namemin = str(namemin).replace(",", "")
    namemin = str(namemin).replace("'", "")

    pctChList = []
    line1 = "For the most current date, " + ndate  + ":"
    line2 = "Max Percentage Change: " + namemax + ": " + str(round(float(valuemax), 2)) + "%"
    line3 = "Min Percentage Change: " + namemin + ": " + str(round(float(valuemin), 2)) + "%"
    pctChList.append(line1)
    pctChList.append(line2)
    pctChList.append(line3)

    return (pctChList)


    cursor.close()
    conn.close()



################################################################################################################################################################



def mostPopularStock():
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    insertHas_Stock = ("select has_stock.ticker, stock_name, count(*) from has_stock, SP500 "
                       "where has_stock.ticker = SP500.ticker "
                       "group by has_stock.ticker "
                       "order by count(*) desc " 
                       "limit 1")


    cursor.execute(insertHas_Stock)

    x = cursor.fetchone()

    moPop =[]
    line1 = "SELECTING MOST POPULAR STOCK IN ALL PORTFOLIOS AND ITS FREQUENCY: "
    line2 = "(" + str(x[0]) + ") " + str(x[1]) + " with a count of " + str(x[2])
    moPop.append(line1)
    moPop.append(line2)
    return(moPop)

    conn.commit()
    cursor.close()
    conn.close()



############################################################################################################################################################



def percentages():
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    selectSectors = ("Select all count(ticker), sector "
                       "from SP500 "
                       "group by sector")

    cursor.execute(selectSectors)

    sectorsCounts = []
    for x in cursor:
        sectorsCounts.append([x[0], x[1], 0])

    selectTickers = ("Select ticker "
                     "from SP500")

    cursor.execute(selectTickers)
    currentTickers = []

    for x in cursor:
        currentTickers.append(x[0])

    sumCap = 0
    for x in currentTickers:
        newdate = str(getLatestDate(x)).replace("-", "")

        selectStocks = ("Select sector, close_price*volume "
                     "from " + x + ", SP500 "
                     "where SP500.ticker = " + x + ".ticker and eod = " + newdate)
        cursor.execute(selectStocks)
        y = cursor.fetchone()
        if y[0] == sectorsCounts[0][1]:
            sectorsCounts[0][2] = sectorsCounts[0][2] + y[1]
        elif y[0] == sectorsCounts[1][1]:
            sectorsCounts[1][2] = sectorsCounts[1][2] + y[1]
        elif y[0] == sectorsCounts[2][1]:
            sectorsCounts[2][2] = sectorsCounts[2][2] + y[1]
        elif y[0] == sectorsCounts[3][1]:
            sectorsCounts[3][2] = sectorsCounts[3][2] + y[1]
        elif y[0] == sectorsCounts[4][1]:
            sectorsCounts[4][2] = sectorsCounts[4][2] + y[1]
        elif y[0] == sectorsCounts[5][1]:
            sectorsCounts[5][2] = sectorsCounts[5][2] + y[1]
        elif y[0] == sectorsCounts[6][1]:
            sectorsCounts[6][2] = sectorsCounts[6][2] + y[1]
        elif y[0] == sectorsCounts[7][1]:
            sectorsCounts[7][2] = sectorsCounts[7][2] + y[1]
        elif y[0] == sectorsCounts[8][1]:
            sectorsCounts[8][2] = sectorsCounts[8][2] + y[1]
        elif y[0] == sectorsCounts[9][1]:
            sectorsCounts[9][2] = sectorsCounts[9][2] + y[1]
        elif y[0] == sectorsCounts[10][1]:
            sectorsCounts[10][2] = sectorsCounts[10][2] + y[1]

        sumCap = sumCap + y[1]
    sectorList = []
    print(sectorsCounts)
    returnstr = "~Current Market Cap for S&P500: " + str(sumCap)
    sectorList.append(returnstr)
    for x in sectorsCounts:
        sectorList.append("Sector: " + str(x[1]) + "     Companies in Sector: " + str(x[0]) +
                     "     Sector Market Cap: " + str(round(x[2], 2)) + "     " 
                    "Market Share Percentage: "+ str(round(((x[2]/sumCap)*100), 1)) + "%")

    return(sectorList)
    cursor.close()
    conn.close()



#################################################################################################################################################################



def seeUsersPortfoliosStocks():
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()
    selectQuery = ("Select username, portfolio_name, stock_name "
                     "From Users, has_portfolio, portfolio, has_stock, SP500 "
                     "where Users.login_id = has_portfolio.login_id and has_portfolio.portfolio_id = "
                     "portfolio.portfolio_id and portfolio.portfolio_id = has_stock.portfolio_id and "
                     "has_stock.ticker = SP500.ticker "
                     "Order By username")
    cursor.execute(selectQuery)
    records = cursor.fetchall()

    user = []
    port = []
    ticker = []
    for row in records:
        user.append(row[0])
        port.append(row[1])
        ticker.append(row[2])

    return([user, port, ticker]) # returns columns for a table
    cursor.close()
    conn.close()



#################################################################################################################################################################



@app.route('/funData', methods=['POST'])
def funData():
    pct_changes = findBiggestPercentChange()
    mostPop = mostPopularStock()
    marketShares = percentages()
    lenMS = len(marketShares)

    return render_template('funData.html', pct_changes=pct_changes, mostPop=mostPop, marketShares=marketShares, lenMS=lenMS)



@app.route('/userData', methods=['POST'])
def userData():
    portfolioData = seeUsersPortfoliosStocks()  # returns columns for a table
    length = len(portfolioData[0])
    return render_template('userData.html', portfolioData=portfolioData, length=length)



##############################################################################################################################################################



@app.route('/delPort', methods=['POST'])
def delPort():
    try:
        portfolio_name = request.form['name']

        conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb', autocommit=True)
        cursor = conn.cursor()

        deletePortfolio = ("DELETE FROM portfolio WHERE portfolio_name = '" + portfolio_name + "'")

        cursor.execute(deletePortfolio)
        print(deletePortfolio)

        index = None
        ports = session['portfolio_name']
        for x in range(len(ports)):
            if ports[x] ==  portfolio_name:
                index = x
                break

        portfolio_id = session['portfolio_id'][index]

        idslist = session['portfolio_id']
        namelist = session['portfolio_name']

        idslist.remove(portfolio_id)
        namelist.remove(portfolio_name)

        session['portfolio_id'] = idslist
        session['portfolio_name'] = namelist

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('viewAcc.html')
    except:
        flash(u'Portfolio does not exist -- Cannot delete', 'delete')
        return render_template('viewAcc.html')




######################################################################################################################################################



@app.route('/createPort', methods=['POST'])
def createPort():
    portfolio_name = request.form['name']
    loginid = session['user_id']

    if (portfolio_name in session['portfolio_name']):
        flash(u'Portfolio name already exists -- Cannot create portfolio', 'create')
        return render_template('viewAcc.html')


    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb', autocommit=True)
    cursor = conn.cursor()

    selectPortfolioid = ("SELECT Max(portfolio_id) + 1 "
                         "FROM portfolio")

    cursor.execute(selectPortfolioid)

    for x in cursor:
        portfolio_id = x[0]

    insertPortfolio = ("INSERT INTO portfolio " 
                       "(portfolio_id, portfolio_name) "
                       "VALUES (%s, %s)")

    insertData = [portfolio_id, portfolio_name]

    cursor.execute(insertPortfolio, insertData)

    insertStatement = "INSERT INTO portfolio (portfolio_id, portfolio_name) VALUES " + "(" + str(portfolio_id) + ", " + str(portfolio_name) + ")"
    print(insertStatement)

    inserthasPortfolio = ("INSERT INTO has_portfolio "
                       "(login_id, portfolio_id) "
                       "VALUES (%s, %s)")
    insertData = [loginid, portfolio_id]

    cursor.execute(inserthasPortfolio, insertData)
    insertStatement = "INSERT INTO has_portfolio (login_id, portfolio_id) VALUES " + str(insertData)
    print(insertStatement)

    idslist = session['portfolio_id']
    namelist = session['portfolio_name']

    idslist.append(portfolio_id)
    namelist.append(portfolio_name)

    session['portfolio_id'] = idslist
    session['portfolio_name'] = namelist


    conn.commit()
    cursor.close()
    conn.close()

    return render_template('viewAcc.html')



##################################################################################################################################################



@app.route('/delStock', methods=['POST'])
def delStock():
    session['currentStock'] = request.form['ticker']
    ticker = session['currentStock']
    portid = session['currentPortid']

    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    selectTickerQuery = ("Select ticker "
                         "From has_stock "
                         "Where portfolio_id = " + str(portid))
    cursor.execute(selectTickerQuery)

    tickers = []
    for x in cursor:
        tickers.append(x[0])

    if ticker not in tickers:
        flash(u'Stock is not in Portfolio -- Cannot delete', 'deleteStock')
    else:
        deleteStock = "DELETE FROM has_stock WHERE portfolio_id = " + str(portid) + " and ticker = " + "'" + str(ticker) + "'"
        cursor.execute(deleteStock)
        print(deleteStock)
        tickers.remove(ticker)

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('viewPort.html', tickers=tickers)



################################################################################################################################################



@app.route('/addStock', methods=['POST'])
def addStock():
    try:
        session['currentStock'] = request.form['ticker']
        ticker = session['currentStock']
        portid = session['currentPortid']

        conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
        cursor = conn.cursor()

        insertStock = ("INSERT INTO has_stock "
                           "(portfolio_id, ticker) "
                           "VALUES (%s, %s)")

        insertData = [int(portid), ticker]
        cursor.execute(insertStock, insertData)
        insertStatement = "INSERT INTO has_stock (portfolio_id, ticker) VALUES " + str(insertData)
        print(insertStatement)

        selectTickerQuery = ("Select ticker "
                             "From has_stock "
                             "Where portfolio_id = " + str(portid))
        cursor.execute(selectTickerQuery)

        tickers = []
        for x in cursor:
            tickers.append(x[0])

        conn.commit()
        cursor.close()
        conn.close()

        return render_template('viewPort.html', tickers=tickers)
    except:
        portid = session['currentPortid']
        conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
        cursor = conn.cursor()

        selectTickerQuery = ("Select ticker "
                             "From has_stock "
                             "Where portfolio_id = " + str(portid))
        cursor.execute(selectTickerQuery)

        tickers = []
        for x in cursor:
            tickers.append(x[0])

        conn.commit()
        cursor.close()
        conn.close()

        flash(u'Ticker does not exist in Database or it is already in your portfoliod', 'addStock')

        return render_template('viewPort.html', tickers=tickers)




##########################################################################################################################################################



@app.route('/updateSub', methods=['POST'])
def updateSubscription():
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    if session['subscriber'] == 1:

        updateQuery = ("UPDATE users "
                       "SET subscriber = 0 "
                       "WHERE login_id = '" + str(session['user_id']) + "'")
        cursor.execute(updateQuery)
        print(updateQuery)
        session['subscriber'] = 0

    else:
        updateQuery = ("UPDATE users "
                       "SET subscriber = 1 "
                       "WHERE login_id = '" + str(session['user_id']) + "'")
        cursor.execute(updateQuery)
        print(updateQuery)
        session['subscriber'] = 1
        flash(u'Thank you for subscribing!!', 'sub')

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('viewAcc.html')



###########################################################################################################################################################



@app.route('/deleteAcc', methods=['POST'])
def deleteAcc():
    login_id = session['user_id']

    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb', autocommit=True)
    cursor = conn.cursor()

    # find portfolios of user to delete before removing account

    portfolio_ids = session['portfolio_id']
    count = 0
    for x in portfolio_ids:
        deletePortfolios = ("DELETE FROM portfolio WHERE portfolio_id = " + str(x))
        cursor.execute(deletePortfolios)
        print("Deleting Portfolio: " + session['portfolio_name'][count])
        count += 1


    deleteAccount = ("DELETE FROM users WHERE login_id = " + str(login_id))

    cursor.execute(deleteAccount)
    print("Deleting Account: " + session['username'])

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('logout2')



######################################################################################################################################################33##



@app.route('/viewAcc.html', methods=['POST']) # for choosing the stock
def viewAcc():
    portfolios = session['portfolio_name']
    empty = []
    if(portfolios == empty):
        flash(u'First, create a portfolio', 'createPort')
    return render_template('viewAcc.html')

@app.route('/viewPort', methods=['POST'])
def viewPort():
    port = request.form['portfolio']

    count = 0
    for x in session['portfolio_name']:
        if x == port:
            break
        count += 1

    portid = session['portfolio_id'][count]
    session['currentPortid'] = portid

    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    selectTickerQuery = ("Select ticker "
                       "From has_stock "
                       "Where portfolio_id = " + str(portid))
    cursor.execute(selectTickerQuery)

    tickers = []
    for x in cursor:
        tickers.append(x[0])

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('viewPort.html', tickers=tickers)


@app.route('/actionDet', methods=['POST']) # for choosing the stock
def actionDet():
    session['currentStock'] = request.form['stock']
    action = request.form['action']

    if action == "display":
        return setViewTickerPort()
    elif action == "pred":
        return setPredTickerPort()
    elif action == "rec":
        return setRecTickerPort()
    else:
        return mainPage()




######################################################################################################################################################################################


@app.route('/sendDisplay', methods=['POST'])
def sendDisplay():
    return render_template('viewStock.html')

@app.route('/sendPred', methods=['POST'])
def sendPred():
    return render_template('viewPred.html')

@app.route('/sendRec', methods=['POST'])
def sendRed():
    return render_template('viewRec.html')

@app.route('/sendSignup', methods=['POST'])
def sendSignup():
    return render_template('signup.html')



#############################################################################################################################################################################################




@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return mainPage()

@app.route('/logout2')
def logout2():
    session.clear()
    return mainPage()



############################################################################################################################################################################################



@app.route('/signin.html')
def signIn():
    return render_template('signin.html')

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    selectUsers = ("SELECT username "
                   "FROM users ")

    cursor.execute(selectUsers)

    users = []
    for x in cursor:
        users.append(x)

    usernameExist = False
    for x in users:
        if(username == x[0]):
            usernameExist = True

    if usernameExist == False:
        flash('Username does not exist')
        return mainPage()

    selectDateQuery = ("Select password_salt "
                       "From users "
                       "Where username = " + "'" + username + "'")
    cursor.execute(selectDateQuery)

    for x in cursor:
        salt = x[0]

    hash = encrypt_string(str(salt) + request.form['password'])

    selectDateQuery = ("Select login_id, password_hash, fname, subscriber, username "
                       "From users "
                       "Where username = " + "'" + username + "'")
    cursor.execute(selectDateQuery)

    for x in cursor:
        currentUser = x[0]
        pass_hash = x[1]
        fname = x[2]
        subscriber = x[3]
        username = x[4]

    selectDateQuery = ("Select Portfolio.portfolio_id, portfolio_name "
                       "From has_portfolio, portfolio "
                       "Where has_portfolio.portfolio_id = portfolio.portfolio_id and has_portfolio.login_id = " + str(currentUser))
    cursor.execute(selectDateQuery)

    portids = []
    portNames = []
    for x in cursor:
        portids.append(x[0])
        portNames.append(x[1])


    if(hash == pass_hash):
        session['logged_in'] = True
        session['user_id'] = currentUser
        session['fname'] = fname
        session['subscriber'] = subscriber
        session['username'] = username
        session['portfolio_id'] = portids
        session['portfolio_name'] = portNames

    else:
        flash('Wrong Password')
    return mainPage()



##############################################################################################################################################################


# create view recommendation page
@app.route('/viewRec.html') # for choosing the stock
def chooseRecPage():
    return render_template('viewRec.html')

@app.route('/getRecDataPort', methods = ['POST'])
def setRecTickerPort():
    if(session['subscriber'] == 0):
        portid = session['currentPortid']
        conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
        cursor = conn.cursor()
        selectTickerQuery = ("Select ticker "
                             "From has_stock "
                             "Where portfolio_id = " + str(portid))
        cursor.execute(selectTickerQuery)

        tickers = []
        for x in cursor:
            tickers.append(x[0])

        conn.commit()
        cursor.close()
        conn.close()

        flash(u'You must be a subscriber to view a trading strategy', 'subs')
        return render_template('viewPort.html', tickers=tickers)

    ticker = session['currentStock']
    return getRecData(ticker)
@app.route('/getRecData', methods = ['POST'])
def setRecTickerReg():
    if (session['subscriber'] == 0):
        flash(u'You must be a subscriber to view a trading strategy', 'subscribe')
        return render_template('viewRec.html')


    ticker = request.form['ticker']
    return getRecData(ticker)

def getRecData(ticker):
    style.use('ggplot')
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    selectDateQuery = ("Select * "
                       "From " + ticker)

    cursor.execute(selectDateQuery)

    df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume', 'ticker'])
    count = 0
    for x in cursor:
        df.loc[count] = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]]
        count += 1

    cursor.close()
    conn.close()

    data = df.set_index('date')

    # Initialize the short and long windows
    short_window = 40
    long_window = 100

    # Initialize the `signals` DataFrame with the `signal` column
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    # Create short simple moving average over the short window
    signals['short_mavg'] = data['adjclose'].rolling(window=short_window, min_periods=1, center=False).mean()

    # Create long simple moving average over the long window
    signals['long_mavg'] = data['adjclose'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Create signals
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    # Generate trading orders
    signals['positions'] = signals['signal'].diff()

    # Print `signals`
    # print(signals)

    fig = plt.figure()
    ax1 = fig.add_subplot(111, ylabel='Price in $')  # Add a subplot and label for y-axis
    data['adjclose'].plot(ax=ax1, color='r', lw=2.)  # Plot the closing price
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)  # Plot the short and long moving averages
    ax1.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0], '^',
             markersize=10, color='m')  # Plot the buy signals
    ax1.plot(signals.loc[signals.positions == -1.0].index, signals.short_mavg[signals.positions == -1.0], 'v',
             markersize=10, color='k')  # Plot the sell signals
    plt.title('Trading Strategy for ' + ticker)
    fig.savefig('C:/Users/wrenp/PycharmProjects/FlaskPractice/static/displayRecFigure.png')

    return redirect('/viewRec2.html')

@app.route('/viewRec2.html')  # for displaying the chosen stock
def viewRec2():
    return redirect('/static/displayRecFigure.png')



############################################################################################################################################################################



# create view prediction page
@app.route('/viewPred.html') # for choosing the stock
def choosePredPage():
    return render_template('viewPred.html')

@app.route('/getPredDataPort', methods = ['POST'])
def setPredTickerPort():
    ticker = session['currentStock']
    return getPredData(ticker)

@app.route('/getPredData', methods = ['POST'])
def setPredTickerReg():
    ticker = request.form['ticker']
    return getPredData(ticker)

def getPredData(ticker):
    style.use('ggplot')
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    selectDateQuery = ("Select * "
                       "From " + ticker)

    cursor.execute(selectDateQuery)

    df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume', 'ticker'])
    count = 0
    for x in cursor:
        df.loc[count] = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]]
        count += 1

    cursor.close()
    conn.close()

    data = df[['adjclose']]

    bp = int(data.shape[0] - 31)

    train = data[:bp]
    valid = data[bp:]
    # splitting into train and validation (change valid to be length=50)

    # find average percent change over the last week of train
    Mdata = df[['adjclose', 'open']]
    Mtrain = Mdata[bp - 7:bp]
    close = np.array(Mtrain['adjclose'])
    open = np.array(Mtrain['open'])
    pct_C = []
    for i in range(len(close)):
        pct_change = (close[i] - open[i]) / open[i]
        pct_C.append(pct_change)
    # df['PCT_change'] = (df['adjclose'] - df['open']) / df['open'] * 100.0
    avg_pct_C = sum(pct_C) / len(pct_C)  # multiplying by 10 to give multiplier more weight
    multiplier = 1 + avg_pct_C

    pred = []
    for i in range(0, valid.shape[0]):
        a = (train['adjclose'][len(train) - valid.shape[0] + i:].sum() + sum(
            pred))  # * multiplier # multiplying by stock trend within the last week
        b = a / valid.shape[0] * multiplier
        pred.append(b)
    # make predictions

    lastTrain = train['adjclose'].iloc[-1]
    firstPred = pred[:1]
    dif = lastTrain - firstPred
    pred = [x + dif for x in pred]

    valid.insert(loc=0, column='Predictions', value=pred)

    xupper = data.shape[0] + 10
    xlower = data.shape[0] - 175
    closeArr = np.array(data['adjclose'])
    yupper = 0
    for x in closeArr[xlower:]:
        if (x > yupper):
            yupper = x
    ylower = 1000000
    for x in closeArr[xlower:]:
        if (x < ylower):
            ylower = x
    ylower = ylower - 15

    fig = plt.figure()
    plt.plot(train['adjclose'])
    # plt.plot(valid[['adjclose', 'Predictions']]) # to print real values and predicted values
    plt.plot(valid[['Predictions']])
    plt.title(ticker + ' Forecast')
    plt.xlim(xlower, xupper)
    plt.ylim(ylower, yupper)
    fig.savefig('C:/Users/wrenp/PycharmProjects/FlaskPractice/static/displayPredFigure.png')  # to save picture of plot

    return redirect('/viewPred2.html')

@app.route('/viewPred2.html')  # for displaying the chosen stock
def viewPred2():
    return redirect('/static/displayPredFigure.png')



############################################################################################################################################################################



# create view stock data page
@app.route('/viewStock.html') # for choosing the stock
def chooseStockPage():
    return render_template('viewStock.html')

@app.route('/getStockDataPort', methods = ['POST'])
def setViewTickerPort():
    ticker = session['currentStock']
    sdate = ""
    edate = ""
    return getStockData(ticker, sdate, edate)

@app.route('/getStockData', methods = ['POST'])
def setViewTickerReg():
    ticker = request.form['ticker']
    syear = request.form['syear']
    smonth = request.form['smonth']
    sday = request.form['sday']
    eyear = request.form['eyear']
    emonth = request.form['emonth']
    eday = request.form['eday']
    sdate = syear + smonth + sday
    edate = eyear + emonth + eday
    return getStockData(ticker, sdate, edate)

def getStockData(ticker, sdate, edate):
    style.use('ggplot')

    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    if(sdate == "" and edate == ""):
        selectDateQuery = ("Select * "
                           "From " + ticker)
    elif(sdate != "" and edate == ""):
        selectDateQuery = ("Select * "
                           "From " + ticker + " "
                           "Where eod > " + sdate)
    elif (sdate == "" and edate != ""):
        selectDateQuery = ("Select * "
                           "From " + ticker + " "
                           "Where eod < " + edate)
    elif (sdate != "" and edate != ""):
        selectDateQuery = ("Select * "
                           "From " + ticker + " "
                           "Where eod > " + sdate + " and eod < " + edate)


    cursor.execute(selectDateQuery)

    data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'adjclose', 'volume', 'ticker'])
    count = 0
    for x in cursor:
        data.loc[count] = [x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]]
        count += 1
    cursor.close()
    conn.close()

    data = data.set_index('date')
    data = data[['adjclose']]

    fig = plt.figure()
    plt.plot(data['adjclose'])
    plt.legend(loc=4)
    plt.title(ticker)
    plt.xlabel('Date')
    plt.ylabel('Price')
    fig.savefig('C:/Users/wrenp/PycharmProjects/FlaskPractice/static/displayFigure.png') # to save picture of plot

    return redirect('/viewStock2.html')

@app.route('/viewStock2.html')  # for displaying the chosen stock
def viewStock2():
    return redirect('/static/displayFigure.png')



############################################################################################################################################################################



# sign up page
@app.route('/signup.html')
def signupPage():
    return render_template('signup.html')

userslist = []
@app.route('/signup', methods = ['POST'])
def signup():
    # assign form inputs to variables - then insert values into sql
    username = request.form['username']
    userslist.append(username)
    print(userslist)
    # ^ for checking that all users are being recorded ^
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    try:
        subscriber = request.form['subscriber']
        subscriber = 1
    except:
        subscriber = 0
    insertUser(username, password, fname, lname, email, subscriber)
    return redirect('/')

def insertUser(username, password, fname, lname, email, subscriber):
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    insertUsers = ("INSERT INTO USERS"
                      "(username, password_salt, password_hash, fname, lname, email, subscriber) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)")

    salt = int(binascii.hexlify(os.urandom(3)), 16)
    guid = uuid.uuid4()

    # names=["username", "password", "fname", "lname", "email", "subscriber"])
    user_data = [username, str(salt), encrypt_string(str(salt) + password),
                 fname, lname, email, subscriber]

    cursor.execute(insertUsers, user_data)
    print("INSERT INTO USERS(variables) VALUES " + str(user_data))

    conn.commit()
    cursor.close()
    conn.close()



############################################################################################################################################################################


'''
# for displaying users
@app.route('/users.html')
def users():
    return render_template('users.html', userslist=userslist)
'''



######################################################################################################################################################################



def updateStockData():
    conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
    cursor = conn.cursor()

    selectTickers = ("SELECT ticker "
                     "FROM SP500")
    cursor.execute(selectTickers)

    tickers = []
    for x in cursor:
        tickers.append(x[0])

    conn.commit()
    cursor.close()
    conn.close()

    for x in tickers:
        conn = sqlconnection.connect(user='root', password='redblanket', host='127.0.0.1', database='financedb')
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



##########################################################################################################################################################################

@app.route('/return', methods=['POST'])
def home():
    if not session.get('logged_in'):
        return render_template('signin.html')
    else:
        if session['subscriber']==1:
            subs = "subscriber"
        else:
            subs = "non-subscriber"
        return render_template('index.html', sub=subs)


@app.route('/')
def mainPage():
    if not session.get('logged_in'):
        return render_template('signin.html')
    else:
        if session['subscriber']==1:
            subs = "subscriber"
        else:
            subs = "non-subscriber"
        return render_template('index.html', sub=subs)
# if the browser requests the address with / then the function mainPage is run and sent to the browser


if __name__ == '__main__':
    weekno = datetime.datetime.today().weekday()
    if weekno < 5:
        latestDate = getLatestDate('MSFT').strftime('%Y-%m-%d')
        currentDate = datetime.today().strftime('%Y-%m-%d')
        if (latestDate != currentDate):
            updateStockData()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run(debug=True)

# if this script is run directly then start the application

