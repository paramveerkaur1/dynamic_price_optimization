import streamlit as st

st.set_page_config(
    page_title="Dynamic Pricing System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 Dynamic Price Optimization System")

st.markdown("""
### 🚀 Overview

This system enables:
- 📈 Demand prediction using ML
- 💡 Price optimization for revenue maximization
- 🏪 Store-level pricing strategies

👉 Use the sidebar to navigate between modules.
""")

st.divider()

col1, col2, col3 = st.columns(3)

col1.info("🔍 Optimize pricing for any item-store combination")
col2.info("📊 Analyze trends and demand patterns")
col3.info("⚙️ Understand model behavior and features")

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)