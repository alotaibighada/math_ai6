import streamlit as st
from sympy import symbols, Eq, solve, sympify
import re  # لاستخدام التعابير النمطية

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI", layout="centered")

# -----------------------------
# CSS للخلفية والنصوص
# -----------------------------
st.markdown("""
<style>
.stApp { 
    background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1470&q=80");
    background-size: cover;
    background-attachment: fixed;
}
.stNumberInput>div>div>input,
.stTextInput>div>div>input {
    background: rgba(255,255,255,0.95) !important;
    font-size: 1.5em;
    font-weight: bold;
    text-align: center;
}
.stButton>button {
    height: 3em;
    font-size: 1.2em;
    font-weight: bold;
    border-radius: 10px;
}
.success-box {background-color: rgba(0,200,0,0.3); padding:10px; border-radius:10px; font-size:1.4em; font-weight:bold;}
.error-box {background-color: rgba(200,0,0,0.3); padding:10px; border-radius:10px; font-size:1.4em; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.title("🧮 Math AI – المساعد الرياضي")

# -----------------------------
# سجل العمليات
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# العمليات الحسابية
# -----------------------------
st.header("العمليات الحسابية")
col1, col2 = st.columns(2)
num1 = col1.number_input("🔢 الرقم الأول:", value=0)
num2 = col2.number_input("🔢 الرقم الثاني:", value=0)

col_op1, col_op2, col_op3, col_op4 = st.columns(4)
op_selected = None
if col_op1.button("جمع"): op_selected = "جمع"
if col_op2.button("طرح"): op_selected = "طرح"
if col_op3.button("ضرب"): op_selected = "ضرب"
if col_op4.button("قسمة"): op_selected = "قسمة"

if op_selected:
    try:
        if op_selected == "جمع": result = num1 + num2; symbol = "+"
        elif op_selected == "طرح": result = num1 - num2; symbol = "-"
        elif op_selected == "ضرب": result = num1 * num2; symbol = "×"
        elif op_selected == "قسمة":
            if num2 == 0:
                result = None
                st.markdown('<div class="error-box">❌ لا يمكن القسمة على صفر</div>', unsafe_allow_html=True)
            else:
                result = num1 / num2
                symbol = "÷"
        if result is not None:
            st.markdown(f'<div class="success-box">✅ {num1} {symbol} {num2} = {result}</div>', unsafe_allow_html=True)
            st.session_state.history.append(f"{num1} {symbol} {num2} = {result}")
    except Exception as e:
        st.markdown(f'<div class="error-box">❌ خطأ: {e}</div>', unsafe_allow_html=True)

# -----------------------------
# حل المعادلات مع تصحيح 2x -> 2*x
# -----------------------------
st.header("حل المعادلات")
user_input = st.text_input("اكتب معادلة (مثال: 2*x+5=15 أو 2x*8)")

def fix_implied_multiplication(expr):
    """
    يحول أي 2x أو 3y إلى 2*x و 3*y قبل تمريرها لـ sympify
    """
    # إضافة * بين رقم ومتغير (مثل 2x -> 2*x)
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    # إضافة * بين متغير ومتغير (مثل xy -> x*y)
    expr = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr)
    return expr

if user_input:
    try:
        fixed_input = fix_implied_multiplication(user_input)
        if "=" in fixed_input:
            left, right = fixed_input.split("=", maxsplit=1)
            left_expr = sympify(left.strip())
            right_expr = sympify(right.strip())
            
            vars_in_eq = list(left_expr.free_symbols.union(right_expr.free_symbols))
            if vars_in_eq:
                eq = Eq(left_expr, right_expr)
                sol = solve(eq, vars_in_eq)
                st.markdown(f'<div class="success-box">✅ حل المعادلة: {sol}</div>', unsafe_allow_html=True)
                st.session_state.history.append(f"{user_input} = {sol}")
            else:
                if left_expr == right_expr:
                    st.markdown('<div class="success-box">✅ المعادلة صحيحة</div>', unsafe_allow_html=True)
                    st.session_state.history.append(f"{user_input} = صحيحة")
                else:
                    st.markdown('<div class="error-box">❌ المعادلة خاطئة</div>', unsafe_allow_html=True)
                    st.session_state.history.append(f"{user_input} = خاطئة")
        else:
            # تعبير رياضي فقط بدون =
            result = sympify(fixed_input).evalf()
            st.markdown(f'<div class="success-box">✅ نتيجة التعبير: {result}</div>', unsafe_allow_html=True)
            st.session_state.history.append(f"{user_input} = {result}")
    except Exception as e:
        st.markdown(f'<div class="error-box">❌ خطأ في المعادلة: {e}</div>', unsafe_allow_html=True)

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
col_reset, col_clear = st.columns(2)
col_reset.button("🔄 إعادة التعيين", on_click=lambda: None)
col_clear.button("🗑️ مسح السجل", on_click=lambda: st.session_state.history.clear())
