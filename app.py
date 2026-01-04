import streamlit as st
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime
from sklearn.linear_model import LinearRegression

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI-Powered Water Usage Incentive System",
    page_icon="💧",
    layout="wide"
)

st.markdown("""
<style>
body { background-color: #0e1117; }
[data-testid="stMetric"] { background: #161b22; padding: 15px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CONSTANTS
# -------------------------------------------------
CSV_FILE = "waterdata.csv"
HAPPY_IMG = "squirtle_happy.jpg"
ANGRY_IMG = "squirtle_angry.jpg"
RATE_PER_LITER = 0.5  # ₹ per liter

# -------------------------------------------------
# LOAD / INIT CSV
# -------------------------------------------------
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "date", "usage_liters", "family_members",
        "expected_usage", "efficiency", "streak",
        "reward_points"
    ])
    df.to_csv(CSV_FILE, index=False)

df = pd.read_csv(CSV_FILE)
if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
col_title, col_img = st.columns([5, 1])
with col_title:
    st.title("💧 AI-Powered Water Usage Incentive System")
    st.caption("Smart • Fair • Incentive-Driven Water Conservation")

with col_img:
    pass  # Squirtle appears only after analysis

st.divider()

# -------------------------------------------------
# SIDEBAR INPUTS
# -------------------------------------------------
with st.sidebar:
    st.header("📥 Daily Input")
    usage = st.number_input("Water used today (liters)", min_value=0, step=1)
    members = st.slider("Family members", 1, 10, 3)
    analyze = st.button("🚀 Analyze Usage")

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def predict_expected(df, members):
    if len(df) < 3:
        return members * 135  # fallback WHO estimate

    X = df[["family_members"]]
    y = df["usage_liters"]

    model = LinearRegression()
    model.fit(X, y)

    pred = model.predict([[members]])[0]

    rolling = df["usage_liters"].rolling(3).mean().iloc[-1]
    return int((pred + rolling) / 2)

def show_squirtle(happy: bool):
    img = HAPPY_IMG if happy else ANGRY_IMG
    if os.path.exists(img):
        st.image(img, width=130)

# -------------------------------------------------
# MAIN LOGIC
# -------------------------------------------------
if analyze:
    expected = predict_expected(df, members)

    efficiency = max(0, min(100, int((1 - usage / expected) * 100))) if expected else 0

    last_streak = int(df.iloc[-1]["streak"]) if not df.empty else 0
    streak = last_streak + 1 if usage <= expected else 0

    reward_points = max(0, expected - usage) // 10
    saved = max(0, expected - usage)

    base_bill = usage * RATE_PER_LITER
    discount = min(0.25, reward_points * 0.01)
    final_bill = base_bill * (1 - discount)

    badge = (
        "🥇 Water Hero" if streak >= 7 else
        "🥈 Eco Guardian" if streak >= 3 else
        "🥉 Smart Saver" if streak >= 1 else
        "—"
    )

    # Save to CSV
    new_row = {
        "date": datetime.now(),
        "usage_liters": usage,
        "family_members": members,
        "expected_usage": expected,
        "efficiency": efficiency,
        "streak": streak,
        "reward_points": reward_points
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------
    st.success("✔ Analysis completed")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Water Used (L)", usage)
    col2.metric("Expected Usage (L)", expected)
    col3.metric("Efficiency Score", f"{efficiency}%")
    col4.metric("Streak (days)", streak)

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Base Bill (₹)", f"{base_bill:.2f}")
    col6.metric("Discount", f"{int(discount*100)}%")
    col7.metric("Final Bill (₹)", f"{final_bill:.2f}")
    col8.metric("Reward Points", reward_points)

    st.subheader("🏆 Achievement Badge")
    st.info(badge)

    st.subheader("🌍 Environmental Impact")
    st.write(f"💧 Water saved: **{saved} liters**")
    st.write(f"👥 Drinking water for **{saved // 100} people/day**")

    st.subheader("🧠 Squirtle Says")
    show_squirtle(usage <= expected)

# -------------------------------------------------
# ANALYTICS
# -------------------------------------------------
if not df.empty:
    st.divider()
    st.subheader("📈 Historical Trends")
    st.line_chart(df.set_index("date")[["usage_liters", "expected_usage"]])

# -------------------------------------------------
# QUOTES & FACTS
# -------------------------------------------------
quotes = [
    "Water is life. Save it.",
    "Every drop counts.",
    "Conserve water, preserve the future.",
    "Saving water saves energy.",
    "No water, no life.",
    "Think blue, act green.",
    "Water today, life tomorrow.",
    "Respect every drop.",
    "Small actions create big change.",
    "Use water wisely."
]

facts = [
    "Only 1% of Earth's water is drinkable.",
    "A dripping tap wastes 15 liters/day.",
    "Showers use less water than baths.",
    "India faces extreme water stress.",
    "Water scarcity affects 40% globally.",
    "RO wastewater can be reused.",
    "Rainwater harvesting saves bills.",
    "Agriculture uses 70% freshwater.",
    "Water demand rises 1% yearly.",
    "Urban leaks waste millions of liters."
]

st.divider()
st.info(f"💬 Quote: {random.choice(quotes)}")
st.warning(f"📘 Fact: {random.choice(facts)}")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.caption("AI-Powered Water Usage Incentive System • Prototype • VTU Mini Project")
