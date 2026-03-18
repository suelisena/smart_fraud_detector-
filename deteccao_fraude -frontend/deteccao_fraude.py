import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib

model = joblib.load("fraude_model.pkl")
scaler = joblib.load("scaler.pkl")

st.markdown("<h1 style='font-size:40px; color:#2E86C1;'>💳 Fraud Detection System</h1>", unsafe_allow_html=True)

with st.form("fraude_form"):
    valor_str = st.text_input("Transaction amount (R$)", "15000")
    amount = float(valor_str.replace(".", "").replace(",", "."))

    time_input = st.number_input("Transaction time (0-23)", min_value=0, max_value=23)
    location = st.selectbox("Transaction location", ["Physical Store", "Online"])
    submitted = st.form_submit_button("Detect Fraud")

if submitted:
    df_new = pd.DataFrame([{"amount": amount, "time": time_input, "location": location}])
    df_new_encoded = pd.get_dummies(df_new, columns=['location'], drop_first=True)

    for col in ["location_Online"]:
        if col not in df_new_encoded.columns:
            df_new_encoded[col] = 0

    df_new_encoded[['amount', 'time']] = scaler.transform(df_new_encoded[['amount', 'time']])
    prob = model.predict_proba(df_new_encoded)[0,1]
    prediction = 1 if prob > 0.5 else 0 

    st.write(f"🔎 Fraud Probability: **{prob:.2f}**")
    if prediction == 1:
        st.error("🚨 Fraud detected! Attention to sales.")
    else:
        st.success("✅ Secure transaction.")

    # --- Dataserver statistics ---
st.write("---")
st.subheader("📊 Dataserver Statistics")

# Load the original dataset here to display statistics.
df = pd.read_csv("fraudes.csv") 

# Fraudes by hour
fraudes_by_hour = df.groupby("time")["is_fraud"].sum()
st.bar_chart(fraudes_by_hour)

# Create histogram of values
hist_values, bin_edges = np.histogram(df["amount"], bins=20)

st.subheader("📊 Distribution of transaction values")
st.bar_chart(hist_values)

# Distribution of values
st.subheader("📊 Distribution of transaction values")
fig, ax = plt.subplots()
ax.hist(df["amount"], bins=20, color="skyblue", edgecolor="black")
ax.set_xlabel("Transaction Value (BRL)")
ax.set_ylabel("Quantity")
st.pyplot(fig)

# Metrics
st.metric("Total of transactions", len(df))
st.metric("Total of frauds", df["is_fraud"].sum())
st.metric("Percentage of frauds", f"{df['is_fraud'].mean()*100:.2f}%")