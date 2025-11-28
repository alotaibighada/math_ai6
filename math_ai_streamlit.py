import streamlit as st
from sympy import symbols, Eq, solve, sympify

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# -----------------------------
# الخلفية الثابتة
# -----------------------------
background_url = "https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1470&q=80"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* تحسين وضوح الحقول */
    .stNumberInput>div>div>input,
    .stTextInput>div>div>input {{
        background: rgba(255,255,255,0.95) !important;
        color: black !important;
        font-size: 1.3em;
        padding: 0.5em;
        border-radius: 10px;
        border: 1px solid #555;
        text-align: center;
    }}

    /* أزرار واضحة */
    .stButton>button {{
        height: 3em;
        width: 100%;
        border-radius: 12px;
        border: n
