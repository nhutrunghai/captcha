from tensorflow.keras.models import load_model
import numpy as np
import cv2
import string

# Load lại biến LABEL_TO_CHAR để giải mã
CHARACTERS = string.digits + string.ascii_uppercase
LABEL_TO_CHAR = {i: c for i, c in enumerate(CHARACTERS)}

model = load_model("captcha_model.h5")

def predict_image(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (110, 35))  # Phải khớp với kích thước huấn luyện
    image = image / 255.0
    image = image.reshape(1, 35, 110, 1)

    preds = model.predict(image)
    result = ''.join([LABEL_TO_CHAR[np.argmax(p)] for p in preds])
    return result

print(predict_image("2UW6.png"))
