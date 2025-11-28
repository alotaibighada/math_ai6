import streamlit as st
from sympy import symbols, Eq, solve, simplify, sympify
import re

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
.step-box {background-color: rgba(0,0,200,0.2); padding:10px; border-radius:10px; font-size:1.2em; margin-bottom:5px;}
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
# حل المعادلات مع خطوات
# -----------------------------
st.header("حل المعادلات خطوة بخطوة")
user_input = st.text_input("اكتب معادلة (مثال: 2*x+5=15 أو 2x*8)")

def fix_implied_multiplication(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)  # 2x -> 2*x
    expr = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr)  # xy -> x*y
    return expr

def solve_with_steps(eq_text):
    steps = []
    fixed_input = fix_implied_multiplication(eq_text)
    if "=" in fixed_input:
        left, right = fixed_input.split("=", maxsplit=1)
        left_expr = sympify(left.strip())
        right_expr = sympify(right.strip())
        
        vars_in_eq = list(left_expr.free_symbols.union(right_expr.free_symbols))
        if vars_in_eq:
            eq = Eq(left_expr, right_expr)
            steps.append(f"المعادلة الأصلية: {eq_text}")
            # تبسيط الجانب الأيسر والأيمن
            left_s = simplify(left_expr)
            right_s = simplify(right_expr)
            steps.append(f"بعد التبسيط: {left_s} = {right_s}")
            # الحل
            sol = solve(eq, vars_in_eq)
            steps.append(f"الحل: {sol}")
            return steps
        else:
            if left_expr == right_expr:
                steps.append("المعادلة صحيحة ✅")
            else:
                steps.append("المعادلة خاطئة ❌")
            return steps
    else:
        # تعبير رياضي فقط
        result = sympify(fixed_input).evalf()
        steps.append(f"نتيجة التعبير: {result}")
        return steps

if user_input:
    try:
        steps = solve_with_steps(user_input)
        for s in steps:
            st.markdown(f'<div class="step-box">{s}</div>', unsafe_allow_html=True)
        st.session_state.history.append(f"{user_input} = {steps[-1]}")
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
