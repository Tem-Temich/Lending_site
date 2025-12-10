#!/usr/bin/env python3
"""
Простой HTTP сервер для отображения страницы contacts.html
Использует только встроенные библиотеки Python
"""

import http.server
import socketserver
import os
from urllib.parse import urlparse

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Кастомный обработчик запросов"""

    def __init__(self, *args, **kwargs):
        # Устанавливаем базовую директорию для сервера
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        """Обработка GET запросов"""
        # Парсим URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Главная страница - показываем contacts.html
        if path == '/' or path == '':
            self.path = '/contacts.html'

        # Вызываем стандартный обработчик
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        """Переопределяем логирование для более читаемого вывода"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server():
    """Запуск HTTP сервера"""
    # Меняем рабочую директорию на директорию скрипта
    os.chdir(BASE_DIR)

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print("=" * 60)
        print(f"Сервер запущен на http://127.0.0.1:{PORT}")
        print(f"Откройте браузер и перейдите по адресу: http://127.0.0.1:{PORT}")
        print(f"Для остановки сервера нажмите Ctrl+C")
        print("=" * 60)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nСервер остановлен.")
            httpd.shutdown()


if __name__ == '__main__':
    run_server()


