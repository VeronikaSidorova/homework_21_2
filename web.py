# Импорт встроенной библиотеки для работы веб-сервера
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8000  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """Метод для обработки входящих GET-запросов"""
        # Читаем содержимое файла contacts.html
        with open("contacts.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        self.send_response(200)  # Отправка кода ответа
        self.send_header(
            "Content-type", "text/html"
        )  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(html_content.encode("utf-8"))  # Тело ответа

    def do_POST(self):
        """Метод для обработки входящих POST-запросов"""
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        # Распарсим тело POST-запроса (обычно в формате application/x-www-form-urlencoded)
        parsed_data = urllib.parse.parse_qs(body)

        # Выводим все параметры
        print("Полученные данные от пользователя:")
        for key, values in parsed_data.items():
            for value in values:
                # Декодируем значение из bytes в str
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                print(f"{key}: {value}")
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
