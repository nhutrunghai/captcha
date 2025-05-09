import cv2
import pytesseract
from PIL import Image
import numpy as np

# Đường dẫn ảnh CAPTCHA bạn muốn nhận dạng
image_path = "0DB2.png"  # ← sửa lại file bạn muốn thử

# Đọc ảnh gốc
image = cv2.imread(image_path)

# Tiền xử lý: chuyển sang ảnh xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Nhị phân hóa ảnh (làm rõ chữ)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Dùng morphology để loại nhiễu nhỏ
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# Lưu ảnh tạm nếu muốn xem
cv2.imwrite("processed.png", cleaned)

# OCR
text = pytesseract.image_to_string(cleaned, config='--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

print("Kết quả OCR:", text.strip())
