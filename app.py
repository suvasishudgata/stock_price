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

@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    stock_name = data['stock_name'].strip().upper()
    stock_name_full = f"{stock_name}.NS"
    # Check if stock exists
    stock_info = backend.fetch_stock_data(stock_name_full)
    if stock_info['stock_price'] is None:
        return jsonify({"success": False, "message": "Stock does not exist in NSE"})
    
    # Append the stock name to the stock.txt file
    file_path = r"C:\Users\suvasish\python-bot\stock.txt"
    with open(file_path, 'a') as file:
        file.write(f"{stock_name_full}\n")
    return jsonify({"success": True, "message": f"{stock_name_full} added successfully!"})

@app.route('/get_stock_alerts')
def get_stock_alerts():
    file_path = r"C:\Users\suvasish\python-bot\stock.txt"
    stocks = backend.stock_list(file_path)
    alerts = []
    for stock in stocks:
        stock_info = backend.fetch_stock_data(stock)
        if stock_info['avg_price_1y'] and stock_info['stock_price'] < stock_info['avg_price_1y']:
            alerts.append(stock_info)
    return jsonify(alerts)

if __name__ == '__main__':
    app.run(debug=True)
