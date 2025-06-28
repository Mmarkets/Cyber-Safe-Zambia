// Sidebar Toggle
document.getElementById('sidebar-toggle').addEventListener('click', () => {
    const sidebar = document.getElementById('sidebar-wrapper');
    sidebar.classList.toggle('active');
    sidebar.classList.toggle('hidden');
    document.body.classList.toggle('sidebar-hidden');
});

// Theme Toggle
document.getElementById('theme-toggle').addEventListener('click', () => {
    document.documentElement.classList.toggle('dark-mode');
    const theme = document.documentElement.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
    fetch('/set-theme', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ theme })
    }).catch(error => console.error('Theme save error:', error));
});

// Apply saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark-mode');
}

// Language Selector
document.getElementById('language-select').addEventListener('change', (e) => {
    window.location.href = `?lang=${e.target.value}`;
});

// Progress Circle Animation
document.querySelectorAll('.progress-circle').forEach(circle => {
    const value = parseInt(circle.getAttribute('data-value'));
    const fg = circle.querySelector('.fg');
    const offset = 283 - (283 * value) / 100;
    fg.style.strokeDashoffset = offset;
});

// WebSocket for Notifications
const ws = new WebSocket('ws://' + window.location.host + '/notifications');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    document.getElementById('notification-count').textContent = data.count;
};

// Onboarding Tour
if (!localStorage.getItem('tourCompleted')) {
    const tourSteps = [
        { element: '.sidebar-brand', message: '{{ gettext('Welcome to Cyber Safe Zambia! Start here.') }}' },
        { element: '.notification-bell', message: '{{ gettext('Check notifications for alerts.') }}' },
        { element: '.dark-mode-toggle', message: '{{ gettext('Toggle dark mode for comfort.') }}' }
    ];
    let currentStep = 0;
    const tooltip = document.createElement('div');
    tooltip.style.position = 'absolute';
    tooltip.style.background = 'var(--black)';
    tooltip.style.color = 'var(--white)';
    tooltip.style.padding = '10px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.zIndex = '3000';
    document.body.appendChild(tooltip);

    function showStep() {
        if (currentStep >= tourSteps.length) {
            tooltip.remove();
            localStorage.setItem('tourCompleted', 'true');
            return;
        }
        const el = document.querySelector(tourSteps[currentStep].element);
        if (el) {
            const rect = el.getBoundingClientRect();
            tooltip.textContent = tourSteps[currentStep].message;
            tooltip.style.top = `${rect.bottom + 10}px`;
            tooltip.style.left = `${rect.left}px`;
            el.scrollIntoView({ behavior: 'smooth' });
        }
        currentStep++;
    }

    tooltip.addEventListener('click', showStep);
    showStep();
};

// AJAX Interceptor for Loading Spinner
$(document).ajaxStart(() => {
    document.getElementById('loadingSpinner').style.display = 'flex';
}).ajaxStop(() => {
    document.getElementById('loadingSpinner').style.display = 'none';
});