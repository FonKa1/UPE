// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let tariffs = [];
let computers = [];
let services = [];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('PC Club App Initialized');
    
    // Load initial data
    loadTariffs();
    loadComputers();
    loadServices();
    loadStatistics();
    
    // Set minimum date for booking to today
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
        dateInput.value = today;
    }
});

// ==================== API FUNCTIONS ====================

// Fetch tariffs from API
async function loadTariffs() {
    try {
        const response = await fetch(`${API_BASE_URL}/tariffs`);
        const data = await response.json();
        
        if (data.success) {
            tariffs = data.data;
            renderTariffs();
            populateTariffSelect();
        }
    } catch (error) {
        console.error('Error loading tariffs:', error);
        showError('Ошибка загрузки тарифов');
    }
}

// Fetch computers from API
async function loadComputers() {
    try {
        const response = await fetch(`${API_BASE_URL}/computers`);
        const data = await response.json();
        
        if (data.success) {
            computers = data.data;
            renderComputers(computers);
        }
    } catch (error) {
        console.error('Error loading computers:', error);
        showError('Ошибка загрузки компьютеров');
    }
}

// Fetch services from API
async function loadServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/services`);
        const data = await response.json();
        
        if (data.success) {
            services = data.data;
            renderServices();
        }
    } catch (error) {
        console.error('Error loading services:', error);
        showError('Ошибка загрузки услуг');
    }
}

// Fetch statistics from API
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        const data = await response.json();
        
        if (data.success) {
            renderStatistics(data.data);
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Create booking via API
async function createBooking(bookingData) {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error creating booking:', error);
        throw error;
    }
}

// ==================== RENDER FUNCTIONS ====================

// Render tariffs on services page
function renderTariffs() {
    const grid = document.getElementById('tariffs-grid');
    if (!grid) return;
    
    grid.innerHTML = tariffs.map((tariff, index) => `
        <div class="pricing-card ${index === 1 ? 'featured' : ''}">
            <h3>${tariff.name}</h3>
            <div class="price">${tariff.price_per_hour} ₽</div>
            <div class="period">/час</div>
            <p>${tariff.description || ''}</p>
            ${tariff.features ? `
                <ul>
                    ${tariff.features.map(feature => `<li>${feature}</li>`).join('')}
                </ul>
            ` : ''}
            <button class="btn ${index === 1 ? 'btn-primary' : 'btn-secondary'}" 
                    onclick="showPage('booking')">
                ${index === 1 ? 'Выбрать' : 'Забронировать'}
            </button>
        </div>
    `).join('');
}

// Render computers on PCs page
function renderComputers(computersToRender) {
    const grid = document.getElementById('computers-grid');
    if (!grid) return;
    
    if (computersToRender.length === 0) {
        grid.innerHTML = '<p style="text-align: center; grid-column: 1/-1; color: var(--text-secondary);">Компьютеры не найдены</p>';
        return;
    }
    
    grid.innerHTML = computersToRender.map(pc => `
        <div class="pc-config-card">
            <h3>${pc.name}</h3>
            <div class="status ${pc.status}">${getStatusText(pc.status)}</div>
            <div class="config-spec">
                <span class="config-label">Тариф:</span>
                <span class="config-value">${pc.tariff_name || 'N/A'} (${pc.price_per_hour}₽/час)</span>
            </div>
            <div class="config-spec">
                <span class="config-label">Видеокарта:</span>
                <span class="config-value">${pc.gpu}</span>
            </div>
            <div class="config-spec">
                <span class="config-label">Процессор:</span>
                <span class="config-value">${pc.cpu}</span>
            </div>
            <div class="config-spec">
                <span class="config-label">ОЗУ:</span>
                <span class="config-value">${pc.ram}</span>
            </div>
            <div class="config-spec">
                <span class="config-label">Монитор:</span>
                <span class="config-value">${pc.monitor}</span>
            </div>
            <div class="config-spec">
                <span class="config-label">Периферия:</span>
                <span class="config-value">${pc.peripherals || 'Стандартная'}</span>
            </div>
        </div>
    `).join('');
}

// Render services on services page
function renderServices() {
    const grid = document.getElementById('services-grid');
    if (!grid) return;
    
    const serviceCards = services.filter(s => s.category !== 'gaming').map(service => `
        <div class="pricing-card">
            <h3>${service.name}</h3>
            ${service.price ? `<div class="price">${service.price} ₽</div>` : ''}
            <p>${service.description || ''}</p>
            <button class="btn btn-secondary" onclick="showPage('contacts')">Узнать больше</button>
        </div>
    `).join('');
    
    grid.innerHTML = serviceCards || '<p style="text-align: center; grid-column: 1/-1; color: var(--text-secondary);">Дополнительные услуги загружаются...</p>';
}

// Render statistics on home page
function renderStatistics(stats) {
    const grid = document.getElementById('statistics-grid');
    if (!grid) return;
    
    grid.innerHTML = `
        <div class="feature-card">
            <h3>💻 Компьютеры</h3>
            <p>Всего: ${stats.computers.total}<br>
               Доступно: ${stats.computers.available}<br>
               Занято: ${stats.computers.occupied}</p>
        </div>
        <div class="feature-card">
            <h3>📅 Бронирования</h3>
            <p>Сегодня: ${stats.bookings.today}<br>
               Активных: ${stats.bookings.active}</p>
        </div>
        <div class="feature-card">
            <h3>💰 Выручка</h3>
            <p>Всего: ${stats.revenue.total.toLocaleString('ru-RU')} ₽</p>
        </div>
    `;
}

// Populate tariff select dropdown
function populateTariffSelect() {
    const select = document.getElementById('tariff');
    if (!select) return;
    
    select.innerHTML = '<option value="">-- Выберите тариф --</option>' + 
        tariffs.map(tariff => 
            `<option value="${tariff.id}">${tariff.name} (${tariff.price_per_hour} ₽/час)</option>`
        ).join('');
}

// ==================== UTILITY FUNCTIONS ====================

// Get status text in Russian
function getStatusText(status) {
    const statusMap = {
        'available': 'Доступен',
        'occupied': 'Занят',
        'maintenance': 'Обслуживание'
    };
    return statusMap[status] || status;
}

// Show page
function showPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    // Show selected page
    const selectedPage = document.getElementById(pageId);
    if (selectedPage) {
        selectedPage.classList.add('active');
    }
    
    // Update active nav link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.dataset.page === pageId) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Filter computers by tariff
function filterComputers(tariffId) {
    if (tariffId === 'all') {
        renderComputers(computers);
    } else {
        const filtered = computers.filter(pc => pc.tariff_id === tariffId);
        renderComputers(filtered);
    }
}

// Calculate booking price
function calculatePrice() {
    const tariffSelect = document.getElementById('tariff');
    const durationInput = document.getElementById('duration');
    const priceInfo = document.getElementById('price-info');
    const totalPriceEl = document.getElementById('total-price');
    
    if (!tariffSelect || !durationInput || !priceInfo || !totalPriceEl) return;
    
    const tariffId = parseInt(tariffSelect.value);
    const duration = parseInt(durationInput.value);
    
    if (tariffId && duration) {
        const tariff = tariffs.find(t => t.id === tariffId);
        if (tariff) {
            const total = tariff.price_per_hour * duration;
            totalPriceEl.textContent = `${total.toLocaleString('ru-RU')} ₽`;
            priceInfo.style.display = 'block';
        }
    } else {
        priceInfo.style.display = 'none';
    }
}

// Handle booking form submission
async function handleBooking(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Get form data
    const bookingData = {
        client_name: form.name.value,
        client_phone: form.phone.value,
        client_email: form.email.value,
        booking_date: form.date.value,
        booking_time: form.time.value,
        duration: parseInt(form.duration.value),
        tariff_id: parseInt(form.tariff.value),
        comments: form.comments.value
    };
    
    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Обработка...';
    
    try {
        const result = await createBooking(bookingData);
        
        if (result.success) {
            // Show success message
            showSuccess(`Бронирование успешно создано! ID: ${result.data.booking_id}. Итого: ${result.data.total_price} ₽`);
            
            // Reset form
            form.reset();
            document.getElementById('price-info').style.display = 'none';
            
            // Set date to today again
            const today = new Date().toISOString().split('T')[0];
            form.date.value = today;
            
            // Reload statistics
            loadStatistics();
        } else {
            showError(result.error || 'Ошибка при создании бронирования');
        }
    } catch (error) {
        showError('Не удалось создать бронирование. Проверьте подключение к серверу.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Забронировать';
    }
}

// Show success message
function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success';
    alert.textContent = message;
    
    const container = document.querySelector('.booking-form');
    if (container) {
        container.insertBefore(alert, container.firstChild);
        
        // Remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    } else {
        alert(message);
    }
}

// Show error message
function showError(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-error';
    alert.textContent = message;
    
    const container = document.querySelector('.booking-form') || document.querySelector('.container');
    if (container) {
        container.insertBefore(alert, container.firstChild);
        
        // Remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    } else {
        alert(message);
    }
}

// Make functions available globally
window.showPage = showPage;
window.filterComputers = filterComputers;
window.calculatePrice = calculatePrice;
window.handleBooking = handleBooking;
