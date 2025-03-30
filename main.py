# main.py

from fueling_engine import goal_logic_run, recommend_macros
import joblib
import pandas as pd

# ---- Athlete info (mock input or from real app) ----
athlete = {
    "id": "A002",
    "age": 25,
    "height_cm": 172,
    "weight_lbs": 180,
    "goal": "maintain",
    "sport": "marathon_running"
}

# ---- Load a workout row (simulate or pull from csv) ----
df = pd.read_csv("combined_with_engineered_features.csv")
sample = df.sample(1, random_state=42)  # Pick a random row for testing

# ---- Predict calories burned ----
model = joblib.load("lightgbm_calorie_model.pkl")
features = [
    "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv",
    "avg_hr", "max_hr", "distance_km", "duration_min", "elevation_gain_m",
    "sleep_hrs_prior", "hrv_today", "temp_c", "session_type",
    "hr_fluctuation", "fatigue_index", "depletion_score"
]

from sklearn.preprocessing import LabelEncoder
import joblib

# Load the encoders you saved earlier
encoder_sex = joblib.load("encoder_sex.pkl")
encoder_session = joblib.load("encoder_session.pkl")

# Apply encoders to the sample
sample["sex"] = encoder_sex.transform(sample["sex"])
sample["session_type"] = encoder_session.transform(sample["session_type"])


calories_burned = model.predict(sample[features])[0]

# ---- Run goal logic ----
final_goal = goal_logic_run(
    athlete["id"],
    athlete["age"],
    athlete["height_cm"],
    athlete["weight_lbs"],
    athlete["goal"],
    athlete["sport"]
)

# ---- Generate macro plan ----
macro_plan = recommend_macros(
    calories_burned=calories_burned,
    sport_profile=athlete["sport"],
    goal=final_goal
)

# ---- Clean the macro plan output ----
clean_plan = {k: round(float(v), 2) if isinstance(v, (float, int)) else v for k, v in macro_plan.items()}

# ---- Print result ----
print("\n--- Session Summary ---")
print(f"Athlete ID: {athlete['id']}")
print(f"Calories Burned (predicted): {calories_burned:.2f} kcal")
print(f"Nutrition Goal: {final_goal}")
print(f"Macro Plan: {clean_plan}")

import csv
import os

# ---- Log to CSV ----
log_file = "fueling_log.csv"
log_fields = [
    "athlete_id", "calories_burned", "goal", "replenish_kcal",
    "carbs_g", "protein_g", "fat_g", "carbs_kcal", "protein_kcal", "fat_kcal",
    "profile_type"
]

log_entry = {
    "athlete_id": athlete["id"],
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
#-- CSV history log --
file_exists = os.path.isfile(log_file)

with open(log_file, mode="a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=log_fields)

    if not file_exists:
        writer.writeheader()

    writer.writerow(log_entry)

print(f"\n✅ Session logged to {log_file}")
