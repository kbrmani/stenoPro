from flask import Flask, render_template, request, send_file
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

d = {chr(i): i for i in range(255)}  
c = {i: chr(i) for i in range(255)}  

def encrypt_image(image_path, message, password):
    img = cv2.imread(image_path)
    n, m, z = 0, 0, 0

    
    for i in range(len(message)):
        img[n, m, z] = d[message[i]]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    
    img[n, m, z] = d["\0"]

    encrypted_path = os.path.join(ENCRYPTED_FOLDER, "encryptedImage.jpg")
    cv2.imwrite(encrypted_path, img)
    return encrypted_path

def decrypt_image(image_path, password):
    img = cv2.imread(image_path)
    n, m, z = 0, 0, 0
    message = ""

    while True:
        pixel_value = img[n, m, z]
        
       
        if pixel_value in c:
            char = c[pixel_value]
            if char == "\0":  
                break
            message += char
        else:
            print(f"Unexpected pixel value encountered: {pixel_value}")
            break 

        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    return message

@app.route("/", methods=["GET", "POST"])
def index():
    decrypted_message = None
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        password = request.form["password"]
        action = request.form["action"]

        if action == "encrypt":
            message = request.form["message"]
            encrypted_path = encrypt_image(image_path, message, password)
            return send_file(encrypted_path, as_attachment=True)

        elif action == "decrypt":
           
            decrypted_message = decrypt_image(image_path, password)

    return render_template("index.html", decrypted_message=decrypted_message)

if __name__ == "__main__":
    app.run(debug=True)
