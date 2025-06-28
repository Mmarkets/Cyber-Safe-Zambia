$(document).ready(function() {
    // User Behavior Table
    $('#userBehaviorTable').DataTable({
        ajax: '/api/user_behavior',
        columns: [
            { data: 'user_id' },
            { data: 'username' },
            { data: 'failed_logins' },
            { data: 'last_activity' },
            { data: 'status', render: function(data) {
                return `<span class="badge bg-${data === 'Normal' ? 'success' : 'danger'}">${data}</span>`;
            }}
        ],
        responsive: true,
        language: { url: `/static/js/datatables-${document.documentElement.lang}.json` }
    });

    // System Metrics Chart (Bar)
    const systemMetricsCtx = document.getElementById('systemMetricsChart').getContext('2d');
    new Chart(systemMetricsCtx, {
        type: 'bar',
        data: {
            labels: ['CPU', 'Memory', 'Disk'],
            datasets: [{
                label: 'Usage (%)',
                data: [65, 80, 45],
                backgroundColor: ['#198A00', '#DE7300', '#DE2010']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, max: 100 }
            }
        }
    });
});