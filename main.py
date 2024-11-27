from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
import json
from flask_socketio import SocketIO
import time
import threading

load_dotenv()
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

DEBUG = False

def debug(output):
    if DEBUG:
        print(output)

app = Flask(__name__)
socketio = SocketIO(app)

current_ticker = {'ticker': None, 'stop': False}  # Shared state
bg_task = None

def get_price(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}"
    headers = {"X-Finnhub-Token": os.getenv('FINNHUB_API_KEY')}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['c']

def get_data(symbol):
    url = f"https://finnhub.io/api/v1/stock/metric?metric=all&symbol={symbol}"
    headers = {"X-Finnhub-Token": os.getenv('FINNHUB_API_KEY')}
    response = requests.get(url, headers=headers)
    return response.json()

@socketio.on('connect')
def handle_connect():
    debug("Client connected")
    global current_ticker, bg_task
    if current_ticker['ticker']:
        if bg_task is None or not bg_task.is_alive():
            bg_task = socketio.start_background_task(send_price_updates)

@socketio.on('disconnect')
def handle_disconnect():    
    debug("Client disconnected")
    global current_ticker, bg_task
    current_ticker['stop'] = True  # Signal the task to stop
    if bg_task and bg_task.is_alive():
        bg_task.join()
    bg_task = None
    current_ticker['stop'] = False

def send_price_updates():
    while not current_ticker['stop']:
        if current_ticker['ticker']:
            price = get_price(current_ticker['ticker'])
            socketio.emit('price_update', {'ticker': current_ticker['ticker'], 'price': price})
            debug(f"Sent price update for {current_ticker['ticker']}")
        time.sleep(4)  # Adjust frequency as needed

@app.route('/', methods=['GET'])
def index():
    return """
    <html>
        <head>
            <title>Stock Data App</title>
        </head>
        <body>
            <h1>Stock Data App</h1>
            <p>Go to <a href="/AAPL">AAPL</a> for example</p>
        </body>
    </html>
    """

@app.route('/<string:ticker>', methods=['GET'])
def get_metrics_table(ticker):
    global current_ticker
    current_ticker['ticker'] = ticker
    current_ticker['stop'] = False

    data = get_data(ticker)
    data = {
        "ticker": ticker.upper(),
        "marketCap": f"${data['metric']['marketCapitalization']:,.0f}M" if data['metric']['marketCapitalization'] else "N/A",
        "peRatio": f"{data['metric']['peAnnual']:.3f}" if data['metric']['peAnnual'] else "N/A",
        "dividendYield": f"{data['metric']['currentDividendYieldTTM']:.3f}" if data['metric']['currentDividendYieldTTM'] else "N/A",
        "ebitda": f"${data['metric']['ebitdPerShareAnnual']:,.3f}" if data['metric']['ebitdPerShareAnnual'] else "N/A",
        "revenue": f"${data['metric']['revenuePerShareAnnual']:,.3f}" if data['metric']['revenuePerShareAnnual'] else "N/A",
        "netIncome": f"${data['metric']['netIncomeEmployeeAnnual']:,.3f}M" if data['metric']['netIncomeEmployeeAnnual'] else "N/A",
        "debtToEquity": f"{data['metric']['totalDebt/totalEquityAnnual']:.3f}" if data['metric']['totalDebt/totalEquityAnnual'] else "N/A",
        "profitMargin": f"{data['metric']['netProfitMarginAnnual']:.2f}%" if data['metric']['netProfitMarginAnnual'] else "N/A",
    }
    return render_template('table.html', data=data)


if __name__ == '__main__':
    DEBUG = True
    socketio.run(app, debug=True)