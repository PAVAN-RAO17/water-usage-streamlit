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
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# FUTURISTIC CSS (GLOW + ANIMATIONS)
# ==================================================
st.markdown(
    """
    <style>
    body {
        background-color: #0b0f19;
        color: #e0e0e0;
    }

    .glow-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.25);
        animation: glow 2.5s infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(0,255,255,0.2); }
        to   { box-shadow: 0 0 25px rgba(0,255,255,0.6); }
    }

    .slide-in {
        animation: slide 0.8s ease-out;
    }

    @keyframes slide {
        from { transform: translateY(20px); opacity: 0; }
        to   { transform: translateY(0); opacity: 1; }
    }

    .tip-box {
        background-color: #111827;
        border-left: 4px solid #22d3ee;
        padding: 15px;
        border-radius: 12px;
        margin-top: 10px;
        animation: slide 0.8s ease-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# SAFE CSV LOADING
# ==================================================
DATA_DIR = "data"
DATA_PATH = os.path.join(DATA_DIR, "water_data.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(DATA_PATH):
    df = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "usage_liters": [420],
            "family_members": [4],
            "expected_usage": [450],
            "reward_points": [0],
        }
    )
    df.to_csv(DATA_PATH, index=False)
else:
    df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])


# ==================================================
# HEADER
# ==================================================
st.markdown(
    "<h1 class='slide-in'>💧 Smart Water Usage AI</h1>",
    unsafe_allow_html=True,
)
st.caption("AI-powered insights for sustainable water usage 🌐")
st.divider()


# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.header("📥 Daily Input")
    usage = st.number_input("Water Used Today (liters)", min_value=0)
    members = st.number_input("Family Members", min_value=1)
    analyze = st.button("Analyze with AI ⚡")


# ==================================================
# MAIN LOGIC
# ==================================================
if analyze:
    with st.spinner("Running AI analysis..."):
        expected = predict_expected_usage(df)
        reward = calculate_rewards(usage, expected)

    new_row = {
        "date": datetime.today(),
        "usage_liters": usage,
        "family_members": members,
        "expected_usage": expected,
        "reward_points": reward,
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

    st.toast("AI analysis complete ✔", icon="🤖")

    # ------------------------------
    # METRICS (FUTURISTIC)
    # ------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="glow-card">
            <h3>💦 Usage</h3>
            <h2>{usage} L</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="glow-card">
            <h3>📊 Expected</h3>
            <h2>{expected} L</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="glow-card">
            <h3>⭐ Rewards</h3>
            <h2>{reward}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------------------
    # PROGRESS + FEEDBACK
    # ------------------------------
    st.subheader("🚰 Water Efficiency Index")

    if usage < expected:
        progress = min((expected - usage) / expected, 1.0)
        st.progress(progress)
        st.success("Efficiency level optimal 🌱")
    else:
        st.progress(0.15)
        st.warning("Efficiency below optimal – consider reducing usage ⚠️")

    st.subheader("🧠 AI Feedback")

    if reward > 0:
        st.info("Status: **Water Saver Mode Activated** ✅")
    else:
        st.info("Status: **Optimization Recommended** ⚙️")


# ==================================================
# ANALYTICS
# ==================================================
st.divider()
st.subheader("📈 Consumption Intelligence")

col1, col2 = st.columns([2, 1])

with col1:
    st.line_chart(
        df.set_index("date")[["usage_liters", "expected_usage"]],
        height=350,
    )

with col2:
    st.markdown(
        """
        **Graph Legend**
        - 🔵 Actual consumption  
        - ⚫ AI baseline  
        - Staying below baseline improves efficiency  
        """
    )


# ==================================================
# SMART TIPS
# ==================================================
st.divider()
st.subheader("💡 Smart Water Optimization Tips")

tips = [
    "Turn off taps during brushing 🪥",
    "Repair leaks immediately 🚰",
    "Prefer bucket baths over long showers 🪣",
    "Reuse RO wastewater for plants 🌿",
    "Run appliances only at full load 👕",
    "Harvest rainwater where possible 🌧️",
]

st.markdown(
    f"<div class='tip-box'>🤖 AI Suggests: {np.random.choice(tips)}</div>",
    unsafe_allow_html=True,
)


# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.caption("🚀 Futuristic AI Dashboard | Innovation & Design Thinking Project")
