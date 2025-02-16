from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
ENCODED_FOLDER = "static/encoded"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCODED_FOLDER, exist_ok=True)

# ASCII Mapping for Encoding & Decoding
d = {chr(i): i for i in range(255)}
c = {i: chr(i) for i in range(255)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    if "image" not in request.files or request.form["message"] == "" or request.form["password"] == "":
        return "Error: Missing fields"

    # Read inputs
    image_file = request.files["image"]
    message = request.form["message"]
    password = request.form["password"]

    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    encoded_path = os.path.join(ENCODED_FOLDER, "encrypted_" + image_file.filename)

    image_file.save(image_path)  # Save the uploaded image
    img = cv2.imread(image_path)  # Read image using OpenCV

    if img is None:
        return "Error: Unable to read image."

    # Encrypt message length
    message_length = len(message)
    img[0, 0, 0] = message_length // 256
    img[0, 0, 1] = message_length % 256

    # Encrypt message into image
    n, m, z = 0, 1, 2  # Start from (0,1) to avoid length data
    for char in message:
        if n < img.shape[0] and m < img.shape[1]:
            img[n, m, z] = d[char]
            n += 1
            m += 1
            z = (z + 1) % 3

    cv2.imwrite(encoded_path, img)  # Save the encrypted image
    return send_file(encoded_path, as_attachment=True)


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

    # Read message length
    try:
        msg_length = (int(img[0, 0, 0]) * 256) + int(img[0, 0, 1])
    except IndexError:
        return "Error: Unable to read message length from image."

    # Decrypt message
    message = ""
    n, m, z = 0, 1, 2  # Start from (0,1) to avoid length data

    for _ in range(msg_length):  # Extract only the stored message length
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