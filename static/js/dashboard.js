$(document).ready(function() {
    // Threat Trend Chart (Line)
    const threatTrendCtx = document.getElementById('threatTrendChart').getContext('2d');
    new Chart(threatTrendCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Phishing Attempts',
                data: [10, 15, 8, 12, 20, 5],
                borderColor: '#DE2010',
                backgroundColor: 'rgba(222, 32, 16, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                tooltip: { mode: 'index', intersect: false },
                legend: { display: true }
            }
        }
    });

    // Threat Severity Chart (Doughnut)
    const threatSeverityCtx = document.getElementById('threatSeverityChart').getContext('2d');
    new Chart(threatSeverityCtx, {
        type: 'doughnut',
        data: {
            labels: ['Low', 'Medium', 'High'],
            datasets: [{
                data: [50, 30, 20],
                backgroundColor: ['#198A00', '#DE7300', '#DE2010']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: { callbacks: { label: function(context) { return `${context.label}: ${context.raw}%`; } } }
            }
        }
    });

    // Threat Table
    $('#threatTable').DataTable({
        ajax: '/api/threats',
        columns: [
            { data: 'id' },
            { data: 'type' },
            { data: 'severity', render: function(data) {
                return `<span class="badge bg-${data === 'High' ? 'danger' : data === 'Medium' ? 'warning' : 'success'}">${data}</span>`;
            }},
            { data: 'timestamp' },
            { data: 'ip_address' },
            { data: 'actions', render: function() {
                return '<button class="btn btn-sm btn-primary view-details">{{ gettext('View') }}</button>';
            }}
        ],
        responsive: true,
        language: { url: `/static/js/datatables-${document.documentElement.lang}.json` }
    });

    // Report Modal
    $('#previewReport').click(function() {
        const formData = $('#reportForm').serialize();
        $.ajax({
            url: '/api/report/preview',
            method: 'POST',
            data: formData,
            success: function(response) {
                alert('Preview: ' + JSON.stringify(response));
            },
            error: function() {
                alert('Error generating preview.');
            }
        });
    });

    $('#downloadReport').click(function() {
        const formData = $('#reportForm').serialize();
        window.location.href = '/api/report/download?' + formData;
    });

    // Date Range Picker (use flatpickr or similar)
    $('#dateRange').flatpickr({
        mode: 'range',
        dateFormat: 'Y-m-d'
    });
});