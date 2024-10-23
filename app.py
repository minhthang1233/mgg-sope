from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_coupon_codes(shopee_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    response = requests.get(shopee_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tìm các phần tử chứa mã giảm giá dựa trên class 'mini-vouchers__mask'
        coupon_elements = soup.find_all('div', class_='mini-vouchers__mask')

        coupons = []
        for coupon in coupon_elements:
            coupon_code = coupon.text.strip()
            coupons.append(coupon_code)
        
        if coupons:
            return coupons
        else:
            return ['Không tìm thấy mã giảm giá.']
    else:
        return ['Lỗi khi truy cập trang web.']

@app.route('/', methods=['GET', 'POST'])
def index():
    coupons = None
    if request.method == 'POST':
        shopee_url = request.form.get('url')
        coupons = get_coupon_codes(shopee_url)
    return render_template('index.html', coupons=coupons)

if __name__ == '__main__':
    app.run(debug=True)
