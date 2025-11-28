import streamlit as st
from sympy import symbols, Eq, solve, sympify

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# -----------------------------
# الخلفية الثابتة + CSS
# -----------------------------
css = """
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1470&q=80");
    background-size: cover;
    background-attachment: fixed;
}
.stNumberInput>div>div>input,
.stTextInput>div>div>input {
    background: rgba(255,255,255,0.95) !important;
    color: black !important;
    font-size: 1.6em;
    font-weight: bold;
    padding: 0.6em;
    border-radius: 12px;
    border: 1px solid #555;
    text-align: center;
}
.stButton>button {
    height: 3.5em;
    width: 100%;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    font-size: 1.3em;
    background-color: rgba(0, 123, 255, 0.9) !important;
    color: white !important;
}
.stMarkdown, .stHeader, .stSubheader {
    background: rgba(0,0,0,0.5);
    padding: 8px 12px;
    border-radius: 10px;
    color: white !important;
    font-size: 1.6em;
    font-weight: bold;
    text-shadow: 2px 2px 3px black;
}
.stAlert {
    font-size: 1.8em !important;
    font-weight: bold !important;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# -----------------------------
# العنوان
# -----------------------------
st.title("🧮 Math AI – المساعد الرياضي الذكي")
st.markdown("أدخل الأرقام أو المعادلة واختر العملية لنقوم بالحساب أو الحل.")

# -----------------------------
# session_state
# -----------------------------
if "num1" not in st.session_state:
    st.session_state.num1 = 0
if "num2" not in st.session_state:
    st.session_state.num2 = 0
if "equation_input" not in st.session_state:
    st.session_state.equation_input = ""
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# دوال التحكم
# -----------------------------
def reset_inputs():
    st.session_state.num1 = 0
    st.session_state.num2 = 0
    st.session_state.equation_
