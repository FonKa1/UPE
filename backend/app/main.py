from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template
import json
import os
import sys
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATES_DIR)
CORS(app)
# Если db.py в той же папке:
try:
    from db import init_db, get_connection
except ImportError:
    # Создаем заглушки для тестирования
    print("⚠ Внимание: db.py не найден, используем заглушки")
    
    def init_db():
        print("Инициализация БД пропущена (файл db.py не найден)")
    
    def get_connection():
        print("Подключение к БД пропущено")
        return None
# Добавляем путь для импорта модуля database
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

app = Flask(__name__)
@app.route('/')
def index():
    """Главная страница панели управления"""
    return render_template('extracted_html.html')

@app.route('/admin')
def admin_panel():
    """Альтернативный путь к панели"""
    return render_template('extracted_html.html')
CORS(app)

# ============= TARIFFS API =============

@app.route('/api/tariffs', methods=['GET'])
def get_tariffs():
    """Получить все тарифы"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tariffs ORDER BY price_per_hour')
        tariffs = []
        for row in cursor.fetchall():
            tariff = dict(row)
            tariff['features'] = json.loads(tariff['features']) if tariff['features'] else []
            tariffs.append(tariff)
        conn.close()
        return jsonify({'success': True, 'data': tariffs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/tariffs/<int:tariff_id>', methods=['GET'])
def get_tariff(tariff_id):
    """Получить тариф по ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tariffs WHERE id = ?', (tariff_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'success': False, 'error': 'Tariff not found'}), 404
        
        tariff = dict(row)
        tariff['features'] = json.loads(tariff['features']) if tariff['features'] else []
        return jsonify({'success': True, 'data': tariff})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= COMPUTERS API =============

