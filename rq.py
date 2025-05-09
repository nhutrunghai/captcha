import requests
headers = {
    "authority": "thanhtoanhocphi.epu.edu.vn",
    "method": "GET",
    "path": "/WebCommon/GetCaptcha",
    "scheme": "https",
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "priority": "u=2, i",
    "referer": "https://thanhtoanhocphi.epu.edu.vn/sinh-vien-dang-nhap.html",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

response = requests.get('https://thanhtoanhocphi.epu.edu.vn/WebCommon/GetCaptcha', headers=headers)
print(response.status_code)