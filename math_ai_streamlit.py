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
.success-box {
    background-color: rgba(0, 200, 0, 0.3);
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 1.5em;
}
.error-box {
    background-color: rgba(200, 0, 0, 0.3);
    padding: 10px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 1.5em;
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
    st.session_state.equation_input = ""

def clear_history():
    st.session_state.history = []

# -----------------------------
# العمليات الحسابية
# -----------------------------
st.header("العمليات الحسابية")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🔢 الرقم الأول:**", unsafe_allow_html=True)
    st.session_state.num1 = st.number_input("", value=st.session_state.num1, key="num1_input")

with col2:
    st.markdown("**🔢 الرقم الثاني:**", unsafe_allow_html=True)
    st.session_state.num2 = st.number_input("", value=st.session_state.num2, key="num2_input")

col_op1, col_op2, col_op3, col_op4 = st.columns(4)
op_selected = None

if col_op1.button("جمع"):
    op_selected = "جمع"
if col_op2.button("طرح"):
    op_selected = "طرح"
if col_op3.button("ضرب"):
    op_selected = "ضرب"
if col_op4.button("قسمة"):
    op_selected = "قسمة"

if op_selected:
    num1 = st.session_state.num1
    num2 = st.session_state.num2

    if op_selected == "جمع":
        result = num1 + num2
        symbol = "+"
    elif op_selected == "طرح":
        result = num1 - num2
        symbol = "-"
    elif op_selected == "ضرب":
        result = num1 * num2
        symbol = "×"
    elif op_selected == "قسمة":
        if num2 == 0:
            st.markdown('<div class="error-box">❌ لا يمكن القسمة على صفر</div>', unsafe_allow_html=True)
            result = None
        else:
            result = num1 / num2
            symbol = "÷"

    if result is not None:
        st.markdown(f'<div class="success-box">✅ {num1} {symbol} {num2} = {result}</div>', unsafe_allow_html=True)
        st.session_state.history.append(f"{num1} {symbol} {num2} = {result}")

# -----------------------------
# حل أي معادلة
# -----------------------------
st.header("حل المعادلات")
user_inpu_
