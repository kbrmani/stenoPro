import cv2
import os
import numpy as np
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

    filepath = os.path.join(UPLOAD_FOLDER, "encrypted_" + file.filename)
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return "Invalid image format", 400

    # Store password hash and message length in the top-left pixel
    password_hash = hash(password) % 256
    msg_length = len(msg)

    img[0, 0, 0] = password_hash
    img[0, 0, 1] = msg_length // 256
    img[0, 0, 2] = msg_length % 256

    print(f"Password hash stored: {password_hash}")  # Debugging statement
    print(f"Message length stored: {msg_length}")  # Debugging statement

    n, m, z = 0, 1, 2  # Start from (0,1) to avoid the top-left pixel
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n += 1
        m += 1
        z = (z + 1) % 3

    cv2.imwrite(filepath, img)
    return send_file(filepath, as_attachment=True)

@app.route("/decrypt", methods=["POST"])
def decrypt():
    if "image" not in request.files or request.form["password"] == "":
        return "Error: Missing fields"

    # Read inputs
    image_file = request.files["image"]
    input_password = request.form["password"]

    image_path = os.path.join(UPLOAD_FOLDER, "to_decrypt_" + image_file.filename)
    image_file.save(image_path)  # Save uploaded encrypted image
    img = cv2.imread(image_path)

    if img is None:
        return "Error: Unable to read image."

    # Retrieve the stored password hash and message length
    stored_password_hash = int(img[0, 0, 0])
    msg_length = (int(img[0, 0, 1]) * 256) + int(img[0, 0, 2])

    print(f"Password hash retrieved: {stored_password_hash}")  # Debugging statement
    print(f"Message length retrieved: {msg_length}")  # Debugging statement

    # Check if the input password hash matches the stored password hash
    if stored_password_hash != (hash(input_password) % 256):
        return "Error: You are not authorized to decrypt this image."

    # Decrypt message
    message = ""
    n, m, z = 0, 1, 2  # Start from (0,1) to avoid the top-left pixel

    for _ in range(msg_length):
        if n < img.shape[0] and m < img.shape[1]:
            message += c[img[n, m, z]]
            n += 1
            m += 1
            z = (z + 1) % 3
        else:
            return "Error: Image size is too small to contain the full message."

    return message


if __name__ == "__main__":
    app.run(debug=True)
