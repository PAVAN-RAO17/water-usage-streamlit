import streamlit as st
import pandas as pd
from model import predict_expected_usage
from logic import calculate_rewards
from datetime import datetime

st.set_page_config(
    page_title="Smart Water AI",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Smart Water Usage AI System")
st.subheader("Save Water • Earn Rewards • Build a Sustainable Future")

DATA_PATH = "data/water_data.csv"

df = pd.read_csv(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

with st.sidebar:
    st.header("📥 Enter Today's Usage")
    usage = st.number_input("Water Used Today (liters)", min_value=0)
    members = st.number_input("Family Members", min_value=1)

if st.button("Analyze Usage 🚀"):
    expected = predict_expected_usage(df)
    reward = calculate_rewards(usage, expected)

    new_row = {
        "date": datetime.today(),
        "usage_liters": usage,
        "family_members": members,
        "expected_usage": expected,
         "reward_points": reward
    }

    df = pd.concat([df, pd.DataFrame([new_row])])
    df.to_csv(DATA_PATH, index=False)

    if reward > 0:
        st.success(f"🌟 AMAZING! You are a Water Saviour!\n\nReward Points Earned: {reward}")
        st.balloons()
    else:
        st.warning("⚠ Usage exceeded expected level.\nTry reducing usage to earn rewards.")

st.divider()

st.subheader("📊 Water Usage Analytics")

col1, col2 = st.columns(2)

with col1:
    st.line_chart(df.set_index("date")[["usage_liters", "expected_usage"]])

with col2:
    st.bar_chart(df.set_index("date")[["reward_points"]])

st.divider()

latest = df.iloc[-1]
if latest["reward_points"] > 0:
    st.markdown("### 🌱 Feedback: *You are contributing to water conservation. Keep it up!*")
else:
    st.markdown("### 💡 Feedback: *Small changes can save big amounts of water. Try again tomorrow!*")

