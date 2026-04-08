import streamlit as st
import pickle

st.title("⚙️ Model Insights")

model = pickle.load(open("model.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

st.subheader("📦 Model Summary")
st.code(str(model))

st.subheader("🧾 Features Used")
st.write(features)

st.success("✔ Model is store-aware and item-aware")

st.info("""
This model uses:
- Item-level demand patterns
- Store-level behavior
- Price sensitivity signals
""")