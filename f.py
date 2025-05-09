import pytesseract
from PIL import Image

# (Tùy chọn) nếu cần chỉ định đường dẫn Tesseract:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Đọc ảnh sau khi xử lý
image = Image.open("processed.png")

# OCR
text = pytesseract.image_to_string(image, config='--psm 8 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

print("Kết quả OCR:", text.strip())
