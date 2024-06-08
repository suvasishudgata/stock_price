// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('check-price-btn').addEventListener('click', fetchStockInfo);
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
        `;
    })
    .catch(error => console.log(error));
}
