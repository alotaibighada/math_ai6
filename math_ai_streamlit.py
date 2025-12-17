import streamlit as st
from sympy import symbols, Eq, solve, sympify
import easyocr
from PIL import Image
import numpy as np

st.title("🧮 Math AI – نسخة مبسطة مع OCR")

# -----------------------------
# العمليات الحسابية البسيطة
# -----------------------------
st.header("العمليات الحسابية")
num1 = st.number_input("الرقم الأول:", value=0)
num2 = st.number_input("الرقم الثاني:", value=0)
operation = st.selectbox("اختر العملية:", ["جمع", "طرح", "ضرب", "قسمة"])

if st.button("احسب"):
    try:
        if operation == "جمع":
            result = num1 + num2
        elif operation == "طرح":
            result = num1 - num2
        elif operation == "ضرب":
            result = num1 * num2
        elif operation == "قسمة":
            if num2 == 0:
                st.error("❌ لا يمكن القسمة على صفر")
                result = None
            else:
                result = num1 / num2
        if result is not None:
            st.success(f"✅ النتيجة: {result}")
    except Exception as e:
        st.error(f"❌ خطأ: {e}")

# -----------------------------
# حل المعادلات البسيطة
# -----------------------------
st.header("حل المعادلات البسيطة")
x = symbols("x")
eq_input = st.text_input("اكتب معادلة (مثال: 2*x + 5 = 15):")

if st.button("حل المعادلة"):
    try:
        left, right = eq_input.split("=")
        eq = Eq(sympify(left), sympify(right))
        solution = solve(eq, x)
        st.success(f"✅ الحل: {solution}")
    except:
        st.error("❌ صياغة المعادلة خاطئة")

# -----------------------------
# OCR لمسح المعادلات من الصور
# -----------------------------
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
        try:
            left, right = extracted_text.split("=")
            eq = Eq(sympify(left), sympify(right))
            solution = solve(eq, x)
            st.success(f"✅ الحل: {solution}")
        except:
            st.error("❌ لا يمكن حل المعادلة المستخرجة")
