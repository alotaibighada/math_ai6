import streamlit as st
from sympy import symbols, Eq, solve, sympify

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# CSS لتجميل الواجهة ووضع صورة كخلفية
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1610878180933-bec6d217f8f4?auto=format&fit=crop&w=1050&q=80");
    background-size: cover;
    background-attachment: fixed;
}
.stNumberInput>div>div>input, .stTextInput>div>div>input {
    background: rgba(255,255,255,0.85);
    color: black;
    font-size: 1.4em;
    padding: 0.6em;
    border-radius: 8px;
    border: 1px solid #aaa;
    text-align: center;
}
.stButton>button {
    height: 3.5em;
    width: 100%;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    font-size: 1.2em;
    cursor: pointer;
}
.stMarkdown, .stHeader, .stSubheader {
    color: white;
    text-shadow: 1px 1px 2px black;
}
</style>
""", unsafe_allow_html=True)

st.title("Math AI – المساعد الرياضي الذكي 🧮")
st.markdown("**العمليات الحسابية + حل المعادلات** في مكان واحد. أدخل الأرقام أو المعادلة وجرب الأزرار أدناه.")

# -----------------------------
# إعداد session_state
# -----------------------------
if 'history' not in st.session_state:
    st.session_state.history = []

if 'num1' not in st.session_state:
    st.session_state.num1 = 0
if 'num2' not in st.session_state:
    st.session_state.num2 = 0
if 'equation_input' not in st.session_state:
    st.session_state.equation_input = ""

# -----------------------------
# العمليات الحسابية
# -----------------------------
st.header("العمليات الحسابية")

col1, col2 = st.columns(2)
st.session_state.num1 = col1.number_input("الرقم الأول:", value=st.session_state.num1, key="num1_input")
st.session_state.num2 = col2.n_
