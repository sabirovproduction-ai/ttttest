from datetime import datetime
import os
from flask import Flask, request, send_file, abort

app = Flask(__name__)


@app.route("/<filename>.jpg")
def serve_photo(filename):
  # Проверяем, что имя файла состоит только из безопасных символов (защита от взлома через ../)
  # Разрешаем только буквы, цифры, дефисы и нижние подчеркивания
  if not filename.isalnum() and "_" not in filename and "-" not in filename:
    abort(400, description="Invalid filename")

  # Определяем IP с учетом прокси хостинга
  user_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(
      ","
  )[0]
  current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # Сохраняем информацию в лог с указанием запрошенного файла
  log_path = os.path.join(app.root_path, "log.txt")
  with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"[{current_time}] IP: {user_ip} requested {filename}.jpg\n")

  # Ищем запрошенный файл в папке проекта
  image_filename = f"{filename}.jpg"
  image_path = os.path.join(app.root_path, image_filename)

  # Если файл не найден — возвращаем ошибку 404
  if not os.path.exists(image_path):
    abort(404)

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
