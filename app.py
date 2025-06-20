from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        target_format = request.form.get("format", "jpg").lower()
        if target_format == "jpg":
            target_format_pillow = "JPEG"
        else:
            target_format_pillow = target_format.upper()

        if file and target_format:
            img = Image.open(file.stream)
            img = img.convert("RGB")
            filename = f"{uuid.uuid4()}.{target_format}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            img.save(filepath, format=target_format_pillow)
            return send_file(filepath, as_attachment=True)
    return render_template("index.html")