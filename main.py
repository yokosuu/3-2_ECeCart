import streamlit as st
import smtplib
from email.mime.text import MIMEText

# 商品情報の設定
products = [
    {"id": 1, "name": "商品1", "description": "説明1", "image": "https://via.placeholder.com/150"},
    {"id": 2, "name": "商品2", "description": "説明2", "image": "https://via.placeholder.com/150"},
    {"id": 3, "name": "商品3", "description": "説明3", "image": "https://via.placeholder.com/150"},
    {"id": 4, "name": "商品4", "description": "説明4", "image": "https://via.placeholder.com/150"},
    {"id": 5, "name": "商品5", "description": "説明5", "image": "https://via.placeholder.com/150"},
    {"id": 6, "name": "商品6", "description": "説明6", "image": "https://via.placeholder.com/150"},
    {"id": 7, "name": "商品7", "description": "説明7", "image": "https://via.placeholder.com/150"},
    {"id": 8, "name": "商品8", "description": "説明8", "image": "https://via.placeholder.com/150"},
    {"id": 9, "name": "商品9", "description": "説明9", "image": "https://via.placeholder.com/150"},
]

# カート情報を保持
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# ページタイトル
st.title("口八商店")

# 商品の表示
cols = st.columns(3)
for i, product in enumerate(products):
    with cols[i % 3]:
        st.image(product["image"])
        st.write(f"商品No: {product['id']}")
        st.write(product["description"])
        if st.button(f"カートに追加 - {product['name']}", key=product['id']):
            st.session_state['cart'].append(product)
            st.success(f"{product['name']} をカートに追加しました")

# カートに進むボタン
if st.button("カートを見る"):
    st.write("カートの中身：")
    for item in st.session_state['cart']:
        st.write(f"{item['name']} - {item['description']}")

    # 備考の入力
    notes = st.text_area("備考を入力してください")

    # メール送信
    if st.button("注文を送信"):
        cart_details = "\n".join([f"{item['name']} - {item['description']}" for item in st.session_state['cart']])
        message = f"注文内容:\n{cart_details}\n\n備考:\n{notes}"

        msg = MIMEText(message)
        msg['Subject'] = "注文内容"
        msg['From'] = "your_email@example.com"
        msg['To'] = "recipient_email@example.com"

        # メール送信処理（SMTP設定が必要です）
        try:
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login("your_email@example.com", "your_password")
                server.send_message(msg)
                st.success("注文が送信されました")
        except Exception as e:
            st.error(f"メール送信に失敗しました: {e}")
