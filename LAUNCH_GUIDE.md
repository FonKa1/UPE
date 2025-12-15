ИНСТРУКЦИЯ ПО ЗАПУСКУ ВЕБ-ПРИЛОЖЕНИЯ PC CLUB CYBERARENA
ТРЕБОВАНИЯ

Необходимое ПО:

- **Python 3.8+** (проверено на Python 3.10)
- **pip** (менеджер пакетов Python)
- Веб-браузер (Chrome, Firefox, Safari, Edge)
  
### Опционально:

- **Git** (для клонирования репозитория)
- **Node.js** (для продвинутых инструментов разработки)

---

СПОСОБЫ ЗАПУСКА

СПОСОБ 1: Автоматический запуск (рекомендуется)

#### Linux / macOS:

```bash
cd pc-club-app
chmod +x start.sh
./start.sh
```

#### Windows:

```cmd
cd pc-club-app
start.bat
```

**Что происходит:**
1. Автоматически устанавливаются зависимости
2. Запускается Backend сервер на порту 5000
3. Запускается Frontend сервер на порту 8000
4. Открывается браузер с приложением

---

СПОСОБ 2: Ручной запуск (полный контроль)

#### ШАГ 1: Установка зависимостей Backend

```bash
cd pc-club-app/backend
pip install -r requirements.txt
```

**Для Linux (если требуется):**
```bash
pip install -r requirements.txt --break-system-packages
```

**Устанавливаемые пакеты:**
- Flask 3.0.0
- Flask-CORS 4.0.0
- flask-swagger-ui 4.11.1
- python-dotenv 1.0.0

#### ШАГ 2: Запуск Backend сервера

```bash
cd backend/app
python main.py
```

**Ожидаемый вывод:**
```
✓ База данных инициализирована: .../pc_club.db
 * Serving Flask app 'main'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
```

**Backend готов!** API доступен на `http://localhost:5000/api/`

#### ШАГ 3: Запуск Frontend сервера (новый терминал)

```bash
cd pc-club-app/frontend
python -m http.server 8000
```

**Альтернативы для Frontend:**

**Node.js (http-server):**
```bash
npx http-server -p 8000
```

**PHP:**
```bash
php -S localhost:8000
```

**Frontend готов!** Сайт доступен на `http://localhost:8000/index_new.html`

---

### СПОСОБ 3: Запуск интеграционного теста

Запускает оба сервера и тестирует все компоненты:

```bash
cd pc-club-app
python integration_test.py
```

**Что происходит:**
1. Запускается Backend
2. Тестируются все API endpoints
3. Запускается Frontend
4. Выводится полный отчет о работоспособности

---

## ДОСТУП К ПРИЛОЖЕНИЮ

После успешного запуска откройте в браузере:

### Frontend (основное приложение):
```
http://localhost:8000/index_new.html
```

### Backend API:
```
http://localhost:5000/api/
```

### Swagger документация:
```
http://localhost:5000/api/docs
```

### Демо страница:
```
http://localhost:8000/DEMO.html
```

---

## ТЕСТИРОВАНИЕ API

### Примеры запросов:

**1. Проверка работоспособности:**
```bash
curl http://localhost:5000/api/health
```

**Ответ:**
```json
{
  "success": true,
  "message": "PC Club API is running",
  "version": "1.0.0"
}
```

**2. Получить все тарифы:**
```bash
curl http://localhost:5000/api/tariffs
```

**3. Получить все компьютеры:**
```bash
curl http://localhost:5000/api/computers
```

**4. Создать бронирование:**
```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Иван Иванов",
    "client_phone": "+7 999 123-45-67",
    "client_email": "ivan@example.com",
    "booking_date": "2025-12-25",
    "booking_time": "18:00",
    "duration": 3,
    "tariff_id": 2,
    "comments": "Хочу поиграть в CS2"
  }'
```

**5. Получить статистику:**
```bash
curl http://localhost:5000/api/statistics
```

---

ВОЗМОЖНЫЕ ПРОБЛЕМЫ И РЕШЕНИЯ

### Проблема 1: Порт уже занят

**Ошибка:** `Address already in use`

**Решение:**

**Для порта 5000 (Backend):**
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Для порта 8000 (Frontend):**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Проблема 2: Модуль не найден

**Ошибка:** `ModuleNotFoundError: No module named 'flask'`