@app.route('/api/computers', methods=['GET'])
def get_computers():
    """Получить все компьютеры"""
    try:
        tariff_id = request.args.get('tariff_id', type=int)
        status = request.args.get('status')
        
        conn = get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT c.*, t.name as tariff_name, t.price_per_hour
            FROM computers c
            LEFT JOIN tariffs t ON c.tariff_id = t.id
            WHERE 1=1
        '''
        params = []
        
        if tariff_id:
            query += ' AND c.tariff_id = ?'
            params.append(tariff_id)
        
        if status:
            query += ' AND c.status = ?'
            params.append(status)
        
        query += ' ORDER BY c.id'
        
        cursor.execute(query, params)
        computers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'data': computers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/computers/<int:computer_id>', methods=['GET'])
def get_computer(computer_id):
    """Получить компьютер по ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, t.name as tariff_name, t.price_per_hour
            FROM computers c
            LEFT JOIN tariffs t ON c.tariff_id = t.id
            WHERE c.id = ?
        ''', (computer_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'success': False, 'error': 'Computer not found'}), 404
        
        return jsonify({'success': True, 'data': dict(row)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/computers/<int:computer_id>/status', methods=['PUT'])
def update_computer_status(computer_id):
    """Обновить статус компьютера"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['available', 'occupied', 'maintenance']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE computers SET status = ? WHERE id = ?', (status, computer_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'success': False, 'error': 'Computer not found'}), 404
        
        conn.close()
        return jsonify({'success': True, 'message': 'Status updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= BOOKINGS API =============

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Получить все бронирования"""
    try:
        status = request.args.get('status')
        date = request.args.get('date')
        
        conn = get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT b.*, t.name as tariff_name, c.name as computer_name
            FROM bookings b
            LEFT JOIN tariffs t ON b.tariff_id = t.id
            LEFT JOIN computers c ON b.computer_id = c.id
            WHERE 1=1
        '''
        params = []
        
        if status:
            query += ' AND b.status = ?'
            params.append(status)
        
        if date:
            query += ' AND b.booking_date = ?'
            params.append(date)
        
        query += ' ORDER BY b.booking_date DESC, b.booking_time DESC'
        
        cursor.execute(query, params)
        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'data': bookings})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Получить бронирование по ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, t.name as tariff_name, c.name as computer_name
            FROM bookings b
            LEFT JOIN tariffs t ON b.tariff_id = t.id
            LEFT JOIN computers c ON b.computer_id = c.id
            WHERE b.id = ?
        ''', (booking_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'success': False, 'error': 'Booking not found'}), 404
        
        return jsonify({'success': True, 'data': dict(row)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bookings', methods=['POST'])
def create_booking():
    """Создать новое бронирование"""
    try:
        data = request.get_json()
        
        # Валидация обязательных полей
        required_fields = ['client_name', 'client_phone', 'client_email', 
                          'booking_date', 'booking_time', 'duration', 'tariff_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Получаем тариф для расчета цены
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT price_per_hour FROM tariffs WHERE id = ?', (data['tariff_id'],))
        tariff = cursor.fetchone()
        
        if not tariff:
            conn.close()
            return jsonify({'success': False, 'error': 'Tariff not found'}), 404
        
        # Рассчитываем общую стоимость
        total_price = tariff['price_per_hour'] * data['duration']
        
        # Находим свободный компьютер для выбранного тарифа
        cursor.execute('''
            SELECT id FROM computers 
            WHERE tariff_id = ? AND status = 'available'
            LIMIT 1
        ''', (data['tariff_id'],))
        computer = cursor.fetchone()
        computer_id = computer['id'] if computer else None
        
        # Создаем бронирование
        cursor.execute('''
            INSERT INTO bookings 
            (client_name, client_phone, client_email, booking_date, booking_time, 
             duration, tariff_id, computer_id, total_price, comments, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        ''', (
            data['client_name'],
            data['client_phone'],
            data['client_email'],
            data['booking_date'],
            data['booking_time'],
            data['duration'],
            data['tariff_id'],
            computer_id,
            total_price,
            data.get('comments', '')
        ))
        
        booking_id = cursor.lastrowid
        
        # Если компьютер найден, меняем его статус
        if computer_id:
            cursor.execute('UPDATE computers SET status = "occupied" WHERE id = ?', (computer_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Booking created successfully',
            'data': {
                'booking_id': booking_id,
                'total_price': total_price,
                'computer_id': computer_id
            }
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bookings/<int:booking_id>/status', methods=['PUT'])
def update_booking_status(booking_id):
    """Обновить статус бронирования"""
    try:
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['pending', 'confirmed', 'cancelled', 'completed']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Получаем информацию о бронировании
        cursor.execute('SELECT computer_id FROM bookings WHERE id = ?', (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            conn.close()
            return jsonify({'success': False, 'error': 'Booking not found'}), 404
        
        # Обновляем статус бронирования
        cursor.execute('UPDATE bookings SET status = ? WHERE id = ?', (status, booking_id))
        
        # Если бронирование отменено или завершено, освобождаем компьютер
        if status in ['cancelled', 'completed'] and booking['computer_id']:
            cursor.execute('UPDATE computers SET status = "available" WHERE id = ?', (booking['computer_id'],))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Booking status updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """Удалить бронирование"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Получаем компьютер, связанный с бронированием
        cursor.execute('SELECT computer_id FROM bookings WHERE id = ?', (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            conn.close()
            return jsonify({'success': False, 'error': 'Booking not found'}), 404
        
        # Удаляем бронирование
        cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
        
        # Освобождаем компьютер
        if booking['computer_id']:
            cursor.execute('UPDATE computers SET status = "available" WHERE id = ?', (booking['computer_id'],))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Booking deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= SERVICES API =============

@app.route('/api/services', methods=['GET'])
def get_services():
    """Получить все услуги"""
    try:
        category = request.args.get('category')
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('SELECT * FROM services WHERE category = ? ORDER BY name', (category,))
        else:
            cursor.execute('SELECT * FROM services ORDER BY category, name')
        
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'data': services})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= STATISTICS API =============

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Получить статистику"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Общее количество компьютеров
        cursor.execute('SELECT COUNT(*) as total FROM computers')
        total_computers = cursor.fetchone()['total']
        
        # Доступные компьютеры
        cursor.execute("SELECT COUNT(*) as available FROM computers WHERE status = 'available'")
        available_computers = cursor.fetchone()['available']
        
        # Бронирования за сегодня
        cursor.execute("SELECT COUNT(*) as today FROM bookings WHERE booking_date = date('now')")
        bookings_today = cursor.fetchone()['today']
        
        # Активные бронирования
        cursor.execute("SELECT COUNT(*) as active FROM bookings WHERE status IN ('confirmed', 'pending')")
        active_bookings = cursor.fetchone()['active']
        
        # Общая выручка
        cursor.execute("SELECT SUM(total_price) as revenue FROM bookings WHERE status IN ('confirmed', 'completed')")
        total_revenue = cursor.fetchone()['revenue'] or 0
        
        conn.close()
        
        stats = {
            'computers': {
                'total': total_computers,
                'available': available_computers,
                'occupied': total_computers - available_computers
            },
            'bookings': {
                'today': bookings_today,
                'active': active_bookings
            },
            'revenue': {
                'total': total_revenue
            }
        }
        
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============= HEALTH CHECK =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API"""
    return jsonify({
        'success': True,
        'message': 'PC Club API is running',
        'status': 'healthy',
        'version': '1.0.0'
    })


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============= MAIN =============

if __name__ == '__main__':
    print("🚀 Запуск PC Club CYBERARENA API...")
    print("📁 Текущая директория:", os.path.dirname(os.path.abspath(__file__)))
    
    # Инициализация базы данных
    try:
        init_db()
        print("✅ База данных инициализирована")
    except Exception as e:
        print(f"⚠ Ошибка инициализации БД: {e}")
        print("⚠ API будет запущен без БД")
    
    # Запуск сервера
    print("🌐 Сервер запускается на http://localhost:5000")
    print("📋 Доступные endpoints:")
    print("   • /api/health - проверка работы API")
    print("   • /api/tariffs - все тарифы")
    print("   • /api/computers - все компьютеры")
    print("   • /api/bookings - бронирования")
    print("   • /api/services - услуги")
    print("   • /api/statistics - статистика")
    print("\n🛑 Для остановки нажмите Ctrl+C\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)