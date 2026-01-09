import streamlit as st
import pandas as pd
import numpy as np
import os
import random
import base64
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

/* Squirtle bottom-right */
.squirtle {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 130px;
    z-index: 9999;
    pointer-events: none;
}
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
# BASE64 IMAGE LOADER (STREAMLIT SAFE)
# -------------------------------------------------
def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

happy_img_base64 = load_image_base64(HAPPY_IMG)
angry_img_base64 = load_image_base64(ANGRY_IMG)

# -------------------------------------------------
# LOAD / INIT CSV
# -------------------------------------------------
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=[
        "date",
        "usage_liters",
        "family_members",
        "expected_usage",
        "efficiency",
        "streak",
        "reward_points",
        "discount_percent",
        "penalty_percent",
        "final_bill"
    ])
    df.to_csv(CSV_FILE, index=False)

df = pd.read_csv(CSV_FILE)

# Backward compatibility
for col in ["discount_percent", "penalty_percent", "final_bill"]:
    if col not in df.columns:
        df[col] = 0

if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("💧 AI-Powered Water Usage Incentive System")
st.caption("Smart • Fair • Incentive-Driven Water Conservation")
st.divider()

# -------------------------------------------------
# SIDEBAR INPUT
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
        return members * 135  # WHO baseline

    X = df[["family_members"]]
    y = df["usage_liters"]

    model = LinearRegression()
    model.fit(X, y)

    ml_pred = model.predict([[members]])[0]
    rolling = df["usage_liters"].rolling(3).mean().iloc[-1]

    return int((ml_pred + rolling) / 2)

def calculate_penalty(actual, expected):
    if expected == 0:
        return 0

    excess_pct = ((actual - expected) / expected) * 100

    if excess_pct <= 10:
        return 0
    elif excess_pct <= 25:
        return 3
    elif excess_pct <= 50:
        return 6
    else:
        return 10  # lenient cap

def show_squirtle(happy):
    img = happy_img_base64 if happy else angry_img_base64
    st.markdown(
        f"""
        <img src="data:image/jpeg;base64,{img}"
             class="squirtle">
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# MAIN LOGIC
# -------------------------------------------------
if analyze:
    expected = predict_expected(df, members)

    efficiency = (
        max(0, min(100, int((1 - usage / expected) * 100)))
        if expected else 0
    )

    last_streak = int(df.iloc[-1]["streak"]) if not df.empty else 0
    streak = last_streak + 1 if usage <= expected else 0

    # Rewards (UNCHANGED)
    reward_points = max(0, expected - usage) // 10
    saved = max(0, expected - usage)

    base_bill = usage * RATE_PER_LITER

    # Discount (UNCHANGED)
    discount_percent = min(25, reward_points)  # 1 point = 1%
    bill_after_discount = base_bill * (1 - discount_percent / 100)

    # Penalty (SEPARATE)
    penalty_percent = calculate_penalty(usage, expected)
    final_bill = bill_after_discount + (bill_after_discount * penalty_percent / 100)

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
        "reward_points": reward_points,
        "discount_percent": discount_percent,
        "penalty_percent": penalty_percent,
        "final_bill": final_bill
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    # -------------------------------------------------
    # DISPLAY
    # -------------------------------------------------
    st.success("✔ Analysis completed")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Water Used (L)", usage)
    c2.metric("Expected Usage (L)", expected)
    c3.metric("Efficiency (%)", efficiency)
    c4.metric("Streak (days)", streak)

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Base Bill (₹)", f"{base_bill:.2f}")
    c6.metric("Discount (%)", f"{discount_percent}%")
    c7.metric("Penalty (%)", f"{penalty_percent}%")
    c8.metric("Final Bill (₹)", f"{final_bill:.2f}")

    st.subheader("🏆 Achievement Badge")
    st.info(badge)

    st.subheader("🌍 Environmental Impact")
    st.write(f"💧 Water saved: **{saved} liters**")
    st.write(f"👥 Drinking water for **{saved // 100} people/day**")

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
st.caption("AI-Powered Water Usage Incentive System • Prototype •  Mini Project")

