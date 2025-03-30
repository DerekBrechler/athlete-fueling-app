import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10_000  # smaller sample focused on race day
baseline_sleep = 8.0
race_distance_km = 42.2

data = []
for i in range(1, rows + 1):
    age = np.random.randint(22, 45)
    sex = np.random.choice(["M", "F"])
    weight_kg = np.round(np.random.uniform(55, 90), 1)
    vo2_max = np.round(np.random.uniform(40, 65), 1)
    resting_hr = np.random.randint(45, 60)
    baseline_hrv = np.random.randint(60, 100)

    # Marathon duration (in minutes): ~2.3 to 5 hours
    duration_min = np.random.randint(140, 300)

    # Simulate increasing HR due to fatigue
    base_avg_hr = np.random.randint(140, 165)
    avg_hr = base_avg_hr + int(np.random.normal(5, 3))  # small upward drift
    max_hr = avg_hr + np.random.randint(10, 20)

    # Add small fluctuations to pace
    pace_min_per_km = np.round(np.random.normal(duration_min / race_distance_km, 0.2), 2)

    elevation_gain = np.random.randint(50, 250)  # Race route variation
    session_type = "race"

    sleep_hrs_prior = np.round(np.random.uniform(4.0, 7.5), 1)
    hrv_today = np.round(baseline_hrv * np.random.uniform(0.6, 1.0), 1)
    temp_c = np.random.randint(10, 30)

    percent_hr_max = np.round(avg_hr / max_hr, 3)
    hr_efficiency = np.round(avg_hr / race_distance_km + np.random.normal(1, 2), 2)
    vo2_hr_ratio = np.round(vo2_max / avg_hr, 3)
    depletion_factor = np.round(duration_min * avg_hr * np.random.uniform(1.0, 1.15), 1)
    sleep_debt = np.round(baseline_sleep - sleep_hrs_prior, 2)

    calories = round(
        (-55.0969 + 0.6309 * avg_hr + 0.1988 * weight_kg + 0.2017 * age)
        / 4.184 * duration_min * np.random.uniform(1.0, 1.1), 1
    )

    data.append([
        f"R{i:06}", age, sex, weight_kg, vo2_max, resting_hr, baseline_hrv, session_type,
        duration_min, avg_hr, max_hr, race_distance_km, elevation_gain, sleep_hrs_prior,
        hrv_today, temp_c, percent_hr_max, pace_min_per_km, hr_efficiency,
        vo2_hr_ratio, depletion_factor, sleep_debt, calories
    ])

columns = [
    "athlete_id", "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv", "session_type",
    "duration_min", "avg_hr", "max_hr", "distance_km", "elevation_gain_m", "sleep_hrs_prior",
    "hrv_today", "temp_c", "percent_hr_max", "pace_min_per_km", "hr_efficiency",
    "vo2_hr_ratio", "depletion_factor", "sleep_debt", "calories_burned"
]

df_race = pd.DataFrame(data, columns=columns)
df_race.to_csv("race_day_marathon_nonsteady.csv", index=False)
print("✅ Non-steady state race day dataset saved as 'race_day_marathon_nonsteady.csv'")
