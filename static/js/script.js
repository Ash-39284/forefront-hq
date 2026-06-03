// Auto-dismiss flash messages after 5s
document.querySelectorAll('.fhq-alert').forEach(el => {
    setTimeout(() => {
        el.style.transition = 'opacity 0.4s';
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 400);
    }, 5000);
});

// Custom package builder
const checkboxes = document.querySelectorAll('.addon-checkbox');

if (checkboxes.length > 0) {
    const totalEl = document.getElementById('running-total');
    const summaryBtn = document.getElementById('summary-btn');

    function updateTotal() {
        let total = 0;
        checkboxes.forEach(cb => {
            if (cb.checked) total += parseFloat(cb.dataset.price);
        });
        totalEl.textContent = total.toFixed(0);
        summaryBtn.disabled = total === 0;
    }

    checkboxes.forEach(cb => cb.addEventListener('change', updateTotal));
}