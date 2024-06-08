import yfinance as yf
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    # Email configurations
    sender_email = "suvasishudgata14@gmail.com"
    receiver_email = "udgatasuvasish14@gmail.com"
    password = ""

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Create SMTP session for sending the mail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def fetch_stock_data(stock):
    """Fetch stock data for a given stock."""
    stock_data = yf.Ticker(stock)
    hist = stock_data.history(period="1d")
    avg_hist = stock_data.history(period="1y")

    if not hist.empty and not avg_hist.empty:
        last_row = hist.iloc[-1]
        avg_price_1y = avg_hist['Close'].mean()
        stock_price = last_row['Close']
        last_update = last_row.name.to_pydatetime().strftime('%Y-%m-%d %H:%M:%S')
    else:
        stock_price = None
        last_update = None
        avg_price_1y = None

    return {
        "stock_name": stock,
        "stock_price": stock_price,
        "last_update": last_update,
        "avg_price_1y": avg_price_1y
    }

def stock_list(file_path):
    """Read the stock list from a file."""
    with open(file_path, 'r') as file:
        stocks = file.read().splitlines()
    return stocks

def main():
    # Path to the file containing stock list
    file_path = r"C:\Users\suvasish\python-bot\stock.txt"
    
    # Read the stock from the file
    stocks = stock_list(file_path)
    
    # Iterate over each stock and fetch the stock data
    for stock in stocks:
        stock_data = fetch_stock_data(stock)

        stock_price = stock_data["stock_price"]
        avg_price_1y = stock_data["avg_price_1y"]

        if avg_price_1y and stock_price and avg_price_1y > stock_price:
            subject = "ALERT!! The price of this stock is less than the 1 year avg"
            body = f"ALERT!! The price of this stock is less than the 1 year avg {stock}: {stock_price}: avg stock price : {avg_price_1y}"
            send_email(subject, body)
            print(f"ALERT!! The price of this stock is less than the 1 year avg {stock}: {stock_price}: avg stock price : {avg_price_1y}")

if __name__ == "__main__":
    main()
