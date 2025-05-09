import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import string

# === Cấu hình CAPTCHA và mô hình ===
CAPTCHA_URL = "https://thanhtoanhocphi.epu.edu.vn/WebCommon/GetCaptcha"
CAPTCHA_SIZE = (110, 35)  # Nhớ khớp với mô hình bạn đã huấn luyện
CHARACTERS = string.digits + string.ascii_uppercase
LABEL_TO_CHAR = {i: c for i, c in enumerate(CHARACTERS)}

model = load_model("captcha_model.h5")

headers = {
    "authority": "thanhtoanhocphi.epu.edu.vn",
    "method": "GET",
    "path": "/WebCommon/GetCaptcha",
    "scheme": "https",
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "cookie": "cf_clearance=LOkjTJC7LrpcF3yyQ6QpM2uST0.V1VUcTIRU9SivMiA-1729311266-1.2.1.1-ypOEhnbHLm.842OgsrHRCoc7LZVD8nCG57yAXW797EJbINm8nutauFDTSCoEI8lPPTN3ktBMaP85KxsWf5634CqTHvt_N8BcnOh4qVCjUIuCxOUpGX86YNrXHJt_QfZSqY5wLYoob_ko8yxD1m3_ikj1uXqCAQhFl_kkrSAhkBJc_peK7r1EeCj2GsZl89xh1AlqdoKQcJv0E.heqH5Tc44vkUyLPwt8jvGVDX2tIG3CMELdingaEZ0zXV8u3nmfWtLjl3b2NVafqIuZ2hFV6ntwaPwiWJpyRgZSWmdORNYEwD70XqkhHE6QsoBKIrkwVaoOWt7a0DzmbHxplao9GEwKqajhsl6hr3E0PhsjmWJwHaYGIBO7ArEL.ADSanTP4UUe__N5K4zt1yx.kfK8ow; ASP.NET_SessionId=cnu1vpnesqfz5pqq2ix1m4de; __RequestVerificationToken=CJ09cvZVKxLSLntqQaE5ZTVSJ6EtT_yUTw1dlIhy-3_2bEdvD3Lsr55GSTNpibmJHicB5ehVY1urkpMg8zr6XungUXFKXVSwPahLkaQyT7A1; PAVWs3tE769MuloUJ81Y=cey6cWM9Y80IlVZ_9dnJu-ushWfxy7zEQEtlvOt21qY",  # <-- Thay cookie thật của bạn
    "priority": "u=2, i",
    "referer": "https://thanhtoanhocphi.epu.edu.vn/sinh-vien-dang-nhap.html",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Connection": "keep-alive"
}

# === Giao diện chính ===
class CaptchaTester:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR CAPTCHA Tester")
        self.session = requests.Session()

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.result_var = tk.StringVar()
        ttk.Label(root, text="Kết quả OCR:").pack()
        self.result_entry = ttk.Entry(root, textvariable=self.result_var, font=("Arial", 16), justify='center', width=15)
        self.result_entry.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Tải lại CAPTCHA", command=self.load_captcha).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Nhận diện", command=self.predict_captcha).pack(side='left', padx=10)

        self.current_image_data = None
        self.load_captcha()

    def load_captcha(self):
        try:
            response = self.session.get(CAPTCHA_URL, headers=headers, timeout=10)
            response.raise_for_status()

            self.current_image_data = response.content
            image = Image.open(io.BytesIO(self.current_image_data))
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
            self.result_var.set("")
        except Exception as e:
            self.result_var.set(f"Lỗi tải CAPTCHA: {e}")

    def predict_captcha(self):
        if not self.current_image_data:
            self.result_var.set("Chưa có ảnh!")
            return
        try:
            # Convert ảnh từ bytes sang grayscale array
            image = Image.open(io.BytesIO(self.current_image_data)).convert("L")
            image = image.resize(CAPTCHA_SIZE)
            img_array = np.array(image) / 255.0
            img_array = img_array.reshape(1, CAPTCHA_SIZE[1], CAPTCHA_SIZE[0], 1)

            preds = model.predict(img_array)
            result = ''.join([LABEL_TO_CHAR[np.argmax(p)] for p in preds])
            self.result_var.set(result)
        except Exception as e:
            self.result_var.set(f"Lỗi nhận diện: {e}")

# === Khởi chạy ===
if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaTester(root)
    root.mainloop()
