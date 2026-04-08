import streamlit as st
import pandas as pd
import numpy as np
import pickle

@st.cache_data
def load_data():
    return pd.read_csv("data_processed.csv")

data = load_data()

st.title("📈 Compare Multiple Items")

# -----------------------------
# SELECTORS
# -----------------------------
items = st.multiselect("Select Items", sorted(data['item_id'].unique()))
store = st.selectbox("Select Store", sorted(data['store_id'].unique()))

results = []

# -----------------------------
# SIMPLE OPTIMIZATION (FAST)
# -----------------------------
def optimize_price(subset):

    price_mean = subset['price'].mean()
    demand_mean = subset['demand'].mean()

    price_range = np.linspace(price_mean * 0.7, price_mean * 1.3, 20)

    best_price = price_mean
    max_rev = 0

    for p in price_range:
        revenue = p * demand_mean

        if revenue > max_rev:
            max_rev = revenue
            best_price = p

    return best_price, max_rev

# -----------------------------
# RUN
# -----------------------------
if st.button("Compare Items"):

    for item in items:

        subset = data[
            (data['item_id'] == item) &
            (data['store_id'] == store)
        ]

        if len(subset) < 30:
            continue

        price, rev = optimize_price(subset)

        results.append({
            "item": item,
            "store": store,
            "optimal_price": price,
            "revenue": rev
        })

    df = pd.DataFrame(results)

    st.dataframe(df)

    if not df.empty:
        st.bar_chart(df.set_index('item')['optimal_price'])