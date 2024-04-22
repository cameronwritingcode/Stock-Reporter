import yfinance as yf

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('finance', __name__)

@bp.route('/')
def getTicker():

    """
    if request.method == 'POST':
        ticker = request.form['ticker']

        try:
            stockInfo = yf.Ticker(ticker)


        except Exception as e:
            print(e)
    """
    

    return render_template('info/getTicker.html', ticker=ticker)