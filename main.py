import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import os

SAVE_DIR = r"D:\traincaptcha\img"
CAPTCHA_URL = "https://thanhtoanhocphi.epu.edu.vn/WebCommon/GetCaptcha"

class CaptchaTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Train CAPTCHA Tool")

        # Sử dụng session để tăng tốc độ kết nối
        self.session = requests.Session()

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.input_entry = tk.Entry(root, font=("Arial", 14), justify='center')
        self.input_entry.pack(pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.done_button = tk.Button(button_frame, text="Done", width=10, command=self.save_and_next)
        self.done_button.grid(row=0, column=0, padx=5)

        self.reload_button = tk.Button(button_frame, text="Load lại", width=10, command=self.load_new_captcha)
        self.reload_button.grid(row=0, column=1, padx=5)

        self.current_image_data = None
        self.load_new_captcha()

    def load_new_captcha(self):
        try:
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

            response = self.session.get(CAPTCHA_URL, headers=headers, timeout=10)
            response.raise_for_status()

            self.current_image_data = response.content
            image = Image.open(io.BytesIO(self.current_image_data))
            self.tk_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.tk_image)
            self.input_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Lỗi khi tải CAPTCHA", f"{e}")

    def save_and_next(self):
        input_text = self.input_entry.get().strip()
        if not input_text:
            messagebox.showwarning("Chưa nhập CAPTCHA", "Vui lòng nhập CAPTCHA trước khi nhấn Done.")
            return

        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

        filename = os.path.join(SAVE_DIR, f"{input_text}.png")
        with open(filename, "wb") as f:
            f.write(self.current_image_data)

        self.load_new_captcha()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaTrainer(root)
    root.mainloop()
