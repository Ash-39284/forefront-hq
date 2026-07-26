document.addEventListener('DOMContentLoaded', function () {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function (dropdown) {
        const btn = dropdown.querySelector('.dropbtn');
        const content = dropdown.querySelector('.dropdown-content');

        btn.addEventListener('click', function (e) {
            // Only intercept the click on mobile widths — desktop uses :hover
            if (window.innerWidth < 768) {
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