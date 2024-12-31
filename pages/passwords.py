import streamlit as st
from password_generator import password_generate
import time
import pandas as pd
import os
from streamlit_js_eval import streamlit_js_eval
from cryptography.fernet import Fernet
import numpy as np

st.set_page_config(
    layout="wide"
)

st.title("Şifreleriniz")
st.divider()

# Şifreleme anahtarını saklamak veya yüklemek için bir fonksiyon
def load_key():
    key_file = "key.key"
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
    else:
        with open(key_file, "rb") as file:
            key = file.read()
    return key

# Şifreyi şifrelemek için bir fonksiyon
def encrypt_password(key, password):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()

# Şifreyi çözmek için bir fonksiyon
def decrypt_password(key, encrypted_password):
    fernet = Fernet(key)
    try:
        return fernet.decrypt(encrypted_password.encode()).decode()
    except:
        return encrypted_password

# Şifrelerin saklanacağı dosyayı kontrol et ve yükle
file_path = "passwords.csv"
key = load_key()

if os.path.exists(file_path): 
    passwords = pd.read_csv(file_path)
    if "Password" in passwords.columns: 
        passwords['Password'] = passwords['Password'].apply(lambda x: decrypt_password(key, x))
    else:
        passwords = pd.DataFrame(columns=["No", "Platform", "Email", "Password", "Strength"])
else:
    passwords = pd.DataFrame(columns=["No", "Platform", "Email", "Password", "Strength"])

# Tablo başlıklarını tanımlama
fields = ["No", "Platform", "Mail", "Şifre", "Şifre Gücü"]

# Başlıkları sütunlara yerleştirme
colms = st.columns((1, 2, 2, 2, 2))
for col, field_name in zip(colms, fields):
    col.write(f"**{field_name}**")

# Tablodaki her satır için içerik oluşturma
for x, row in passwords.iterrows():
    col1, col2, col3, col4, col5 = st.columns((1, 2, 2, 2, 2))
    col1.write(row["No"])
    col2.write(row["Platform"])
    col3.write(row["Email"])
    col4.write(row["Password"])
    col5.write(row["Strength"])

if passwords['No'].isna().all() or passwords['No'].max() == np.nan:
    st.error("Şifrelerinizi görebilmek için lütfen yeni bir şifre oluşturun!") 

st.divider()


# Şifre gücünü hesaplayan bir fonksiyon
def calculate_strength(password):
    length = len(password)  # Şifrenin uzunluğu
    has_upper = any(char.isupper() for char in password)  # Büyük harf kontrolü
    has_lower = any(char.islower() for char in password)  # Küçük harf kontrolü
    has_digit = any(char.isdigit() for char in password)  # Rakam kontrolü
    has_special = any(not char.isalnum() for char in password)  # Özel karakter kontrolü
    strength = sum([has_upper, has_lower, has_digit, has_special])  # Güç kriterlerinin toplamı
    if length >= 8 and strength >= 3:
        return "Güçlü"
    elif length >= 6 and strength >= 2:
        return "Orta"
    else:
        return "Zayıf"

    


# Yeni şifre eklemek için bir genişletilebilir bölüm
with st.expander("### Yeni Şifre Ekle"):
    with st.form("add_password"):
        platform = st.text_input("Platform")
        email = st.text_input("Mail")
        password = st.text_input("Şifre")
        # submit_button = st.form_submit_button("Ekle")
        col_save, col_delete, password2,free,free,free = st.columns((1,3,3,5,6,6))
        submit_button = col_save.form_submit_button("Ekle")
        generate_password = col_delete.form_submit_button("Otomatik Şifre Yarat")


        sifre = ""
        if generate_password:
            sifre = ""
            sifre = password_generate()
            

        st.markdown("""
        <style>
        .big-font {
            font-size:25px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        password2.markdown(f'<p class="big-font">{sifre}</p>', unsafe_allow_html=True)

        if submit_button:
            if isinstance(password, str) and password:
                strength = calculate_strength(password)
                if passwords['No'].isna().all() or passwords['No'].max() == np.nan:
                    new_entry = {  # Yeni bir giriş oluştur
                        "No": 1,
                        "Platform": platform,
                        "Email": email,
                        "Password": password,
                        "Strength": strength
                    }
                else:
                    new_entry = {  # Yeni bir giriş oluştur
                        "No": passwords['No'].max() + 1,
                        "Platform": platform,
                        "Email": email,
                        "Password": password,
                        "Strength": strength
                    }

                if platform == "":
                    st.error("Lütfen bir platform giriniz!")
                elif email == "":
                    st.error("Lütfen bir mail giriniz!")
                elif password == "":
                    st.error("Lütfen bir şifre giriniz!")
                else:
                    passwords = pd.concat([passwords, pd.DataFrame([new_entry])], ignore_index=True)
                    passwords['Password'] = passwords['Password'].apply(lambda x: encrypt_password(key, x))
                    passwords.to_csv(file_path, index=False)
                    st.success("Şifre başarıyla kaydedildi!")
                    time.sleep(0.5)
                    streamlit_js_eval(js_expressions="parent.window.location.reload()")
            else:
                st.error("Lütfen geçerli bir şifre girin!")  # Hata mesajı

# Şifre silmek için bir genişletilebilir bölüm
with st.expander("### Şifre Sil"):
    delete_no = st.number_input("Silmek istediğiniz No değerini girin:", min_value=1, step=1)

    if st.button("Sil"):
        if delete_no in passwords['No'].values:
            passwords = passwords[passwords['No'] != delete_no] 
            passwords['Password'] = passwords['Password'].apply(lambda x: encrypt_password(key, x))
            passwords.to_csv(file_path, index=False)
            st.success(f"No {delete_no} başarıyla silindi!")
            time.sleep(0.5)
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
        else:
            st.error(f"No {delete_no} bulunamadı.")

# Çıkış yapma fonksiyonu
def logout():
    st.session_state.logged_in = False 
    st.info("Başarıyla çıkış yapıldı!")
    time.sleep(0.5)
    st.switch_page("Login.py")

# Çıkış butonu
def logout():
    st.session_state.logged_in = False 
    st.info("Başarıyla çıkış yapıldı!")
    time.sleep(0.5)
    st.switch_page("Login.py")

if st.button("Çıkış"):
    logout()
