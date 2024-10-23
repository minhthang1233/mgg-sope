from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Hàm lấy mã giảm giá từ Shopee (giả định)
def get_coupon_codes(shopee_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    response = requests.get(shopee_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các mã giảm giá (giả định)
        coupon_elements = soup.find_all('div', class_='some-coupon-class')  # Cần sửa class phù hợp

        coupons = []
        for coupon in coupon_elements:
            coupon_code = coupon.text.strip()
            coupons.append(coupon_code)
        
        return coupons
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-coupons', methods=['POST'])
def get_coupons():
    shopee_url = request.form['url']
    coupons = get_coupon_codes(shopee_url)
    
    if coupons:
        return jsonify({'coupons': coupons})
    else:
        return jsonify({'error': 'Không tìm thấy mã giảm giá.'})

if __name__ == '__main__':
    app.run(debug=True)
