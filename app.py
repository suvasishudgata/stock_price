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

if __name__ == '__main__':
    app.run(debug=True)
