# SQL create satements for S&P 500 finance database
Create database financedb;
use financedb;

Create Table if not exists SP500(
	ticker varchar(5) not null,
    stock_name varchar(50) not null,
    sector varchar(50),
    Primary Key(ticker));
    #https://www.w3schools.com/sql/sql_autoincrement.asp

Create Table if not exists Portfolio(
	portfolio_id int not null auto_increment,
    portfolio_name varchar(20),
    Primary Key(portfolio_id));
    
Alter Table Portfolio auto_increment=8000001;

Create Table if not exists Users(
	login_id int not null auto_increment,
    username varchar(20) not null,
    password_salt varchar(20) not null,
    password_hash varchar(80) not null,
    fname varchar(20),
    lname varchar(20),
    email varchar(30),
    subscriber boolean,
    Primary Key(login_id, username));
    
Alter Table Users auto_increment=1000001;

Create Table if not exists has_portfolio(
    login_id int not null,
    portfolio_id int not null,
    Primary key(login_id, portfolio_id),
    Foreign key (login_id) references Users(login_id) ON DELETE CASCADE ON UPDATE CASCADE,
    Foreign key (portfolio_id) references Portfolio(portfolio_id) ON DELETE CASCADE ON UPDATE CASCADE);

Create Table if not exists has_stock(
    portfolio_id int not null,
    ticker varchar(5) not null,
    Primary key(ticker, portfolio_id),
    Foreign key (ticker) references SP500(ticker) ON DELETE CASCADE ON UPDATE CASCADE,
    Foreign key (portfolio_id) references Portfolio(portfolio_id) ON DELETE CASCADE ON UPDATE CASCADE);



