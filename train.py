import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import string

# Cấu hình
CAPTCHA_LENGTH = 4
CHARACTERS = string.digits + string.ascii_uppercase  # '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CHAR_TO_LABEL = {c: i for i, c in enumerate(CHARACTERS)}
LABEL_TO_CHAR = {i: c for c, i in CHAR_TO_LABEL.items()}
IMG_WIDTH = 110
IMG_HEIGHT = 35

# Đọc dữ liệu
def load_data(image_dir, labels_csv):
    df = pd.read_csv(labels_csv)
    X, y = [], []

    for _, row in df.iterrows():
        img_path = os.path.join(image_dir, row['filename'])
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
        image = image / 255.0
        X.append(image)

        label = row['label']
        label_encoded = [CHAR_TO_LABEL[c] for c in label]
        y.append(label_encoded)

    X = np.array(X).reshape(-1, IMG_HEIGHT, IMG_WIDTH, 1)
    y = np.array(y)
    return X, y

# One-hot encode label từng ký tự
def encode_labels(y):
    return [to_categorical(y[:, i], num_classes=len(CHARACTERS)) for i in range(CAPTCHA_LENGTH)]

# Build mô hình
def build_model():
    input_layer = layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)

    outputs = [layers.Dense(len(CHARACTERS), activation='softmax', name=f'char_{i}')(x) for i in range(CAPTCHA_LENGTH)]

    model = models.Model(inputs=input_layer, outputs=outputs)
    model.compile(
        loss=['categorical_crossentropy'] * CAPTCHA_LENGTH,
        optimizer='adam',
        metrics=['accuracy'] * CAPTCHA_LENGTH
    )
    return model

# Train
def train():
    X, y = load_data('img', 'labels.csv')
    y_split = encode_labels(y)

    # Tách dữ liệu cho từng phần của y (từng ký tự)
    X_train, X_val = train_test_split(X, test_size=0.1, random_state=42)
    y_train = []
    y_val = []

    for i in range(CAPTCHA_LENGTH):
        y_t, y_v = train_test_split(y_split[i], test_size=0.1, random_state=42)
        y_train.append(y_t)
        y_val.append(y_v)

    model = build_model()
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=30, batch_size=32)

    model.save("captcha_model.h5")
    print("✅ Mô hình đã được huấn luyện và lưu thành công.")
if __name__ == "__main__":
    train()
