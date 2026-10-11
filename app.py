import http.server
import socketserver
import os
from urllib.parse import parse_qs

PORT = 8000

ROUTES = {
    "/": "index.html",
    "/index": "index.html",
    "/catalog": "catalog.html",
    "/category": "category.html",
    "/contacts": "contacts.html",
}

def read_file(filename):
    # Чтение файла через контекстный менеджер
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        filename = ROUTES.get(self.path)
        if not filename:
            # Страница 404
            try:
                content = read_file("404.html")
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "Страница не найдена и 404.html отсутствует")
            return

        try:
            content = read_file(filename)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, f"Файл {filename} не найден")
        except Exception as e:
            # Страница 500
            try:
                content = read_file("500.html")
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except Exception:
                self.send_error(500, str(e))

    def do_POST(self):
        if self.path == "/contacts":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data_raw = self.rfile.read(content_length).decode("utf-8")
                post_data = parse_qs(post_data_raw)

                # Вывод в консоль
                print("Получен POST-запрос на /contacts. Данные:")
                for key, values in post_data.items():
                    print(f"  {key} = {values[0]}")

                response = """
                <html>
                  <head><title>Спасибо</title></head>
                  <body class="p-4">
                    <h1>Спасибо, ваше сообщение получено!</h1>
                    <p>Данные выведены в консоль сервера.</p>
                    <a href="/contacts">Вернуться на страницу контактов</a>
                  </body>
                </html>
                """
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(response.encode("utf-8"))
            except Exception as e:
                # В случае ошибки при POST — 500
                try:
                    content = read_file("500.html")
                    self.send_response(500)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(content.encode("utf-8"))
                except Exception:
                    self.send_error(500, str(e))
        else:
            self.send_error(405, "POST разрешён только для /contacts")

    def do_HEAD(self):
        self.send_response(405)
        self.end_headers()

if __name__ == "__main__":
    missing = []
    all_files = list(ROUTES.values()) + ["404.html", "500.html"]
    for filename in all_files:
        if not os.path.exists(filename):
            missing.append(filename)
    if missing:
        print(f"Ошибка: не найдены файлы: {', '.join(missing)}")
        print("Убедитесь, что они лежат в той же папке, что и app.py.")
    else:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"Сервер запущен на http://localhost:{PORT}")
            httpd.serve_forever()
