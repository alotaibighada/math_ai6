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
st.markdown("أدخل الأرقام أو المعادلة واختر العملية لنقوم بالحساب أو الحل")

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
    st.markdown("** الرقم الأول**", unsafe_allow_html=True)
    st.session_state.num1 = st.number_input("", value=st.session_state.num1, key="num1_input")

with col2:
    st.markdown("** الرقم الثاني**", unsafe_allow_html=True)
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
            st.error("❌ لا يمكن القسمة على صفر")
            result = None
        else:
            result = num1 / num2
            symbol = "÷"

    if result is not None:
        st.success(f"✅ {num1} {symbol} {num2} = {result}")
        st.session_state.history.append(f"{num1} {symbol} {num2} = {result}")

# -----------------------------
# حل المعادلات
# -----------------------------
st.header("حل المعادلات")
user_input = st.text_input(
    "اكتب معادلة ( 2*x + 5 = 15 :مثال )",
    value=st.session_state.equation_input,
    key="equation_input"
)

x = symbols("x")

if user_input:
    try:
        if "=" in user_input:
            left, right = user_input.split("=", maxsplit=1)
            eq = Eq(sympify(left.strip()), sympify(right.strip()))
            sol = solve(eq, x)
            st.success(f"✅ حل المعادلة: {sol}")
            st.session_state.history.append(f"{user_input} = {sol}")
        else:
            result = sympify(user_input).evalf()
            st.success(f"نتيجة التعبير: {result}")
            st.session_state.history.append(f"{user_input} = {result}")
    except Exception as e:
        st.error(f"❌ خطأ في المعادلة: {e}")

# -----------------------------
# سجل العمليات السابقة
# -----------------------------
if st.session_state.history:
    st.subheader("📜 السجل")
    for i, item in enumerate(reversed(st.session_state.history), 1):
        st.write(f"{i}. {item}")

# -----------------------------
# أزرار التحكم
# -----------------------------
st.subheader("أزرار التحكم")
col_reset, col_clear = st.columns(2)
col_reset.button("🔄 إعادة التعيين", on_click=reset_inputs)
col_clear.button("🗑️ مسح السجل", on_click=clear_history)


