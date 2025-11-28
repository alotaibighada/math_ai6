import streamlit as st
from sympy import symbols, Eq, solve, sympify

# -----------------------------
# إعداد الصفحة
# -----------------------------
st.set_page_config(page_title="Math AI – المساعد الرياضي", layout="centered")

# -----------------------------
# الخلفية الثابتة
# -----------------------------
st.markdown(
"""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1470&q=80");
    background-size: cover;
    background-attachment: fixed;
}

/* تحسين وضوح الحقول */
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

/* أزرار واضحة وكبيرة */
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

/* النصوص والعناوين أكبر وأكثر وضوحًا */
.stMarkdown, .stHeader, .stSubheader {
    background: rgba(0,0,0,0.5);
    padding: 8px 12px;
    border-radius: 10px;
    color: white !important;
    font-size: 1.6em;
