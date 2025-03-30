# app.py
import streamlit as st
import pandas as pd
import joblib
from fueling_engine import goal_logic_run, recommend_macros
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime


BASE_DIR = os.path.dirname(__file__)


# Load model and encoders
model = joblib.load("lightgbm_calorie_model.pkl")
encoder_sex = joblib.load("encoder_sex.pkl")
encoder_session = joblib.load("encoder_session.pkl")

# Define features
features = [
    "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv",
    "avg_hr", "max_hr", "distance_km", "duration_min", "elevation_gain_m",
    "sleep_hrs_prior", "hrv_today", "temp_c", "session_type",
    "hr_fluctuation", "fatigue_index", "depletion_score"
]

# Load session data
@st.cache_data
def load_data():
    return pd.read_csv("combined_with_engineered_features.csv")

df = load_data()

st.title("🏃 Athlete Fueling & Macro Recommendation")

# Sidebar: athlete input
st.sidebar.header("Athlete Profile")
user_id = st.sidebar.text_input("Athlete ID", "A001")
age = st.sidebar.slider("Age", 18, 50, 23)
height = st.sidebar.number_input("Height (cm)", value=180)
weight = st.sidebar.number_input("Weight (lbs)", value=160)
goal = st.sidebar.selectbox("Goal", ["cutting", "maintain", "bulking"])
sport = st.sidebar.selectbox("Sport", [
    "marathon_running", "track_and_field_distance", "track_and_field_mid", "track_and_field_power"
])

# Select a random session
session = df.sample(1, random_state=42).copy()

# Encode categoricals
session["sex"] = encoder_sex.transform(session["sex"])
session["session_type"] = encoder_session.transform(session["session_type"])

# Predict calories
calories_burned = model.predict(session[features])[0]

# Run logic
final_goal = goal_logic_run(user_id, age, height, weight, goal, sport)
macro_plan = recommend_macros(calories_burned, sport, final_goal)
clean_plan = {k: round(float(v), 2) if isinstance(v, (float, int)) else v for k, v in macro_plan.items()}

# Display results
st.subheader("📊 Fueling Recommendation")
st.write(f"**Calories Burned (predicted):** {calories_burned:.2f} kcal")
st.write(f"**Goal:** {final_goal.capitalize()}")
st.write("**Macro Breakdown:**")
st.json(clean_plan)

#-- Click button and logging to backend --#
import csv

log_file = os.path.join(BASE_DIR, "fueling_log.csv")

if st.button("📥 Log This Session"):
    log_fields = [
        "timestamp", "athlete_id", "calories_burned", "goal", "replenish_kcal",
        "carbs_g", "protein_g", "fat_g", "carbs_kcal", "protein_kcal", "fat_kcal",
        "profile_type"
    ]

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "athlete_id": user_id,
        "calories_burned": round(calories_burned, 2),
        "goal": final_goal,
        "replenish_kcal": clean_plan["total_kcal_to_replenish"],
        "carbs_g": clean_plan["carbs_g"],
        "protein_g": clean_plan["protein_g"],
        "fat_g": clean_plan["fat_g"],
        "carbs_kcal": clean_plan["carbs_kcal"],
        "protein_kcal": clean_plan["protein_kcal"],
        "fat_kcal": clean_plan["fat_kcal"],
        "profile_type": clean_plan["profile_type"]
    }

    file_exists = os.path.isfile(log_file)

    with open(log_file, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=log_fields)
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)

    st.success("✅ Session logged to fueling_log.csv")


# Optional plot if log exists
log_file = "fueling_log.csv"
if os.path.exists(log_file):
    st.subheader("📈 Logged Session History")
    df_log = pd.read_csv(log_file)
    fig, ax = plt.subplots()
    sns.lineplot(data=df_log, y="calories_burned", x=range(len(df_log)), marker="o", ax=ax)
    ax.set_title("Calories Burned Over Sessions")
    ax.set_xlabel("Session Number")
    ax.set_ylabel("Calories Burned (kcal)")
    st.pyplot(fig)
else:
    st.info("No session log found. Run main.py to generate fueling_log.csv")
