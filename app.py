import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

from model import predict_expected_usage
from logic import calculate_rewards


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Smart Water AI",
    page_icon="💧",
    layout="wide"
)


# ==================================================
# DATA SETUP (SAFE & BACKWARD-COMPATIBLE)
# ==================================================
DATA_DIR = "data"
DATA_PATH = os.path.join(DATA_DIR, "water_data.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(DATA_PATH):
    df = pd.DataFrame({
        "date": [],
        "usage_liters": [],
        "family_members": [],
        "expected_usage": [],
        "reward_points": [],
        "efficiency_score": [],
        "streak": []
    })
    df.to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH)

# Ensure required columns exist (FIXES YOUR ERROR)
required_cols = [
    "date",
    "usage_liters",
    "family_members",
    "expected_usage",
    "reward_points",
    "efficiency_score",
    "streak"
]

for col in required_cols:
    if col not in df.columns:
        df[col] = 0

if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")


# ==================================================
# HEADER
# ==================================================
st.title("💧 Smart Water Usage AI")
st.caption("Simple, reliable & sustainable water monitoring system")
st.divider()


# ==================================================
# SIDEBAR INPUT
# ==================================================
with st.sidebar:
    st.header("📥 Daily Input")
    usage = st.number_input("Water used today (liters)", min_value=0)
    members = st.number_input("Family members", min_value=1)
    analyze = st.button("Analyze Usage")


# ==================================================
# MAIN LOGIC
# ==================================================
if analyze:
    expected = predict_expected_usage(df)
    reward = calculate_rewards(usage, expected)

    # -----------------------------
    # WATER EFFICIENCY SCORE
    # -----------------------------
    if expected > 0:
        efficiency = max(0, min(100, int((1 - usage / expected) * 100)))
    else:
        efficiency = 0

    # -----------------------------
    # CONSERVATION STREAK (SAFE)
    # -----------------------------
    if not df.empty and "streak" in df.columns:
        last_streak = int(df.iloc[-1]["streak"])
    else:
        last_streak = 0

    streak = last_streak + 1 if usage < expected else 0

    # -----------------------------
    # ENVIRONMENTAL IMPACT
    # -----------------------------
    saved = max(0, expected - usage)
    people_helped = saved // 100

    # -----------------------------
    # ACHIEVEMENT BADGE
    # -----------------------------
    if streak >= 7:
        badge = "🥇 Water Hero"
    elif streak >= 3:
        badge = "🥈 Eco Guardian"
    elif streak >= 1:
        badge = "🥉 Smart Saver"
    else:
        badge = "No badge yet"

    # -----------------------------
    # SAVE DATA
    # -----------------------------
    new_row = {
        "date": datetime.today(),
        "usage_liters": usage,
        "family_members": members,
        "expected_usage": expected,
        "reward_points": reward,
        "efficiency_score": efficiency,
        "streak": streak
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    st.success("Analysis completed successfully ✔")


    # ==================================================
    # RESULTS DISPLAY
    # ==================================================
    col1, col2, col3 = st.columns(3)

    col1.metric("Today's Usage (L)", usage)
    col2.metric("Expected Usage (L)", expected)
    col3.metric("Efficiency Score", f"{efficiency}%")

    st.subheader("🏆 Achievement")
    st.info(badge)

    st.subheader("🌍 Environmental Impact")
    st.write(f"💧 Water saved: **{saved} liters**")
    st.write(f"👤 Drinking water for **{people_helped} people/day**")

    st.subheader("🔥 Conservation Streak")
    st.write(f"Current streak: **{streak} days**")


# ==================================================
# ANALYTICS 
# ==================================================
if not df.empty:
    st.divider()
    st.subheader("📈 Usage Analytics")

    st.line_chart(
        df.set_index("date")[["usage_liters", "expected_usage"]],
        height=300
    )


# ==================================================
# WATER SAVING TIPS
# ==================================================
tips = [
    "Turn off tap while brushing 🪥",
    "Fix leaking taps 🚰",
    "Use bucket instead of shower 🪣",
    "Reuse RO wastewater 🌱",
    "Harvest rainwater 🌧️"
]

st.divider()
st.info(f"💡 Tip: {np.random.choice(tips)}")


# ==================================================
# FOOTER
# ==================================================
st.caption("Smart Water AI | Clean • Stable •" )
