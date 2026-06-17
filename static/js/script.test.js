/**
 * script.test.js
 * Jest tests for static/js/script.js (Forefront HQ)
 *
 * Run with: npm test
 */

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function setupAlerts(count = 1) {
    document.body.innerHTML = Array.from({ length: count })
        .map((_, i) => `<div class="fhq-alert" id="alert-${i}">Message ${i}</div>`)
        .join('');
    return document.querySelectorAll('.fhq-alert');
}

function setupPackageBuilder({ checked = [], pages = 0, pricePerPage = 50 } = {}) {
    document.body.innerHTML = `
        <div id="builder">
            <input type="checkbox" class="addon-checkbox" data-price="150" ${checked.includes(0) ? 'checked' : ''}>
            <input type="checkbox" class="addon-checkbox" data-price="75"  ${checked.includes(1) ? 'checked' : ''}>
            <input id="addon-pages-input" type="number" value="${pages}" data-price="${pricePerPage}">
            <span id="running-total">0</span>
            <button id="summary-btn" disabled>View Summary</button>
        </div>
    `;
}

// ---------------------------------------------------------------------------
// Auto-dismiss flash messages
// ---------------------------------------------------------------------------

describe('Auto-dismiss flash messages', () => {

    beforeEach(() => {
        jest.resetModules();
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.useRealTimers();
        document.body.innerHTML = '';
    });

    test('alert is still visible before 5 seconds', () => {
        setupAlerts(1);
        require('./script.js');

        jest.advanceTimersByTime(4999);
        expect(document.querySelector('.fhq-alert')).not.toBeNull();
    });

    test('alert begins fading after 5 seconds', () => {
        setupAlerts(1);
        require('./script.js');

        jest.advanceTimersByTime(5000);
        const alert = document.querySelector('.fhq-alert');
        expect(alert.style.opacity).toBe('0');
    });

    test('alert is removed from DOM after fade completes', () => {
        setupAlerts(1);
        require('./script.js');

        jest.advanceTimersByTime(5000 + 400);
        expect(document.querySelector('.fhq-alert')).toBeNull();
    });

    test('transition is set before fade out', () => {
        setupAlerts(1);
        require('./script.js');

        jest.advanceTimersByTime(5000);
        const alert = document.querySelector('.fhq-alert');
        expect(alert.style.transition).toBe('opacity 0.4s');
    });

    test('multiple alerts are all dismissed', () => {
        setupAlerts(3);
        require('./script.js');

        jest.advanceTimersByTime(5000 + 400);
        expect(document.querySelectorAll('.fhq-alert').length).toBe(0);
    });

    test('no error when no alerts are present', () => {
        document.body.innerHTML = '';
        expect(() => require('./script.js')).not.toThrow();
    });

});

// ---------------------------------------------------------------------------
// Custom package builder — total calculation
// ---------------------------------------------------------------------------

describe('Custom package builder — total calculation', () => {

    beforeEach(() => {
        jest.resetModules();
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.useRealTimers();
        document.body.innerHTML = '';
    });

    test('total is 0 when no checkboxes are checked and pages is 0', () => {
        setupPackageBuilder();
        require('./script.js');

        const total = document.getElementById('running-total').textContent;
        expect(total).toBe('0');
    });

    test('total reflects a single checked addon', () => {
        setupPackageBuilder({ checked: [0] });
        require('./script.js');

        expect(document.getElementById('running-total').textContent).toBe('150');
    });

    test('total reflects multiple checked addons', () => {
        setupPackageBuilder({ checked: [0, 1] });
        require('./script.js');

        expect(document.getElementById('running-total').textContent).toBe('225');
    });

    test('total includes page cost when pages are set', () => {
        setupPackageBuilder({ pages: 3, pricePerPage: 50 });
        require('./script.js');

        expect(document.getElementById('running-total').textContent).toBe('150');
    });

    test('total combines addons and pages correctly', () => {
        setupPackageBuilder({ checked: [0], pages: 2, pricePerPage: 50 });
        require('./script.js');

        expect(document.getElementById('running-total').textContent).toBe('250');
    });

    test('summary button is disabled when total is 0', () => {
        setupPackageBuilder();
        require('./script.js');

        expect(document.getElementById('summary-btn').disabled).toBe(true);
    });

    test('summary button is enabled when total is greater than 0', () => {
        setupPackageBuilder({ checked: [0] });
        require('./script.js');

        expect(document.getElementById('summary-btn').disabled).toBe(false);
    });

});

// ---------------------------------------------------------------------------
// Custom package builder — checkbox interaction
// ---------------------------------------------------------------------------

describe('Custom package builder — checkbox interaction', () => {

    beforeEach(() => {
        jest.resetModules();
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.useRealTimers();
        document.body.innerHTML = '';
    });

    test('checking an addon updates the total', () => {
        setupPackageBuilder();
        require('./script.js');

        const checkbox = document.querySelectorAll('.addon-checkbox')[0];
        checkbox.checked = true;
        checkbox.dispatchEvent(new Event('change'));

        expect(document.getElementById('running-total').textContent).toBe('150');
    });

    test('unchecking an addon reduces the total', () => {
        setupPackageBuilder({ checked: [0, 1] });
        require('./script.js');

        const checkbox = document.querySelectorAll('.addon-checkbox')[0];
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change'));

        expect(document.getElementById('running-total').textContent).toBe('75');
    });

    test('unchecking all addons disables the summary button', () => {
        setupPackageBuilder({ checked: [0] });
        require('./script.js');

        const checkbox = document.querySelectorAll('.addon-checkbox')[0];
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change'));

        expect(document.getElementById('summary-btn').disabled).toBe(true);
    });

});

// ---------------------------------------------------------------------------
// Custom package builder — page input interaction
// ---------------------------------------------------------------------------

describe('Custom package builder — page input interaction', () => {

    beforeEach(() => {
        jest.resetModules();
        jest.useFakeTimers();
    });

    afterEach(() => {
        jest.useRealTimers();
        document.body.innerHTML = '';
    });

    test('changing page input updates the total', () => {
        setupPackageBuilder({ pricePerPage: 50 });
        require('./script.js');

        const pageInput = document.getElementById('addon-pages-input');
        pageInput.value = '2';
        pageInput.dispatchEvent(new Event('input'));

        expect(document.getElementById('running-total').textContent).toBe('100');
    });

    test('setting pages to 0 removes page cost from total', () => {
        setupPackageBuilder({ pages: 3, pricePerPage: 50 });
        require('./script.js');

        const pageInput = document.getElementById('addon-pages-input');
        pageInput.value = '0';
        pageInput.dispatchEvent(new Event('input'));

        expect(document.getElementById('running-total').textContent).toBe('0');
    });

    test('invalid page input treated as 0', () => {
        setupPackageBuilder();
        require('./script.js');

        const pageInput = document.getElementById('addon-pages-input');
        pageInput.value = 'abc';
        pageInput.dispatchEvent(new Event('input'));

        expect(document.getElementById('running-total').textContent).toBe('0');
    });

    test('no error when page input is absent', () => {
        document.body.innerHTML = `
            <input type="checkbox" class="addon-checkbox" data-price="150">
            <span id="running-total">0</span>
            <button id="summary-btn" disabled>View Summary</button>
        `;
        expect(() => require('./script.js')).not.toThrow();
    });

});