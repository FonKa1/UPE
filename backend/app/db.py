import sqlite3
import json
from pathlib import Path

# Путь к базе данных
DB_PATH = Path(__file__).parent / 'pc_club.db'

def get_connection():
    """Создать подключение к БД"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Для доступа к данным по имени колонки
    return conn

def init_db():
    """Инициализация базы данных с тестовыми данными"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # ============= Создание таблиц =============
    
    # Тарифы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tariffs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price_per_hour INTEGER NOT NULL,
            description TEXT,
            features TEXT
        )
    ''')
    
    # Компьютеры
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS computers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cpu TEXT NOT NULL,
            gpu TEXT NOT NULL,
            ram TEXT NOT NULL,
            monitor TEXT NOT NULL,
            peripherals TEXT,
            tariff_id INTEGER,
            status TEXT DEFAULT 'available',
            FOREIGN KEY (tariff_id) REFERENCES tariffs (id)
        )
    ''')
    
    # Бронирования
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            client_phone TEXT NOT NULL,
            client_email TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            booking_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            tariff_id INTEGER NOT NULL,
            computer_id INTEGER,
            total_price INTEGER NOT NULL,
            comments TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tariff_id) REFERENCES tariffs (id),
            FOREIGN KEY (computer_id) REFERENCES computers (id)
        )
    ''')
    
    # Услуги
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price INTEGER,
            category TEXT
        )
    ''')
    
    conn.commit()
    
    # ============= Проверка наличия тестовых данных =============
    
    # Проверяем, есть ли уже тарифы
    cursor.execute('SELECT COUNT(*) as count FROM tariffs')
    tariff_count = cursor.fetchone()['count']
    
    if tariff_count == 0:
        print("Заполнение базы данных начальными данными...")
        fill_test_data(conn)
        print("База данных успешно инициализирована!")
    else:
        print("База данных уже содержит данные.")
    
    conn.close()

def fill_test_data(conn):
    """Заполнение базы тестовыми данными"""
    cursor = conn.cursor()
    
    # ============= ТАРИФЫ =============
    tariffs = [
        ('STANDARD', 150, 'Базовый игровой опыт', 
         json.dumps(['GTX 1660 Super', 'Intel i5', '16GB RAM', 'Full HD монитор', 'Базовая периферия'])),
        
        ('PRO', 250, 'Профессиональный уровень',
         json.dumps(['RTX 3070', 'Intel i7', '32GB RAM', 'QHD монитор 165Hz', 'Игровая мышь и клавиатура'])),
        
        ('VIP', 400, 'Элитный гейминг',
         json.dumps(['RTX 4090', 'Intel i9', '64GB RAM', '4K монитор 240Hz', 'Профессиональная периферия', 'Отдельная комната']))
    ]
    
    cursor.executemany('''
        INSERT INTO tariffs (name, price_per_hour, description, features)
        VALUES (?, ?, ?, ?)
    ''', tariffs)
    
    conn.commit()
    
    # ============= КОМПЬЮТЕРЫ =============
    computers = [
        # STANDARD компьютеры (tariff_id = 1)
        ('PC-S01', 'Intel i5-12400F', 'GTX 1660 Super', '16GB DDR4', '24" Full HD 144Hz', 'Logitech G', 1, 'available'),
        ('PC-S02', 'Intel i5-12400F', 'GTX 1660 Super', '16GB DDR4', '24" Full HD 144Hz', 'Logitech G', 1, 'available'),
        ('PC-S03', 'Intel i5-12400F', 'GTX 1660 Super', '16GB DDR4', '24" Full HD 144Hz', 'Logitech G', 1, 'available'),
        
        # PRO компьютеры (tariff_id = 2)
        ('PC-P01', 'Intel i7-12700K', 'RTX 3070', '32GB DDR4', '27" QHD 165Hz', 'Razer BlackWidow + DeathAdder', 2, 'available'),
        ('PC-P02', 'Intel i7-12700K', 'RTX 3070', '32GB DDR4', '27" QHD 165Hz', 'Razer BlackWidow + DeathAdder', 2, 'available'),
        ('PC-P03', 'Intel i7-13700K', 'RTX 4070', '32GB DDR5', '27" QHD 240Hz', 'SteelSeries Apex Pro + Rival', 2, 'available'),
        
        # VIP компьютеры (tariff_id = 3)
        ('PC-V01', 'Intel i9-13900K', 'RTX 4090', '64GB DDR5', '32" 4K 240Hz', 'Custom mechanical + Logitech G Pro', 3, 'available'),
        ('PC-V02', 'Intel i9-14900K', 'RTX 4090', '64GB DDR5', '32" 4K 240Hz', 'Custom mechanical + Logitech G Pro', 3, 'available')
    ]
    
    cursor.executemany('''
        INSERT INTO computers (name, cpu, gpu, ram, monitor, peripherals, tariff_id, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', computers)
    
    conn.commit()
    
    # ============= УСЛУГИ =============
    services = [
        ('Организация турнира', 'Проведение локального киберспортивного турнира', 5000, 'event'),
        ('Частная комната', 'Аренда отдельной комнаты на 4 часа', 2000, 'premium'),
        ('Стриминг студия', 'Оборудованное место для стриминга', 1500, 'service'),
        ('Коучинг', 'Индивидуальное обучение от про-игрока', 200, 'service'),
        ('Ночной пакет', 'Игра с 00:00 до 08:00 со скидкой', None, 'gaming')
    ]
    
    cursor.executemany('''
        INSERT INTO services (name, description, price, category)
        VALUES (?, ?, ?, ?)
    ''', services)
    
    conn.commit()
    
    # ============= ТЕСТОВЫЕ БРОНИРОВАНИЯ =============
    bookings = [
        ('Иван Иванов', '+7 (999) 123-45-67', 'ivan@example.com', 
         '2025-12-20', '15:00', 3, 2, 4, 750, 'Хочу играть в CS2', 'confirmed'),
        
        ('Петр Петров', '+7 (999) 987-65-43', 'petr@example.com',
         '2025-12-21', '18:00', 2, 1, 1, 300, 'Dota 2 матч', 'confirmed'),
        
        ('Анна Сидорова', '+7 (999) 555-12-34', 'anna@example.com',
         '2025-12-19', '12:00', 4, 3, 7, 1600, 'Стриминг сессия', 'completed')
    ]
    
    cursor.executemany('''
        INSERT INTO bookings 
        (client_name, client_phone, client_email, booking_date, booking_time, 
         duration, tariff_id, computer_id, total_price, comments, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', bookings)
    
    conn.commit()