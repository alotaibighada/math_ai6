import streamlit as st
from sympy import symbols, Eq, solve, sympify

# إعداد الصفحة
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# CSS لتجميل الواجهة
st.markdown("""
<style>
.stNumberInput>div>div>input, .stTextInput>div>div>input {
    background: rgba(240,240,240,1);
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
st.session_state.num2 = col2.number_input("الرقم الثاني:", value=st.session_state.num2, key="num2_input")

# أزرار العمليات الحسابية
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
    result = None
    symbol = ""
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
        if num2 != 0:
            result = num1 / num2
            symbol = "÷"
        else:
            st.error("❌ لا يمكن القسمة على صفر")
    if result is not None:
        st.success(f"✅ {num1} {symbol} {num2} = {result}")
        st.session_state.history.append(f"{num1} {symbol} {num2} = {result}")

# -----------------------------
# حل المعادلات
# -----------------------------
st.header("حل المعادلات البسيطة")
user_input = st.text_input("اكتب المعادلة (مثال: 2*x + 5 = 15)", value=st.session_state.equation_input, key="equation_input")

x = symbols('x')
if user_input:
    try:
        if '=' in user_input:
            lhs, rhs = user_input.split('=', maxsplit=1)
            equation = Eq(
