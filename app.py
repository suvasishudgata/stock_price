# app.py
from flask import Flask, render_template, jsonify, request
import backend  # Import your backend module

app = Flask(__name__)

@app.route('/')
def index():
    # Read the stock list from the file
    file_path = r"C:\Users\suvasish\python-bot\stock.txt"
    with open(file_path, 'r') as file:
        stocks = file.read().splitlines()
    return render_template('index.html', stocks=stocks)

@app.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    data = request.get_json()
    stock = data['stock']
    stock_info = backend.fetch_stock_data(stock)  # Use function from backend module
    return jsonify(stock_info)

@app.route('/get_stock_alerts', methods=['GET'])
def get_stock_alerts():
    file_path = r"C:\Users\suvasish\python-bot\stock.txt"
    stocks = backend.stock_list(file_path)
    alerts = []

    for stock in stocks:
        stock_data = backend.fetch_stock_data(stock)
        stock_price = stock_data["stock_price"]
        avg_price_1y = stock_data["avg_price_1y"]

        if avg_price_1y and stock_price and avg_price_1y > stock_price:
            alerts.append({
                "stock_name": stock,
                "stock_price": stock_price,
                "avg_price_1y": avg_price_1y
            })

    return jsonify(alerts)

if __name__ == '__main__':
    app.run(debug=True)
