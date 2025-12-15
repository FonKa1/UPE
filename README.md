PC Club CYBERARENA - Веб-приложение

Полнофункциональное веб-приложение для управления компьютерным клубом с системой бронирования, учетом компьютеров и тарифов.

![Stack](https://img.shields.io/badge/Stack-Python%20|%20Flask%20|%20SQLite%20|%20HTML%20|%20CSS%20|%20JavaScript-blue)

Описание проекта

CYBERARENA - это современное веб-приложение для PC клуба, которое включает:

- **Frontend**: Адаптивный веб-интерфейс с киберпанк дизайном
- **Backend**: REST API на Flask с SQLite базой данных
- **API Документация**: Swagger UI для тестирования API
- **База данных**: SQLite3 с автоматической инициализацией

Быстрый старт

### 1. Backend (API сервер)

```bash
cd backend
pip install -r requirements.txt --break-system-packages
cd app
python main.py
```

API будет доступен на `http://localhost:5000`

Swagger документация: `http://localhost:5000/api/docs`

### 2. Frontend (веб-интерфейс)

```bash
cd frontend
python -m http.server 8000
```

Откройте в браузере: `http://localhost:8000/index_new.html`

Структура проекта

```
pc-club-app/
├── backend/                    # Backend часть
│   ├── app/
│   │   ├── main.py            # Flask приложение
│   │   └── static/
│   │       └── swagger.json   # Swagger документация
│   ├── database/
│   │   ├── db.py              # Модуль работы с БД
│   │   └── pc_club.db         # SQLite база (создается автоматически)
│   ├── requirements.txt        # Python зависимости
│   └── README.md              # Документация backend
│
└── frontend/                   # Frontend часть
    ├── index_new.html         # Главный HTML файл ✨
    ├── index.html             # Оригинальный файл (для справки)
    ├── styles.css             # CSS стили
    ├── app.js                 # JavaScript с API интеграцией
    └── README.md              # Документация frontend
```

Технологии

### Backend
- **Python 3.10+**
- **Flask** - веб-фреймворк
- **SQLite3** - реляционная база данных
- **Flask-CORS** - поддержка CORS
- **Swagger UI** - документация API

### Frontend
- **HTML5** - структура
- **CSS3** - стили и анимации
- **JavaScript ES6+** - логика
- **Fetch API** - HTTP запросы

Основные функции

### Управление тарифами
- 3 тарифа: STANDARD, PRO, VIP
- Разные конфигурации компьютеров
- Гибкая ценовая политика

### Управление компьютерами
- 8 игровых ПК разных конфигураций
- Отслеживание статуса (доступен/занят/обслуживание)
- Привязка к тарифам

### Система бронирования
- Онлайн бронирование мест
- Автоматический расчет стоимости
- Проверка доступности
- Управление статусами бронирований

### Дополнительные услуги
- Организация турниров
- Проведение мероприятий
- VIP зоны
- Стриминг поддержка

### Статистика
- Количество доступных ПК
- Активные бронирования
- Общая выручка

API Endpoints

### Тарифы
- `GET /api/tariffs` - все тарифы
- `GET /api/tariffs/{id}` - тариф по ID

### Компьютеры
- `GET /api/computers` - все компьютеры
- `GET /api/computers/{id}` - компьютер по ID
- `PUT /api/computers/{id}/status` - обновить статус

### Бронирования
- `GET /api/bookings` - все бронирования
- `POST /api/bookings` - создать бронирование
- `GET /api/bookings/{id}` - бронирование по ID
- `PUT /api/bookings/{id}/status` - обновить статус
- `DELETE /api/bookings/{id}` - удалить бронирование

### Услуги
- `GET /api/services` - все услуги

### Статистика
- `GET /api/statistics` - общая статистика
- `GET /api/health` - проверка работы API

Дизайн

### Цветовая палитра
- **Основной фон**: `#121212`
- **Вторичный фон**: `#1A1A1A`
- **Акцент**: `#00FFFF` (cyan)
- **Текст**: `#E0E0E0`

### Особенности
- Темная киберпанк тема
- Адаптивный дизайн
- Плавные анимации
- Игровая атмосфера

База данных

### Таблицы

**tariffs** - Тарифы
- id, name, price_per_hour, description, features

**computers** - Компьютеры
- id, name, cpu, gpu, ram, monitor, peripherals, tariff_id, status

**bookings** - Бронирования
- id, client_name, client_phone, client_email, booking_date, booking_time, duration, tariff_id, computer_id, total_price, comments, status

**services** - Дополнительные услуги
- id, name, description, price, category

Тестирование

### Тестирование API через Swagger
1. Запустите backend
2. Откройте `http://localhost:5000/api/docs`
3. Тестируйте endpoints напрямую в интерфейсе

### Тестирование через curl

```bash
# Получить все тарифы
curl http://localhost:5000/api/tariffs

# Создать бронирование
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Иван Иванов",
    "client_phone": "+7 999 123-45-67",
    "client_email": "ivan@example.com",
    "booking_date": "2025-12-20",
    "booking_time": "15:00",
    "duration": 3,
    "tariff_id": 2
  }'
```

Настройка

### Backend
Измените порт в `backend/app/main.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Frontend
Измените API URL в `frontend/app.js`:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

Начальные данные

При первом запуске автоматически создаются:
- 3 тарифа (STANDARD, PRO, VIP)
- 8 компьютеров (3 Standard + 3 Pro + 2 VIP)
- 5 дополнительных услуг

Устранение неполадок

### CORS ошибки
Убедитесь, что:
1. Backend запущен
2. Flask-CORS установлен
3. Frontend открыт через HTTP сервер (не file://)

### База данных не создается
Проверьте права доступа к папке `backend/database/`

### API не отвечает
Проверьте:
1. Backend запущен на порту 5000
2. Нет конфликтов портов
3. Firewall не блокирует соединение

Команда разработки

**Frontend разработчик:**
- HTML, CSS, JavaScript
- API интеграция
- UI/UX дизайн

**Backend разработчик:**
- Python, Flask
- SQLite3
- REST API
- Swagger документация

Лицензия

Этот проект создан в образовательных целях.

Roadmap

- [ ] Авторизация пользователей
- [ ] Админ панель
- [ ] Интеграция оплаты
- [ ] Email уведомления
- [ ] Мобильное приложение
- [ ] Dashboard с аналитикой

Контакты

- Email: info@cyberarena.ru
- Telegram: @cyberarena
- Discord: CYBERARENA Server

---

**Сделано с ❤️ для геймеров**
