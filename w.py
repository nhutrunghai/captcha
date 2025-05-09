import os
import pandas as pd

def create_labels_csv(image_dir, output_csv='labels.csv'):
    data = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            label = os.path.splitext(filename)[0]
            data.append({'filename': filename, 'label': label})

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"✅ File CSV đã được tạo tại: {output_csv} (từ {len(data)} ảnh)")

# Thay đường dẫn thư mục chứa ảnh CAPTCHA tại đây
create_labels_csv('D:\captcha\captcha\img')
