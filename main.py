import streamlit as st
import smtplib, ssl
import streamlit.components.v1 as stc
from email.mime.text import MIMEText
from pathlib import Path

##
gmailaccount = "********@gmail.com"
gmailpassword = "*******"

# 商品情報の設定
products = [
    {"id": 1, "name": "うぇぶぺーじ", "description": "今思えば優しい甘みが特徴のリキュール。", "image": "./img/item01.png"},
    {"id": 2, "name": "html", "description": "スクレイピングで再び出会った複雑な味わいのリキュール", "image": "./img/item02.png"},
    {"id": 3, "name": "えーぴーあい", "description": "複雑な香りと便利な旨味が広がる焼酎", "image": "./img/item03.png"},
    {"id": 4, "name": "すとりーむりっと", "description": "形になる楽しさ・軽やかな味わいの白ワイン。", "image": "./img/item04.png"},
    {"id": 5, "name": "でーびー", "description": "意外にわかりやすさを持つリキュール", "image": "./img/item05.png"},
    {"id": 6, "name": "ぎっと", "description": "よくわからないけどいつの間にか慣れるリキュール", "image": "./img/item06.png"},
    {"id": 7, "name": "ちーびる", "description": "みんなでの議論と分担が楽しい大人の部活動リキュール。", "image": "./img/item07.png"},
    {"id": 8, "name": "step3", "description": "つらたのしい香りが漂うワイン。", "image": "./img/item08.png"},
    {"id": 9, "name": "step4", "description": "つらたのしい味わいの吟醸酒。", "image": "./img/item09.png"},
]

# カート情報を保持
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# ページタイトル
st.title("すずき商店")

# 商品の表示
cols = st.columns(3)
for i, product in enumerate(products):
    with cols[i % 3]:
        # 画像を表示するためのパスを設定
        image_path = Path(product["image"])
        if image_path.exists():
            st.image(str(image_path))
        else:
            st.error(f"画像が見つかりません: {product['image']}")
        st.write(f"商品No: {product['id']}")
        st.write(product['name'])
        st.write(product["description"])
        quantity = st.selectbox(f"数量", range(1, 6), key=f"qty_{product['id']}")
        if st.button(f"カートに追加", key=product['id']):
            st.session_state['cart'].append({"product": product, "quantity": quantity})
            st.success(f"{product['name']} をカートに追加しました")

# カートに進むボタン
if st.button("カートを見る",type="primary",use_container_width=True):
    st.write("カートの中身：")
    for i, item in enumerate(st.session_state['cart']):
        st.write(f"{item['product']['name']} - {item['product']['description']} - 数量: {item['quantity']}")
        if st.button(f"削除 - {item['product']['name']}", key=f"remove_{i}"):
            st.session_state['cart'].pop(i)
            st.experimental_rerun()

    # ニックネームと備考の入力
    nickname = st.text_input("ニックネームを入力してください")
    notes = st.text_area("備考を入力してください")

    # メール送信
    if st.button("注文を送信",help="今回はメアドを抜いてあるので飛びません",type="primary",use_container_width=True):
        cart_details = "\n".join([f"{item['product']['name']} - {item['product']['description']} - 数量: {item['quantity']}" for item in st.session_state['cart']])
        message = f"注文内容:\n{cart_details}\n\nニックネーム:\n{nickname}\n\n備考:\n{notes}"

        msg = MIMEText(message)
        msg['Subject'] = "注文内容"
        msg['From'] = gmailaccount
        msg['To'] = gmailaccount

        # メール送信処理
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
                server.login(gmailaccount, gmailpassword)
                server.send_message(msg)
                st.success("注文が送信されました")
        except Exception as e:
            st.error(f"メール送信に失敗しました: {e}")
