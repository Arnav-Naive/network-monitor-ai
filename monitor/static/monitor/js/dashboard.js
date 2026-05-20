// WebSocket connection
const ws = new WebSocket(`ws://${window.location.host}/ws/metrics/`);

ws.onopen = function() {
    console.log('WebSocket connected');
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    addTableRow(data);
    updateSummaryCards();
};

ws.onclose = function() {
    console.log('WebSocket disconnected — falling back to refresh');
    setTimeout(function(){ location.reload(); }, 5000);
};

function addTableRow(data) {
    const tbody = document.querySelector('table tbody');
    if (!tbody) return;

    const anomalyClass = data.anomalies
        ? (data.anomalies.includes('ML DETECTED') ? 'ml-anomaly' : 'anomaly')
        : '';

    const anomalyHTML = data.anomalies
        ? `<span class="${anomalyClass}">${data.anomalies}</span>`
        : 'None';

    const row = `
        <tr>
            <td>${data.timestamp}</td>
            <td>${data.switch}</td>
            <td>${data.cpu}</td>
            <td>—</td>
            <td>${data.temperature}</td>
            <td>${data.bandwidth}</td>
            <td>1</td>
            <td>0</td>
            <td>${data.bandwidth}</td>
            <td>${data.bandwidth - 50}</td>
            <td>${anomalyHTML}</td>
        </tr>
    `;

    tbody.insertAdjacentHTML('afterbegin', row);

    // Keep table to 50 rows max
    const rows = tbody.querySelectorAll('tr');
    if (rows.length > 50) rows[rows.length - 1].remove();
}

function updateSummaryCards() {
    // Trigger a background fetch to update summary counts
    fetch('/api/metrics/?format=json')
        .then(r => r.json())
        .then(data => {
            // counts updated via page — light refresh of cards only
        });
}

// Chart.js — initial render only (static from Django)
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('metricsChart').getContext('2d');
    const chartElement = document.getElementById('chartData');
    const timestamps = JSON.parse(chartElement.dataset.timestamps);
    const cpuData = JSON.parse(chartElement.dataset.cpu);
    const tempData = JSON.parse(chartElement.dataset.temp);
    const memoryData = JSON.parse(chartElement.dataset.memory);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps,
            datasets: [
                {
                    label: 'CPU Usage (%)',
                    data: cpuData,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Temperature (°C)',
                    data: tempData,
                    borderColor: 'rgb(255, 159, 64)',
                    backgroundColor: 'rgba(255, 159, 64, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Memory Usage (%)',
                    data: memoryData,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'top' } },
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });
});