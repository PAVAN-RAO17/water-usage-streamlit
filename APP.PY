import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import random
import time
import os

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI-Powered Water Usage Incentive System",
    page_icon="💧",
    layout="wide"
)

# ==================================================
# DARK THEME + UI STYLING
# ==================================================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #e5e7eb;
}
input, textarea {
    border-radius: 8px !important;
}
.card {
    background: #1f2937;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 6px 14px rgba(0,0,0,0.45);
}
.card h2 {
    color: #38bdf8;
    margin: 0;
    font-size: 26px;
}
.card p {
    margin-top: 6px;
    font-size: 14px;
    color: #cbd5f5;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# CSV SETUP
# ==================================================
DATA_PATH = "waterdata.csv"

if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=[
        "date",
        "usage_liters",
        "family_members",
        "expected_usage",
        "reward_points",
        "efficiency_score",
        "streak"
    ]).to_csv(DATA_PATH, index=False)

df = pd.read_csv(DATA_PATH)
if not df.empty:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ==================================================
# HEADER + SQUIRTLE SLOT
# ==================================================
header_col, squirtle_col = st.columns([4,1])
with header_col:
    st.title("💧 AI-Powered Water Usage Incentive System")
    st.caption("Smart • Sustainable • Incentive-Driven Water Intelligence")

squirtle_slot = squirtle_col.empty()
st.divider()

# ==================================================
# SIDEBAR INPUT
# ==================================================
with st.sidebar:
    st.header("📥 Daily Input")

    usage = st.number_input(
        "Water used today (liters)",
        min_value=0,
        step=1,
        format="%d"
    )

    members = st.number_input(
        "Family members",
        min_value=1,
        max_value=10,
        step=1,
        format="%d"
    )

    analyze = st.button("🚀 Analyze Usage")

# ==================================================
# AI EXPECTED USAGE FUNCTION
# ==================================================
def predict_expected(data, members):
    if len(data) >= 5:
        X = np.arange(len(data)).reshape(-1, 1)
        y = data["usage_liters"].values
        model = LinearRegression()
        model.fit(X, y)
        return max(50, int(model.predict([[len(data)]])[0]))
    elif len(data) >= 1:
        return int(data["usage_liters"].rolling(3, min_periods=1).mean().iloc[-1])
    else:
        return members * 135

# ==================================================
# MAIN LOGIC
# ==================================================
if analyze:
    with st.spinner("🤖 AI analyzing your water usage..."):
        time.sleep(1)

        expected = predict_expected(df, members)
        base_rate = 0.5
        base_bill = usage * base_rate

        efficiency = max(0, min(100, int((1 - usage / expected) * 100)))

        last_streak = int(df.iloc[-1]["streak"]) if not df.empty else 0
        streak = last_streak + 1 if usage <= expected else 0

        if usage <= expected:
            reward = int((expected - usage) * 2)
            discount = min(0.3, reward / 500)
            squirtle_img = "squirtle_happy.JPG"
        else:
            reward = 0
            discount = -0.25 if usage > expected * 1.5 else 0
            squirtle_img = "squirtle_angry.JPG"

        final_bill = base_bill * (1 - discount)

        saved = max(0, expected - usage)
        people_helped = saved // 100
        co2_saved = round(saved * 0.0003, 3)

        if streak >= 7:
            badge = "🥇 Water Hero"
        elif streak >= 3:
            badge = "🥈 Eco Guardian"
        elif streak >= 1:
            badge = "🥉 Smart Saver"
        else:
            badge = "🚫 No Badge Yet"

        df = pd.concat([df, pd.DataFrame([{
            "date": datetime.today(),
            "usage_liters": usage,
            "family_members": members,
            "expected_usage": expected,
            "reward_points": reward,
            "efficiency_score": efficiency,
            "streak": streak
        }])], ignore_index=True)

        df.to_csv(DATA_PATH, index=False)

    # ===============================
    # SQUIRTLE DISPLAY (5 SECONDS)
    # ===============================
    squirtle_slot.image(squirtle_img, width=140)
    time.sleep(5)
    squirtle_slot.empty()

    st.success("✔ Analysis completed successfully")

    # ==================================================
    # DASHBOARD CARDS
    # ==================================================
    c1, c2, c3, c4, c5 = st.columns(5)

    def card(col, val, label):
        col.markdown(f"""
        <div class="card">
            <h2>{val}</h2>
            <p>{label}</p>
        </div>
        """, unsafe_allow_html=True)

    card(c1, f"{usage} L", "Today's Usage")
    card(c2, f"{expected} L", "Expected Usage")
    card(c3, f"{efficiency}%", "Efficiency Score")
    card(c4, f"₹{int(base_bill)}", "Base Bill")
    card(c5, f"₹{int(final_bill)}", "Final Bill")

    st.subheader("🏅 Achievement Badge")
    st.info(badge)

    st.subheader("🔥 Conservation Streak")
    st.write(f"🌱 **{streak} consecutive days** of responsible water usage")

    st.subheader("🌍 Environmental Impact")
    st.write(f"💧 Water saved: **{saved} liters**")
    st.write(f"👤 Drinking water for **{people_helped} people/day**")
    st.write(f"🌿 CO₂ reduced: **{co2_saved} kg**")

# ==================================================
# HISTORICAL LINE GRAPH
# ==================================================
if not df.empty:
    st.divider()
    st.subheader("📈 Historical Water Usage Trends")
    st.line_chart(df.set_index("date")[["usage_liters", "expected_usage"]])

# ==================================================
# MOTIVATIONAL QUOTES & FACTS
# ==================================================
quotes = [
    "Every drop saved secures tomorrow 💧",
    "Water conservation is self-preservation 🌍",
    "Smart usage is real wealth 💡",
    "Save water today, survive tomorrow 🌱",
    "Small actions create big impact 🚰",
    "Respect water — it sustains life 💙",
    "Saving water is saving energy ⚡",
    "A mindful drop today builds a safer future 🌏",
    "Water wisely, live responsibly ♻️",
    "Conservation begins at home 🏠",
    "Think before you let it flow 🚿"
]

facts = [
    "Only about 1% of Earth’s water is usable freshwater 🌍",
    "A leaking tap can waste up to 15 liters per day 🚰",
    "Producing 1 kg of rice requires nearly 2,500 liters of water 🌾",
    "Shortening your shower by 5 minutes can save up to 40 liters 🚿",
    "Water treatment and pumping consume large amounts of electricity ⚡",
    "Less than 30% of wastewater is treated globally 🌎",
    "Over 2 billion people face water scarcity 💧",
    "Saving water also reduces carbon emissions 🌿",
    "Agriculture consumes about 70% of freshwater 🚜",
    "Rainwater harvesting can meet up to 50% of household needs 🌧️",
    "Freshwater ecosystems are declining rapidly 🌊"
]

st.divider()
st.info(f"💬 Quote: {random.choice(quotes)}")
st.caption(f"📘 Fact: {random.choice(facts)}")

# ==================================================
# FOOTER
# ==================================================
st.caption("AI-Powered Water Usage Incentive System | Final Academic Prototype")







