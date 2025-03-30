
import pandas as pd
import numpy as np

np.random.seed(42)

rows = 500_000
baseline_sleep = 8.0

data = []
for i in range(1, rows + 1):
    age = np.random.randint(20, 45)
    sex = np.random.choice(["M", "F"])
    weight_kg = np.round(np.random.uniform(55, 90), 1)
    vo2_max = np.round(np.random.uniform(38, 65), 1)
    resting_hr = np.random.randint(45, 65)
    baseline_hrv = np.random.randint(60, 100)

    duration_min = np.random.randint(30, 120)
    avg_hr = np.random.randint(130, 180)
    max_hr = avg_hr + np.random.randint(5, 20)
    distance_km = np.round(duration_min * np.random.uniform(0.1, 0.2), 1)
    elevation_gain = np.random.randint(0, 300)
    session_type = np.random.choice(["long_run", "tempo", "intervals"])
    sleep_hrs_prior = np.round(np.random.uniform(4.5, 9), 1)
    hrv_today = np.round(baseline_hrv * np.random.uniform(0.7, 1.15), 1)
    temp_c = np.random.randint(10, 35)

    percent_hr_max = np.round(avg_hr / max_hr, 3)
    pace_min_per_km = np.round(duration_min / distance_km, 2)
    hr_efficiency = np.round(avg_hr / distance_km, 2)
    vo2_hr_ratio = np.round(vo2_max / avg_hr, 3)
    depletion_factor = np.round(duration_min * avg_hr * np.random.uniform(0.95, 1.05), 1)
    sleep_debt = np.round(baseline_sleep - sleep_hrs_prior, 2)

    calories = round(
        (-55.0969 + 0.6309 * avg_hr + 0.1988 * weight_kg + 0.2017 * age)
        / 4.184 * duration_min * np.random.uniform(0.95, 1.05), 1
    )

    data.append([
        f"A{i:06}", age, sex, weight_kg, vo2_max, resting_hr, baseline_hrv, session_type,
        duration_min, avg_hr, max_hr, distance_km, elevation_gain, sleep_hrs_prior,
        hrv_today, temp_c, percent_hr_max, pace_min_per_km, hr_efficiency,
        vo2_hr_ratio, depletion_factor, sleep_debt, calories
    ])

columns = [
    "athlete_id", "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv", "session_type",
    "duration_min", "avg_hr", "max_hr", "distance_km", "elevation_gain_m", "sleep_hrs_prior",
    "hrv_today", "temp_c", "percent_hr_max", "pace_min_per_km", "hr_efficiency",
    "vo2_hr_ratio", "depletion_factor", "sleep_debt", "calories_burned"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("mock_athlete_data_500k.csv", index=False)
print("✅ Dataset with 500,000 entries saved as 'mock_athlete_data_500k.csv'")
