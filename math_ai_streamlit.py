import streamlit as st
from sympy import symbols, Eq, solve, sympify

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# -----------------------------
# الخلفية الثابتة
# -----------------------------
background_url = "https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1470&q=80"

st.markdown(f'''
<style>
.stApp {{
    background-image: url("{background_url}");
    background-size: cover;
    background-attachment: fixed;
}}
/* تحسين وضوح الحقول */
.stNumberInput>div>div>input, .stTextInput>div>div>input {{
    background: rgba(255,255,255,0.9);
    color: black;
    font-size: 1.3em;
    padding: 0.5em;
    border-radius: 8px;
    border: 1px solid #555;
    text-align: center;
}}
.stButton>button {{
    height: 3em;
    width: 100%;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    font-size: 1.1em;
    background-color: rgba(0, 123, 255, 0.8);
    color: white;
}}
.stMarkdown, .stHeader, .stSubheader {{
    color: white;
    text-shadow: 2px 2px 4px black;
}}
</style>
''', unsafe_allow_html=True)

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
    st
