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