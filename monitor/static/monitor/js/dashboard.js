// Auto-refresh every 10 seconds
setTimeout(function(){
    location.reload();
}, 10000);

// Chart.js configuration
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('metricsChart').getContext('2d');
    
    // Get data from template (passed via data attributes)
    const chartElement = document.getElementById('chartData');
    const timestamps = JSON.parse(chartElement.dataset.timestamps);
    const cpuData = JSON.parse(chartElement.dataset.cpu);
    const tempData = JSON.parse(chartElement.dataset.temp);
    const memoryData = JSON.parse(chartElement.dataset.memory);
    
    const chart = new Chart(ctx, {
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
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
});