**Решение:**
```bash
cd backend
pip install -r requirements.txt
```

---

### Проблема 3: CORS ошибки

**Ошибка:** `Access to fetch... has been blocked by CORS policy`

**Решение:**
1. Убедитесь, что Backend запущен
2. Убедитесь, что Frontend открыт через HTTP сервер (не напрямую через file://)
3. Проверьте, что Flask-CORS установлен: `pip install flask-cors`

---

### Проблема 4: База данных не создается

**Ошибка:** `No such file or directory: 'pc_club.db'`

**Решение:**
```bash
cd backend/database
python db.py
```

Это вручную создаст базу данных с начальными данными.

---

СТРУКТУРА ПРОЕКТА

```
pc-club-app/
├── backend/                    # Backend приложение
│   ├── app/
│   │   ├── main.py            # Flask API сервер
│   │   └── static/
│   │       └── swagger.json   # API документация
│   ├── database/
│   │   ├── db.py              # Модуль БД
│   │   └── pc_club.db         # SQLite база данных
│   └── requirements.txt       # Python зависимости
│
├── frontend/                   # Frontend приложение
│   ├── index_new.html         # Главная страница ⭐
│   ├── styles.css             # Стили
│   └── app.js                 # JavaScript логика
│
├── start.sh                    # Скрипт запуска (Linux/Mac)
├── start.bat                   # Скрипт запуска (Windows)
├── integration_test.py         # Интеграционные тесты
├── test_api.py                # Тесты API
├── DEMO.html                   # Демо страница
└── README.md                   # Документация
```

---

ИСПОЛЬЗОВАНИЕ ПРИЛОЖЕНИЯ

### 1. Главная страница
- Приветственный баннер
- Преимущества клуба

### 2. Услуги и цены
- Просмотр всех тарифов (STANDARD, PRO, VIP)
- Дополнительные услуги
- Информация о ценах

### 3. Игровые ПК
- Список всех компьютеров с характеристиками

### 4. Бронирование
- Форма для бронирования места
- Автоматический расчет стоимости
- Выбор даты, времени и продолжительности
- Выбор тарифа

### 5. Контакты
- Адрес клуба
- Телефоны и email
- Режим работы
- Социальные сети

---

##ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ

### База данных

**Расположение:** `backend/database/pc_club.db`  
**Тип:** SQLite3  
**Размер:** ~28 KB

**Таблицы:**
- `tariffs` - 3 тарифа
- `computers` - 8 компьютеров
- `bookings` - бронирования
- `services` - 5 дополнительных услуг

**Сброс БД:**
```bash
cd backend/database
rm pc_club.db
python db.py
```

---

### API Endpoints

Полный список доступен в Swagger: `http://localhost:5000/api/docs`

**Основные endpoints:**
- `GET /api/health` - проверка работы
- `GET /api/tariffs` - все тарифы
- `GET /api/computers` - все компьютеры
- `GET /api/services` - все услуги
- `GET /api/statistics` - статистика
- `POST /api/bookings` - создать бронирование
- `GET /api/bookings` - получить бронирования

---

ПРОВЕРКА РАБОТОСПОСОБНОСТИ

### Быстрая проверка:

```bash
# 1. Проверить Backend
curl http://localhost:5000/api/health

# 2. Проверить Frontend
curl http://localhost:8000/index_new.html

# 3. Полный тест
python integration_test.py
```

### Ожидаемые результаты:

Backend отвечает на порту 5000  
Frontend доступен на порту 8000  
Все API endpoints возвращают корректные данные  
CORS настроен правильно  
База данных работает  

---

ПОДДЕРЖКА

Если возникли проблемы:

1. Проверьте версию Python: `python --version` (должна быть 3.8+)
2. Проверьте, что порты 5000 и 8000 свободны
3. Убедитесь, что все зависимости установлены
4. Проверьте логи серверов
5. Запустите `integration_test.py` для диагностики

---

КОНТРОЛЬНЫЙ СПИСОК ЗАПУСКА

- [ ] Python 3.8+ установлен
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] Backend запущен (`python main.py`)
- [ ] Frontend запущен (`python -m http.server 8000`)
- [ ] Открыт браузер на `http://localhost:8000/index_new.html`
- [ ] API доступен на `http://localhost:5000/api/health`

---

**Сделано с ❤️ для геймеров**  
**© 2025 CYBERARENA**
