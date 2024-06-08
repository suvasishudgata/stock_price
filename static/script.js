document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('check-price-btn').addEventListener('click', fetchStockInfo);
    document.getElementById('add-stock-btn').addEventListener('click', addNewStock);
    fetchStockAlerts(); // Fetch stock alerts on page load
});

function fetchStockInfo() {
    const selectedStock = document.getElementById('stock-dropdown').value;
    fetch('/get_stock_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ stock: selectedStock })
    })
    .then(response => response.json())
    .then(data => {
        const stockInfoContainer = document.getElementById('stock-info');
        stockInfoContainer.innerHTML = `
            <p><strong>Stock Name:</strong> ${data.stock_name}</p>
            <p><strong>Last Update:</strong> ${data.last_update}</p>
            <p><strong>Stock Price:</strong> ${data.stock_price}</p>
            <p><strong>1 Year Avg Price:</strong> ${data.avg_price_1y}</p>
        `;
    })
    .catch(error => console.log(error));
}

function fetchStockAlerts() {
    fetch('/get_stock_alerts')
    .then(response => response.json())
    .then(data => {
        const stockAlertsContainer = document.getElementById('stock-alerts');
        stockAlertsContainer.innerHTML = data.map(alert => `
            <p><strong>Stock Name:</strong> ${alert.stock_name}</p>
            <p><strong>Current Price:</strong> ${alert.stock_price}</p>
            <p><strong>1 Year Avg Price:</strong> ${alert.avg_price_1y}</p>
            <hr>
        `).join('');
    })
    .catch(error => console.log(error));
}

function addNewStock() {
    const newStock = document.getElementById('new-stock').value.trim();
    if (!newStock) {
        document.getElementById('add-stock-message').textContent = 'Please enter a stock symbol.';
        return;
    }
    fetch('/add_stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ stock_name: newStock })
    })
    .then(response => response.json())
    .then(data => {
        const messageContainer = document.getElementById('add-stock-message');
        messageContainer.textContent = data.message;
        if (data.success) {
            document.getElementById('stock-dropdown').innerHTML += `<option value="${newStock}.NS">${newStock}.NS</option>`;
            document.getElementById('new-stock').value = '';
        }
    })
    .catch(error => console.log(error));
}
