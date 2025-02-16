import cv2
import os
import numpy as np
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

password_store = {}  # Dictionary to store passwords for images

d = {chr(i): i for i in range(255)}
c = {i: chr(i) for i in range(255)}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    msg = request.form["message"]
    password = request.form["password"]

    if file.filename == "":
        return "No selected file", 400

    filepath = os.path.join(UPLOAD_FOLDER, "encrypted.jpg")
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return "Invalid image format", 400

    # Store password for this image
    password_store[filepath] = password

    n, m, z = 0, 0, 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n += 1
        m += 1
        z = (z + 1) % 3

    cv2.imwrite(filepath, img)
    return send_file(filepath, as_attachment=True)

@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    input_password = request.form["password"]

    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return "Invalid image format", 400

    filepath = os.path.join(UPLOAD_FOLDER, "encrypted.jpg")

    # Check if password exists for this image
    if filepath not in password_store:
        return "YOU ARE NOT AUTHORIZED!", 403

    stored_password = password_store[filepath]

    # Validate password
    if input_password != stored_password:
        return "YOU ARE NOT AUTHORIZED!", 403

    n, m, z = 0, 0, 0
    message = ""

    for _ in range(255):  # Attempt to retrieve up to 255 characters
        char_code = img[n, m, z]
        if char_code == 0:
            break
        message += c[char_code]
        n += 1
        m += 1
        z = (z + 1) % 3

    return f"Decrypted Message: {message}"

if __name__ == "__main__":
    app.run(debug=True)
