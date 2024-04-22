import functools

import yfinance as yf

import plotly.express as px
from plotly.graph_objs import Scatter

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from src.db import get_db

bp = Blueprint('finance', __name__)
ticker = ""

@bp.route('/saved', methods=('GET', 'POST' ) )
def save():
    print("TEST TEST TEST TEST TEST")
    if( g.user ):          
        ticker = request.form['ticker']
        print("TICKER: " + ticker)
        stockInfo = yf.Ticker(ticker)

        exception = False
        try:
            print(stockInfo.fast_info.previous_close)
            prices = stockInfo.history(interval='1d', period='1d')['Close']
            if prices.empty:
                raise Exception

        except Exception as e:
            print("EEEEEEEEEEEEEEEEEEEEXXXXXXXXXXXXXCCCCCCCCEEEEEEEEEEEEEEEEPPPPPPPPPPTTT")
            print(e)
            exception = True

        if not exception:
            db = get_db()
            if db is None: 
                print("db is none")

            db.execute(
                "INSERT INTO stock ( user_id, ticker ) VALUES (?, ?)",
                (g.user['id'], ticker),
            )
            
            db.commit()

            stocks = db.execute(
                "SELECT * FROM stock"
            ).fetchall()

            for stock in stocks:
                print( stock['ticker'])
            

    return ('', 204)


@bp.route('/<ticker2>', methods=('GET', 'POST'))
@bp.route('/',  methods=('GET', 'POST'))
def getTicker(ticker2=None):


    if request.method == 'POST' or ticker2 is not None:
        global ticker

        if ticker2 is None:
            ticker = request.form['ticker']

        else:
            ticker = ticker2

        print("TICKER: " + ticker)
        
        if "Get Ticker" in request.form:
            
            
            try:
                stockInfo = yf.Ticker(ticker)
                print("Still executing even though exception occurred!!!!!!!!!!!!!!!!!!!!")
            except Exception as e:
                print(e)

        elif ticker2 is not None:
            ticker = ticker2

            try:
                stockInfo = yf.Ticker(ticker)
            except Exception as e:
                print(e)

        print('case 3')
        try:
            stockInfo = yf.Ticker(ticker)

            print(stockInfo.fast_info.previous_close)

            
            period_len = getLength(request.form) or '1d'
            time_span = getTime(request.form) or '1 day'

            
            
            
            return render_template('getTicker.html', stockInfo = stockInfo, period_len = period_len, time_span = time_span, getFig = getFig)
        
        except Exception as e:
            print(e)
            
        
        

    return render_template('getTicker.html')


@bp.route('/savedStocks', methods=('GET', 'POST'))
def savedStocks():
    if request.method == 'GET':
        print("click")
        try:
            print('case 2')
            if( g.user ):
                db = get_db()

                stocks = db.execute(
                    "SELECT * FROM stock WHERE user_id = ?",
                    ( g.user['id'], )
                ).fetchall()

                tickers = []

                for stock in stocks:
                    tickers.append( stock['ticker'] )
           


        except Exception as e:
                print(e)


    return render_template('savedStocks.html', tickers = tickers, getName = getName)

def getFig(stockInfo, period_len, time_span ):

    time_interval = getInterval( period_len )

    prices = stockInfo.history(interval=time_interval, period=period_len)['Close']
    dates = stockInfo.history(interval=time_interval, period=period_len).index

    
    
    plot_1yr = px.line(  x = dates, y = prices, title = time_span + ' Stock Price History', width = 1000, height = 750 )

    plot_1yr.update_layout( xaxis_title = "Date/Time", yaxis_title = "Price ($)", font_family="Helvetica" )

    fig = plot_1yr.to_html()

    return fig

def getName(stockInfo):
    try:
        return stockInfo.info["longName"]
    except Exception as e:
        return


def getInterval(period):
    if period == '1d':
        return '15m'
    elif period == '1y' or period == '5y' or period == 'max':
        return '1d'
    else:
        return '1h'

def getLength(form):

    if "Get Ticker" in form:
        return '1y'
    elif "1 year" in form:
        return '1y'
    elif "1 week" in form:
        return '5d'
    elif "5 years" in form:
        return '5y'
    elif "1 day" in form:
        return '1d'
    elif "1 month" in form:
        return '1mo'
    elif "All Time" in form:
        return 'max'
        
def getTime(form):

    if "Get Ticker" in form:
        return '1 Year'
    elif "1 year" in form:
        return '1 Year'
    elif "1 week" in form:
        return '1 week'
    elif "5 years" in form:
        return '5 year'
    elif "1 day" in form:
        return '1 day'
    elif "1 month" in form:
        return '1 month'
    elif "All Time" in form:
        return 'All Time'
    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else: 
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()