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
const pageInput = document.getElementById('addon-pages-input');

if (checkboxes.length > 0) {
    const totalEl = document.getElementById('running-total');
    const summaryBtn = document.getElementById('summary-btn');

    function updateTotal() {
        let total = 0;
        checkboxes.forEach(cb => {
            if (cb.checked) total += parseFloat(cb.dataset.price);
        });
        if (pageInput) {
            const pages = parseInt(pageInput.value) || 0;
            const pricePerPage = parseFloat(pageInput.dataset.price) || 0;
            total += pages * pricePerPage;
        }
        totalEl.textContent = total.toFixed(0);
        summaryBtn.disabled = total === 0;
    }

    checkboxes.forEach(cb => cb.addEventListener('change', updateTotal));
    if (pageInput) pageInput.addEventListener('input', updateTotal);

    // Run on page load to reflect pre-checked boxes
    updateTotal();
}

document.addEventListener('DOMContentLoaded', function () {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function (dropdown) {
        const btn = dropdown.querySelector('.dropbtn');
        const content = dropdown.querySelector('.dropdown-content');

        btn.addEventListener('click', function (e) {
            // Only intercept the click on mobile widths — desktop uses :hover
            if (window.innerWidth <= 767) {
                e.preventDefault();
                content.classList.toggle('show');
            }
        });
    });

    // Close any open dropdown when tapping/clicking outside it
    document.addEventListener('click', function (e) {
        dropdowns.forEach(function (dropdown) {
            if (!dropdown.contains(e.target)) {
                const content = dropdown.querySelector('.dropdown-content');
                content.classList.remove('show');
            }
        });
    });
});