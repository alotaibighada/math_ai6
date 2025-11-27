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
.op-buttons button {
    padding: 0.7em 1.2em;
    margin: 0.2em;
    border-radius: 8px;
    font-size: 1.2em;
    font-weight: bold;
    color: white;
    border: none;
    cursor: pointer;
}
.btn-add { background-color: #FF6F61; }
.btn-sub { background-color: #1E90FF; }
.btn-mul { background-color: #3CB371; }
.btn-div { background-color: #FFA500; }
</style>
""", unsafe_allow_html=True)

st.title("Math AI – المساعد الرياضي الذكي 🧮")
st.markdown("**قسم العمليات الحسابية:** اختر العملية عبر الأزرار، أو أدخل معادلة في الأسفل لحلها.")

# سجل العمليات السابقة
if 'history' not in st.session_state:
    st.session_state.history = []

# -----------------------------
# العمليات الحسابية
# -----------------------------
st.header("العمليات الحسابية")

col1, col2 = st.columns(2)
num1 = col1.number_input("الرقم الأول:", value=0)
num2 = col2.number_input("الرقم الثاني:", value=0)

col_op1, col_op2, col_op3, col_op4 = st.columns(4)
op_selected = None

if col_op1.button("جمع", key="add", help="جمع الرقمين"):
    op_selected = "جمع"
if col_op2.button("طرح", key="sub", help="طرح الرقمين"):
    op_selected = "طرح"
if col_op3.button("ضرب", key="mul", help="ضرب الرقمين"):
    op_selected = "ضرب"
if col_op4.button("قسمة", key="div", help="قسمة الرقمين"):
    op_selected = "قسمة"

if op_selected:
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
user_input = st.text_input("اكتب المعادلة (مثال: 2*x + 5 = 15)")

x = symbols('x')
if user_input:
    try:
        if '=' in user_input:
            lhs, rhs = user_input.split('=', maxsplit=1)
            equation = Eq(sympify(lhs.strip()), sympify(rhs.strip()))
            solution = solve(equation, x)
            st.success(f"✅ حل المعادلة: {solution}")
            st.session_state.history.append(f"{user_input} => {solution}")
        else:
            result = sympify(user_input).evalf()
            st.success(f"✅ الناتج: {result}")
            st.session_state.history.append(f"{user_input} = {result}")
    except Exception as e:
        st.error(f"❌ خطأ في المسألة: {e}")

# -----------------------------
# سجل العمليات وأزرار التحكم
# -----------------------------
if st.session_state.history:
    st.subheader("📜 سجل العمليات السابقة")
    for idx, item in enumerate(reversed(st.session_state.history), 1):
        st.write(f"{idx}. {item}")

col_reset, col_clear = st.columns(2)
if col_reset.button("🔄 إعادة تعيين الإدخالات"):
    st.experimental_rerun()
if col_clear.button("🗑️ مسح سجل النتائج"):
    st.session_state.history = []
    st.experimental_rerun()
