#!/usr/bin/env python3
"""
Простой запуск PC Club сервера
"""
import os
import sys
import subprocess
import time

def main():
    print("=" * 50)
    print("  Запуск PC Club CYBERARENA")
    print("=" * 50)
    
    # Путь к папке проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_dir, "backend", "app")
    
    print(f"📁 Проект: {project_dir}")
    print(f"📁 Backend: {backend_dir}")
    
    # Проверяем наличие main.py
    main_py = os.path.join(backend_dir, "main.py")
    if not os.path.exists(main_py):
        print(f"❌ Файл не найден: {main_py}")
        print("Создаем минимальную версию...")
        
        # Создаем минимальный main.py
        create_minimal_main(backend_dir)
    
    print("\n🚀 Запуск сервера...")
    print("📡 API будет доступен: http://localhost:5000")
    print("📋 Endpoints:")
    print("   • /api/health - проверка работы")
    print("   • /api/tariffs - тарифы")
    print("   • /api/computers - компьютеры")
    print("   • /api/bookings - бронирования")
    print("\n🛑 Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    # Запускаем сервер
    try:
        os.chdir(backend_dir)
        os.system("python main.py")
    except KeyboardInterrupt:
        print("\n\n✅ Сервер остановлен")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")

def create_minimal_main(backend_dir):
    """Создает минимальную версию main.py"""
    os.makedirs(backend_dir, exist_ok=True)
    
    minimal_main = '''from flask import Flask, jsonify
import json

app = Flask(__name__)

# Минимальный API для теста
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': 'PC Club API работает',
        'version': '1.0.0'
    })

@app.route('/api/tariffs', methods=['GET'])
def get_tariffs():
    tariffs = [
        {'id': 1, 'name': 'STANDARD', 'price_per_hour': 150, 'features': ['GTX 1660 Super', '16GB RAM']},
        {'id': 2, 'name': 'PRO', 'price_per_hour': 250, 'features': ['RTX 3070', '32GB RAM']},
        {'id': 3, 'name': 'VIP', 'price_per_hour': 400, 'features': ['RTX 4090', '64GB RAM']}
    ]
    return jsonify({'success': True, 'data': tariffs})

if __name__ == '__main__':
    print("🚀 Сервер запущен на http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
    
    main_path = os.path.join(backend_dir, "main.py")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write(minimal_main)
    
    print(f"✅ Создан файл: {main_path}")
    
    # Создаем requirements.txt
    req_path = os.path.join(backend_dir, "requirements.txt")
    with open(req_path, "w", encoding="utf-8") as f:
        f.write("Flask==2.3.3")
    
    print(f"✅ Создан файл: {req_path}")
    print("📦 Установите зависимости: pip install -r requirements.txt")

if __name__ == "__main__":
    main()