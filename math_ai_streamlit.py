import streamlit as st
from sympy import symbols, Eq, solve, sympify
import base64

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# -----------------------------
# الخلفية الثابتة
# -----------------------------
def get_base64_of_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ضع هنا مسار الصورة الثابتة على جهازك
image_base64 = get_base64_of_image("/mnt/data/981b2b7c-e131-45d6-b564-13dd47cd7442.png")

st.markdown(f'''
<style>
.stApp {{
    background-image: url("data:image/png;base64,{image_base64}");
    background-size: cover;
    background-attachment: fixed;
}}
.stNumberInput>div>div>input, .stTextInput>div>div>input {{
    background: rgba(255,255,255,0.85);
    color: black;
    font-size: 1.3em;
    padding: 0.5em;
    border-radius: 6px;
    border: 1px solid #aaa;
    text-align: center;
}}
.stButton>button {{
    height: 3em;
    width: 100%;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    font-size: 1.1em;
}}
.stMarkdown, .stHeader, .stSubheader {{
    color: white;
    text-shadow: 1px 1px 2px black;
}}
</style>
''', unsafe_allow_html=True)

# -----------------------------
# باقي الكود كما هو
# -----------------------------
st.title("🧮 Math AI – المساعد الرياضي الذكي")
st.markdown("أدخل الأرقام أو المعادلة واختر العملية لنقوم بالحساب أو الحل.")

# session_state
if "num1" not in st.session_state:
    st.session_state.num1 = 0
if "num2" not in st.session_state:
    st.session_state.num2 = 0
if "equation_input" not in st.session_state:
    st.session_state.equation_input = ""
if "history" not in st.session_state:
    st.session_state.history = []

# دوال التحكم
def reset_inputs():
    st.session_state.num1 = 0
    st.session_sta_
