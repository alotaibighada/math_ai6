import streamlit as st
from sympy import symbols, Eq, solve, simplify, sympify, diff, integrate
import numpy as np
import matplotlib.pyplot as plt
import re
import easyocr
from PIL import Image

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI", layout="wide")

# -----------------------------
# CSS للواجهة
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
    font-size: 1.3em;
    font-weight: bold;
    text-align: center;
}
.stButton>button {
    height: 2.5em;
    font-size: 1.1em;
    font-weight: bold;
    border-radius: 10px;
}
.success-box {background-color: rgba(0,200,0,0.3); padding:10px; border-radius:10px; font-size:1.2em; font-weight:bold;}
.error-box {background-color: rgba(200,0,0,0.3); padding:10px; border-radius:10px; font-size:1.2em; font-weight:bold;}
.step-box {background-color: rgba(0,0,200,0.2); padding:10px; border-radius:10px; font-size:1.1em; margin-bottom:5px;}
.explain-box {background-color: rgba(255,255,0,0.3); padding:10px; border-radius:10px; font-size:1em; margin-bottom:5px;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# سجل العمليات
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# دالة تصحيح الضرب الضمني
# -----------------------------
def fix_all_implied_multiplication(expr):
    expr = expr.replace(" ", "")
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z\)])([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))(\d|\()', r'\1*\2', expr)
    return expr

# -----------------------------
# حل المعادلات خطوة بخطوة
# -----------------------------
x = symbols("x")
def solve_with_explanation(eq_text):
    steps = []
    if eq_text.count("=") > 1:
        return ["❌ صياغة المعادلة خاطئة: أكثر من علامة مساواة"]
    steps.append(f"المعادلة الأصلية: {eq_text}")
    
    fixed_input = fix_all_implied_multiplication(eq_text)
    if fixed_input != eq_text:
        steps.append(f"🔧 بعد تصحيح الضرب الضمني: {fixed_input}")
    
    try:
        if "=" in fixed_input:
            left, right = fixed_input.split("=", maxsplit=1)
            left_expr = sympify(left.strip())
            right_expr = sympify(right.strip())
            
            vars_in_eq = list(left_expr.free_symbols.union(right_expr.free_symbols))
            if vars_in_eq:
                eq = Eq(left_expr, right_expr)
                steps.append(f"📐 بعد التبسيط: {simplify(left_expr)} = {simplify(right_expr)}")
                
                sol = solve(eq, vars_in_eq)
                steps.append(f"✅ الحل النهائي: {sol}")
                steps.append(f"💡 تفسير: تم تبسيط ونقل الحدود للحصول على قيمة المتغير.")
            else:
                if left_expr == right_expr:
                    steps.append("✅ المعادلة صحيحة، لا يوجد متغير.")
                else:
                    steps.append("❌ المعادلة خاطئة، لا يوجد متغير ولكن الطرفين غير متساويين.")
        else:
            result = sympify(fixed_input).evalf()
            steps.append(f"📊 نتيجة التعبير الرياضي: {result}")
        return steps
    except:
        return ["❌ صياغة المعادلة خاطئة"]

# -----------------------------
# تبويبات التطبيق
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧮 عمليات", "📐 معادلات", "🟩 مصفوفات", "∂ تفاضل/∫ تكامل", "📷 مسح ضوئي"])

# -----------------------------
# Tab 1: العمليات الحسابية
# -----------------------------
with tab1:
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
# Tab 2: حل المعادلات
# -----------------------------
with tab2:
    st.header("حل المعادلات خطوة بخطوة")
    user_input = st.text_input("اكتب معادلة (مثال: 2*x+5=15 أو 2x*8)")
    if user_input:
        steps = solve_with_explanation(user_input)
        for s in steps:
            if "❌" in s:
                st.markdown(f'<div class="error-box">{s}</div>', unsafe_allow_html=True)
            elif "💡" in s or "🔧" in s or "📐" in s or "📊" in s:
                st.markdown(f'<div class="explain-box">{s}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step-box">{s}</div>', unsafe_allow_html=True)
        st.session_state.history.append(f"{user_input} = {steps[-1]}")

# -----------------------------
# Tab 3: المصفوفات
# -----------------------------
with tab3:
    st.header("عمليات المصفوفات")
    st.markdown("أدخل المصفوفات كقائمة من القوائم. مثال: [[1,2],[3,4]]")
    mat1_text = st.text_area("المصفوفة الأولى:", "[[1,2],[3,4]]")
    mat2_text = st.text_area("المصفوفة الثانية:", "[[5,6],[7,8]]")
    
    col_add, col_sub, col_mul, col_det = st.columns(4)
    try:
        mat1 = np.array(eval(mat1_text))
        mat2 = np.array(eval(mat2_text))
    except:
        st.markdown('<div class="error-box">❌ خطأ في صياغة المصفوفة</div>', unsafe_allow_html=True)
        mat1 = mat2 = None
    
    if mat1 is not None:
        if col_add.button("جمع"): st.write("✅ الناتج:", mat1 + mat2)
        if col_sub.button("طرح"): st.write("✅ الناتج:", mat1 - mat2)
        if col_mul.button("ضرب"): st.write("✅ الناتج:", np.dot(mat1, mat2))
        if col_det.button("محدد المصفوفة الأولى"): st.write("✅ المحدد:", np.linalg.det(mat1))
        if st.button("عكس المصفوفة الأولى"): 
            try: st.write("✅ العكس:", np.linalg.inv(mat1))
            except: st.markdown('<div class="error-box">❌ المصفوفة غير قابلة للعكس</div>', unsafe_allow_html=True)

# -----------------------------
# Tab 4: التفاضل والتكامل
# -----------------------------
with tab4:
    st.header("تفاضل وتكامل")
    func_input = st.text_input("ادخل دالة (مثال: x**2 + 3*x + 1):", "x**2 + 3*x + 1")
    col_diff, col_int = st.columns(2)
    try:
        func = sympify(fix_all_implied_multiplication(func_input))
        if col_diff.button("مشتقة"): st.write("✅ المشتقة:", diff(func, x))
        if col_int.button("تكامل"): st.write("✅ التكامل:", integrate(func, x))
    except:
        st.markdown('<div class="error-box">❌ صياغة الدالة خاطئة</div>', unsafe_allow_html=True)

# -----------------------------
# Tab 5: OCR والمسح الضوئي
# -----------------------------
with tab5:
    st.header("مسح ضوئي للمعادلات")
    uploaded_file = st.file_uploader("اختر صورة المعادلة:", type=["png","jpg","jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المرفوعة", use_column_width=True)
        reader = easyocr.Reader(['ar','en'])
        result = reader.readtext(np.array(image))
        extracted_text = " ".join([res[1] for res in result])
        st.markdown(f"📋 **النص المستخرج:** {extracted_text}")
        if extracted_text:
            steps = solve_with_explanation(extracted_text)
            for s in steps:
                if "❌" in s:
                    st.markdown(f'<div class="error-box">{s}</div>', unsafe_allow_html=True)
                elif "💡" in s or "🔧" in s or "📐" in s or "📊" in s:
                    st.markdown(f'<div class="explain-box">{s}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="step-box">{s}</div>', unsafe_allow_html=True)

# -----------------------------
# سجل العمليات
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
