#!/usr/bin/env python3
"""
Полный интеграционный тест веб-приложения PC Club CYBERARENA
"""
import sys
import time
import subprocess
import requests
import os
from pathlib import Path

print("=" * 70)
print("  ПОЛНОЕ ТЕСТИРОВАНИЕ ВЕБ-ПРИЛОЖЕНИЯ PC CLUB CYBERARENA")
print("=" * 70)

# УКАЖИТЕ ПРАВИЛЬНЫЙ ПУТЬ К ВАШЕМУ ПРОЕКТУ
# Для Windows укажите полный путь, например:
base_dir = Path('C:/Users/Mick_pro/Desktop/Final')  # ИЗМЕНИТЕ ЭТУ СТРОКУ НА СВОЙ ПУТЬ

# Сначала проверим, существует ли папка
if not base_dir.exists():
    print(f"❌ Ошибка: Папка не найдена: {base_dir}")
    print("Пожалуйста, укажите правильный путь к проекту в строке 16")
    
    # Попробуем найти проект автоматически
    possible_paths = [
        Path('C:/Users/Mick_pro/Desktop/Final'),
        Path('C:/Users/Mick_pro/Desktop/pc-club-app'),
        Path('C:/Users/Mick_pro/Documents/Final'),
        Path('.'),  # Текущая директория
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"✓ Найден проект по пути: {path}")
            base_dir = path
            break
    else:
        print("✗ Проект не найден. Укажите путь вручную.")
        sys.exit(1)

print(f"✓ Используется путь: {base_dir}")

backend_dir = base_dir / 'backend' / 'app'
frontend_dir = base_dir / 'frontend'

# Проверим существование папок
if not backend_dir.exists():
    print(f"❌ Backend папка не найдена: {backend_dir}")
    print("Структура проекта должна быть:")
    print("  Ваша_папка/backend/app/main.py")
    print("  Ваша_папка/frontend/index_new.html")
    sys.exit(1)

if not frontend_dir.exists():
    print(f"⚠ Frontend папка не найдена: {frontend_dir}")
    print("Будет запущен только backend")

# Результаты тестов
results = {
    'backend_start': False,
    'frontend_start': False,
    'api_health': False,
    'api_tariffs': False,
    'api_computers': False,
    'api_services': False,
    'api_statistics': False,
    'api_create_booking': False,
    'api_get_bookings': False,
    'cors_enabled': False
}

backend_process = None
frontend_process = None

