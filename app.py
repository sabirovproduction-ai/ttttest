from datetime import datetime
import os
from flask import Flask, request, send_file, abort

app = Flask(__name__)


# Перехватываем любой путь, заканчивающийся на .jpg
@app.route("/<path:filename>")
def serve_photo(filename):
  # Проверяем, что запрашиваемый файл действительно заканчивается на .jpg
  if not filename.lower().endswith(".jpg"):
    abort(404)

  # Определяем IP с учетом прокси хостинга
  user_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(
      ","
  )[0]
  current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # Сохраняем в лог информацию: какой именно URL запросили и чей IP
  log_path = os.path.join(app.root_path, "log.txt")
  with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"[{current_time}] IP: {user_ip} -> запрошен /{filename}\n")

  # Всегда отдаем один и тот же файл, который лежит в папке проекта
  image_path = os.path.join(app.root_path, "image.jpg")

  if not os.path.exists(image_path):
    return "Файл image.jpg не найден на сервере", 404

  return send_file(image_path, mimetype="image/jpeg")


@app.route("/log.txt")
def logtxt():
  file_path = os.path.join(app.root_path, "log.txt")
  if not os.path.exists(file_path):
    return "Log is empty", 404
  return send_file(file_path, mimetype="text/plain")


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
