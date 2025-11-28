import streamlit as st
from sympy import symbols, Eq, solve, sympify
import base64

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# -----------------------------
# دالة لتحويل الصورة إلى Base64
# -----------------------------
def get_base64_of_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -----------------------------
# تحويل الصورة التي أرسلتها
# -----------------------------
image_base64 = get_base64_of_image("981b2b7c-e131-45d6-b564-13dd47cd7442.png")

# -----------------------------
# الخلفية والتصميم
# -----------------------------
st.markdown(f"""
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
""", unsafe_allow_html=True)

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
# دوال الأزرار
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
st.session_state.num1 = col1.number_input("الرقم الأول:", value=st.session_state.num1, key="num1_input")
st.session_state.num2 = col2.number_input("الرقم الثاني:", value=st.session_state.num2, key="num2_input")

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
    "اكتب معادلة (مثال: 2*x + 5 = 15)",
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
