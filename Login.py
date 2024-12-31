import streamlit as st
from time import sleep

st.title("Şifre yöneticisine hoş geldiniz!")

st.write("Şifre yöneticisine giriş yapmak için lütfen kullanıcı adınızı ve şifrenizi giriniz.")

username = st.text_input("Kullanıcı adı")
password = st.text_input("Şifre", type="password")

if st.button("Oturum Aç", type="primary"):
    if username == "test" and password == "test":
        st.session_state.logged_in = True
        st.success("Başarıyla giriş yapıldı!")
        sleep(0.5)
        st.switch_page("pages/passwords.py")
    else:
        st.error("Yanlış şifre veya kullanıcı adı")

