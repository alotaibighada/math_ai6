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
    st.markdown(f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{image_base64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    ''', unsafe_allow_html=True)

# -----------------------------
# تنسيق الإدخالات والأزرار
# -----------------------------
st.markdown('''
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
    elif op_selecte_
