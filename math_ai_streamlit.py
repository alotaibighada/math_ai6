import streamlit as st
from sympy import symbols, Eq, solve, sympify
import base64

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# -----------------------------
# رفع الصورة من المستخدم
# -----------------------------
uploaded_bg = st.file_uploader("اختر صورة خلفية", type=["png", "jpg", "jpeg"])

def get_base64_of_image(image_file):
    data = image_file.read()
    return base64.b64encode(data).decode()

if uploaded_bg:
    image_base64 = get_base64_of_image(uploaded_bg)
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{image_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# تنسيق الإدخالات والأزرار
# -----------------------------
st.markdown("""
<style>
.stNumberInput>div>div>input, .stTextInput>div>div>input {
    background: rgba(255,255,255,0.85);
    color: black;
    font-size: 1.3em;
    padding: 0.5em;
    border-radius: 6px;
    border: 1px solid #aaa;
    text-align: center;
}
.stButton>button {
    height: 3em;
    width: 100%;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    font-size: 1.1em;
}
.stMarkdown, .stHeader, .stSubheader {
    color: white;
    text-shadow: 1px 1px 2px black;
}