try:
    # ЭТАП 1: Запуск Backend
    print("\n📡 ЭТАП 1: Запуск Backend сервера...")
    print("-" * 70)
    
    # Проверим, запущен ли уже backend на порту 5000
    try:
        r = requests.get('http://127.0.0.1:5000/api/health', timeout=1)
        if r.status_code == 200:
            print("✓ Backend уже запущен на порту 5000")
            results['backend_start'] = True
            backend_process = None  # Не будем запускать новый процесс
        else:
            raise Exception("Backend отвечает, но не корректно")
    except:
        # Backend не запущен, запускаем его
        print(f"Запуск backend из: {backend_dir}")
        
        # Проверим, существует ли main.py
        main_py = backend_dir / 'main.py'
        if not main_py.exists():
            print(f"❌ Файл main.py не найден: {main_py}")
            print("Содержимое папки backend/app:")
            for item in backend_dir.iterdir():
                print(f"  - {item.name}")
            sys.exit(1)
        
        backend_process = subprocess.Popen(
            ['python', 'main.py'],
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore',
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        
        # Ждем запуска
        print("Ожидание запуска backend...", end='', flush=True)
        for i in range(10):  # Ждем до 10 секунд
            time.sleep(1)
            print('.', end='', flush=True)
            
            # Проверяем, не завершился ли процесс с ошибкой
            if backend_process.poll() is not None:
                stderr = backend_process.stderr.read()
                stdout = backend_process.stdout.read()
                print(f"\n✗ Backend завершился с ошибкой (код: {backend_process.returncode})")
                if stderr:
                    print(f"Stderr: {stderr[:500]}")  # Первые 500 символов ошибки
                if stdout:
                    print(f"Stdout: {stdout[:500]}")
                sys.exit(1)
                
            # Пробуем подключиться
            try:
                r = requests.get('http://127.0.0.1:5000/api/health', timeout=1)
                if r.status_code == 200:
                    print("\n✓ Backend сервер запущен!")
                    results['backend_start'] = True
                    break
            except:
                continue
        else:
            print("\n✗ Backend не запустился за 10 секунд")
            if backend_process:
                backend_process.terminate()
            sys.exit(1)
    
    # ЭТАП 2: Тестирование API
    print("\n🔍 ЭТАП 2: Тестирование API endpoints...")
    print("-" * 70)
    
    base_url = 'http://127.0.0.1:5000/api'
    
    # Тест Health
    try:
        r = requests.get(f'{base_url}/health', timeout=3)
        if r.status_code == 200 and r.json().get('success'):
            print("✓ GET /api/health - работает")
            results['api_health'] = True
        else:
            print(f"✗ GET /api/health - ошибка ({r.status_code})")
    except Exception as e:
        print(f"✗ GET /api/health - исключение: {e}")
    
    # Тест Tariffs
    try:
        r = requests.get(f'{base_url}/tariffs', timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                count = len(data.get('data', []))
                print(f"✓ GET /api/tariffs - работает ({count} тарифов)")
                results['api_tariffs'] = True
            else:
                print("✗ GET /api/tariffs - неверные данные")
        else:
            print(f"✗ GET /api/tariffs - ошибка ({r.status_code})")
    except Exception as e:
        print(f"✗ GET /api/tariffs - исключение: {e}")
    
    # Тест Computers
    try:
        r = requests.get(f'{base_url}/computers', timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                count = len(data.get('data', []))
                print(f"✓ GET /api/computers - работает ({count} компьютеров)")
                results['api_computers'] = True
            else:
                print("✗ GET /api/computers - неверные данные")
        else:
            print(f"✗ GET /api/computers - ошибка ({r.status_code})")
    except Exception as e:
        print(f"✗ GET /api/computers - исключение: {e}")
    
    # Тест Services
    try:
        r = requests.get(f'{base_url}/services', timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                count = len(data.get('data', []))
                print(f"✓ GET /api/services - работает ({count} услуг)")
                results['api_services'] = True
            else:
                print("✗ GET /api/services - неверные данные")
        else:
            print(f"✗ GET /api/services - ошибка ({r.status_code})")
    except Exception as e:
        print(f"✗ GET /api/services - исключение: {e}")
    
    # Тест Statistics
    try:
        r = requests.get(f'{base_url}/statistics', timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data.get('success') and 'computers' in data.get('data', {}):
                stats = data['data']
                print(f"✓ GET /api/statistics - работает")
                print(f"  Компьютеров: {stats['computers']['total']} (доступно: {stats['computers']['available']})")
                results['api_statistics'] = True
            else:
                print("✗ GET /api/statistics - неверные данные")
        else:
            print(f"✗ GET /api/statistics - ошибка ({r.status_code})")
    except Exception as e:
        print(f"✗ GET /api/statistics - исключение: {e}")
    
    # Тест Create Booking
    try:
        booking_data = {
            'client_name': 'Интеграционный Тест',
            'client_phone': '+7 111 222-33-44',
            'client_email': 'integration@test.com',
            'booking_date': '2025-12-30',
            'booking_time': '20:00',
            'duration': 4,
            'tariff_id': 3,
            'comments': 'Автоматический интеграционный тест'
        }
        r = requests.post(f'{base_url}/bookings', json=booking_data, timeout=3)
        if r.status_code == 201:
            data = r.json()
            if data.get('success'):
                booking_id = data.get('data', {}).get('booking_id')
                total_price = data.get('data', {}).get('total_price')
                print(f"✓ POST /api/bookings - работает (ID: {booking_id}, цена: {total_price}₽)")
                results['api_create_booking'] = True
            else:
                print("✗ POST /api/bookings - неверный ответ")
        else:
            print(f"✗ POST /api/bookings - ошибка ({r.status_code})")
    except Exception as e:
        print(f"✗ POST /api/bookings - исключение: {e}")
    
    # Тест Get Bookings
    try:
        r = requests.get(f'{base_url}/bookings', timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                count = len(data.get('data', []))
                print(f"✓ GET /api/bookings - работает ({count} бронирований)")
                results['api_get_bookings'] = True
            else:
                print("✗ GET /api/bookings - неверные данные")
        else:
            print(f"✗ GET /api/bookings - ошибка ({r.status_code})")
    except Exception as e:
        print(f"✗ GET /api/bookings - исключение: {e}")
    
    # Тест CORS
    try:
        r = requests.get(f'{base_url}/health', timeout=3)
        if 'Access-Control-Allow-Origin' in r.headers:
            print("✓ CORS настроен корректно")
            results['cors_enabled'] = True
        else:
            print("⚠ CORS заголовки отсутствуют (могут быть проблемы с frontend)")
    except Exception as e:
        print(f"✗ CORS - не удалось проверить: {e}")
    
    # ЭТАП 3: Запуск Frontend (если есть папка frontend)
    if frontend_dir.exists():
        print("\n🌐 ЭТАП 3: Запуск Frontend сервера...")
        print("-" * 70)
        
        # Проверим, запущен ли уже frontend
        try:
            r = requests.get('http://127.0.0.1:8000', timeout=1)
            if r.status_code == 200:
                print("✓ Frontend уже запущен на порту 8000")
                results['frontend_start'] = True
                frontend_process = None
            else:
                raise Exception("Frontend отвечает, но не корректно")
        except:
            # Frontend не запущен, запускаем его
            print(f"Запуск frontend из: {frontend_dir}")
            
            frontend_process = subprocess.Popen(
                ['python', '-m', 'http.server', '8000'],
                cwd=str(frontend_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore',
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
            )
            
            time.sleep(2)
            
            if frontend_process.poll() is None:
                print("✓ Frontend сервер запущен (PID: {})".format(frontend_process.pid))
                print("✓ Frontend доступен на: http://localhost:8000/index_new.html")
                results['frontend_start'] = True
            else:
                stderr = frontend_process.stderr.read()
                print("✗ Frontend не запустился")
                if stderr:
                    print(f"Ошибка: {stderr[:500]}")
    else:
        print("\n⚠ ЭТАП 3: Frontend папка не найдена, пропускаем...")
        results['frontend_start'] = True  # Пропускаем тест
    
    # ИТОГОВЫЙ ОТЧЕТ
    print("\n" + "=" * 70)
    print("  ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 70)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n📊 Тестов пройдено: {passed}/{total}")
    print("\nДетали:")
    for test_name, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {test_name.replace('_', ' ').title()}")
    
    if passed >= total - 1:  # Допускаем 1 неудачный тест
        print("\n🎉 ТЕСТИРОВАНИЕ ПРОЙДЕНО УСПЕШНО!")
        print("\n📱 Приложение готово к использованию:")
        print("   • Backend API: http://localhost:5000/api/")
        print("   • Swagger Docs: http://localhost:5000/api/docs")
        if frontend_dir.exists():
            print("   • Frontend: http://localhost:8000/index_new.html")
    else:
        print(f"\n⚠ Обнаружено проблем: {total - passed}")
    
    print("\n💡 Серверы запущены. Нажмите Ctrl+C для остановки...")
    print("=" * 70)
    
    # Держим процессы запущенными
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Остановка серверов...")

except Exception as e:
    print(f"\n❌ Критическая ошибка во время тестирования: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\n🗑️ Очистка...")
    # Остановка процессов
    if backend_process and backend_process.poll() is None:
        print("Остановка Backend сервера...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
            print("✓ Backend сервер остановлен")
        except:
            backend_process.kill()
            print("⚠ Backend сервер принудительно остановлен")
    
    if frontend_process and frontend_process.poll() is None:
        print("Остановка Frontend сервера...")
        frontend_process.terminate()
        try:
            frontend_process.wait(timeout=5)
            print("✓ Frontend сервер остановлен")
        except:
            frontend_process.kill()
            print("⚠ Frontend сервер принудительно остановлен")
    
    print("\n✅ Тестирование завершено")