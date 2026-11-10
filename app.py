import os
from datetime import datetime
from flask import Flask, request, send_file

app = Flask(__name__)


@app.route("/photo.jpg")
def serve_photo():
    # Определяем IP с учетом прокси хостинга
    user_ip = request.headers.get(
        "X-Forwarded-For", request.remote_addr
    ).split(",")[0]
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Сохраняем в лог
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{current_time}] IP: {user_ip}\n")

    return send_file("image.jpg", mimetype="image/jpeg")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
