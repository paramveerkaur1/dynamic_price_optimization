import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return pd.read_csv("data_processed.csv")

@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

@st.cache_resource
def load_features():
    return pickle.load(open("features.pkl", "rb"))

def generate_explanation(subset, optimal_price, price_mean):

    demand_avg = subset['demand'].mean()
    demand_std = subset['demand'].std()
    price_std = subset['price'].std()

    explanations = []

    # Demand level insight
    if demand_avg > subset['demand'].quantile(0.75):
        explanations.append("📈 High demand detected. The model recommends a higher price to maximize revenue.")

    elif demand_avg < subset['demand'].quantile(0.25):
        explanations.append("📉 Low demand observed. A lower price helps stimulate sales.")

    # Price sensitivity
    if price_std > 0.5:
        explanations.append("⚖️ Price variation is high, indicating customers are price sensitive.")

    else:
        explanations.append("🧾 Price variation is low, suggesting stable pricing behavior.")

    # Optimal vs average
    if optimal_price > price_mean:
        explanations.append("💰 Optimal price is above average, indicating strong demand conditions.")

    else:
        explanations.append("💡 Optimal price is below average to maintain demand levels.")

    # Store effect
    explanations.append("🏪 Store-level patterns also influence pricing decisions.")

    return explanations

data = load_data()
model = load_model()
features = load_features()

st.title("🔍 Smart Price Optimization")

# -----------------------------
# TOP FILTER BAR (NO SCROLL)
# -----------------------------
col1, col2, col3 = st.columns([2,2,1])

item = col1.selectbox("Item", sorted(data['item_id'].unique()))
store = col2.selectbox("Store", sorted(data['store_id'].unique()))
elasticity = col3.slider("Elasticity", 0.1, 1.5, 0.8)

subset = data[
    (data['item_id'] == item) &
    (data['store_id'] == store)
]

# -----------------------------
# TABS (KEY IMPROVEMENT)
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📊 Optimization", "📈 Trends", "🧠 Insights"])

# -----------------------------
# OPTIMIZATION TAB
# -----------------------------
with tab1:

    if st.button("🚀 Run Optimization"):

        price_mean = subset['price'].mean()

        price_range = np.linspace(price_mean*0.7, price_mean*1.3, 30)
        results = []

        for p in price_range:

            temp = pd.DataFrame({
                'price':[p],
                'month':[subset.iloc[-1]['month']],
                'weekday':[subset.iloc[-1]['weekday']],
                'lag_7':[subset.iloc[-1]['lag_7']],
                'snap':[subset.iloc[-1]['snap']],
                'price_relative':[p/price_mean],
                'item_code':[subset.iloc[-1]['item_code']],
                'item_avg_demand':[subset['demand'].mean()],
                'store_code':[subset.iloc[-1]['store_code']]
            })

            for col in features:
                if col not in temp.columns:
                    temp[col] = 0

            temp = temp[features]

            demand = model.predict(temp)[0]
            demand_adj = demand * np.exp(-elasticity*(p-price_mean)/price_mean)

            revenue = p * demand_adj
            results.append((p, revenue))

        df = pd.DataFrame(results, columns=['price','revenue'])
        optimal = df.loc[df['revenue'].idxmax()]

        # KPI CARDS
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Optimal Price", f"{optimal['price']:.2f}")
        c2.metric("📈 Max Revenue", f"{optimal['revenue']:.2f}")
        c3.metric("📊 Avg Price", f"{price_mean:.2f}")

        explanations = generate_explanation(subset, optimal['price'], price_mean)
        st.subheader("🧠 AI Pricing Insights")
        for exp in explanations:
            st.write(exp)
        
        confidence = min(100, int((subset.shape[0] / 100) * 100))
        st.metric("📊 Confidence Score", f"{confidence}%")
      
        # GRAPH
        fig, ax = plt.subplots()
        ax.plot(df['price'], df['revenue'], marker='o')
        ax.axvline(optimal['price'], linestyle='--')
        st.pyplot(fig)

        with st.expander("📋 Detailed Data"):
            st.dataframe(df)

# -----------------------------
# TRENDS TAB
# -----------------------------
with tab2:

    st.subheader("📈 Historical Trends")

    fig, ax = plt.subplots()
    ax.plot(subset['date'], subset['demand'])
    ax.set_title("Demand Over Time")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.plot(subset['date'], subset['price'])
    ax2.set_title("Price Over Time")
    st.pyplot(fig2)

# -----------------------------
# INSIGHTS TAB
# -----------------------------
with tab3:

    st.subheader("🧠 Smart Insights")

    st.write(f"Average Demand: {subset['demand'].mean():.2f}")
    st.write(f"Price Range: {subset['price'].min():.2f} - {subset['price'].max():.2f}")

    st.info("""
    💡 Insight:
    - Higher price reduces demand
    - Optimal price balances revenue vs demand
    - Store-level variation impacts pricing
    """)