# server.py
# Web arayüzünü (telefon için) ve API uçlarını sağlayan Flask sunucusu.

import os
import socket
import io
import qrcode
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory

from commands import komutu_isle
from tts import sese_cevir
from config import FRIDAY_PIN, FLASK_PORT
from utils import kaynak_klasoru, veri_klasoru

_kaynak = kaynak_klasoru()
app = Flask(
    __name__,
    template_folder=os.path.join(_kaynak, "templates"),
    static_folder=os.path.join(_kaynak, "static"),
)


def yerel_ip_al() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def pin_dogru_mu() -> bool:
    if not FRIDAY_PIN:
        return True
    return request.headers.get("X-Friday-Pin") == FRIDAY_PIN


@app.route("/")
def anasayfa():
    return render_template("index.html", pin_gerekli=bool(FRIDAY_PIN))


@app.route("/api/command", methods=["POST"])
def api_command():
    if not pin_dogru_mu():
        return jsonify({"error": "Yanlış PIN"}), 401

    data = request.get_json(silent=True) or {}
    metin = data.get("text", "")
    cevap = komutu_isle(metin)
    ses_url = sese_cevir(cevap)
    return jsonify({"reply": cevap, "audio_url": ses_url})


@app.route("/audio/<dosya_adi>")
def ses_dosyasi(dosya_adi):
    return send_from_directory(veri_klasoru(), dosya_adi)


@app.route("/qr")
def qr_kod():
    ip = yerel_ip_al()
    url = f"http://{ip}:{FLASK_PORT}"
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/api/network-info")
def network_info():
    ip = yerel_ip_al()
    return jsonify({"url": f"http://{ip}:{FLASK_PORT}"})
