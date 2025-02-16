# Image Encryption & Decryption

This project is a simple **Image Encryption & Decryption** web application built using **Flask** and **OpenCV**. The application allows users to encrypt a secret message inside an image and decrypt it later using a passcode.

## Features

- Encrypt a message into an image
- Decrypt the message from the image using the correct passcode
- User-friendly web interface
- Uses OpenCV for image processing

## Technologies Used

- Python (Flask, OpenCV)
- HTML, CSS, JavaScript
- Bootstrap for UI design

## Installation & Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/stenoPro.git
   cd stenoPro
   ```

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```sh
   python app.py
   ```

4. Open your browser and go to:

   ```
   http://127.0.0.1:5000
   ```

## How It Works

### **Encryption Process**

1. Upload an image.
2. Enter a secret message and a passcode.
3. Click on **Encrypt & Download**.
4. The encrypted image is generated and downloaded.

### **Decryption Process**

1. Upload the encrypted image.
2. Enter the correct passcode.
3. Click on **Decrypt**.
4. The secret message is displayed.

## Screenshot

Below is a preview of the working application:
![Image Encryption   Decryption - Google Chrome 16-02-2025 20_00_07](https://github.com/user-attachments/assets/00bda95e-15b9-468e-af75-8dbe83ecdda3)

## Folder Structure

```
stenoPro/
│── static/
│── templates/
│   ├── index.html
│── app.py
│── requirements.txt
│── README.md
```

## Known Issues

- Entering the wrong passcode will display an error message.
- Large messages may not work properly due to image size limitations.

## License

This project is open-source and available under the MIT License.

## Author

Developed by **Manish Singh**. Feel free to contribute!

