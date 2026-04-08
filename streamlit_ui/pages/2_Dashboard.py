import streamlit as st
import pandas as pd

data = pd.read_csv("data_processed.csv")

st.title("📊 Executive Dashboard")

store = st.selectbox("Store", ["All"] + list(data['store_id'].unique()))

if store != "All":
    data = data[data['store_id'] == store]

# KPI ROW
c1, c2, c3, c4 = st.columns(4)

c1.metric("Items", data['item_id'].nunique())
c2.metric("Stores", data['store_id'].nunique())
c3.metric("Avg Price", round(data['price'].mean(),2))
c4.metric("Avg Demand", round(data['demand'].mean(),2))

# CHART ROW
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Demand Items")
    st.bar_chart(data.groupby('item_id')['demand'].mean().head(10))

with col2:
    st.subheader("Store Comparison")
    st.bar_chart(data.groupby('store_id')['price'].mean())