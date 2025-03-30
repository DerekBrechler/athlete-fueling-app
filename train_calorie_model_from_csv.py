
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# --- Load datasets ---
df_train = pd.read_csv("mock_athlete_data_500k.csv")
df_race = pd.read_csv("race_day_marathon_nonsteady.csv")

# --- Combine categories for encoding ---
combined_session_types = pd.concat([df_train["session_type"], df_race["session_type"]])
combined_sex = pd.concat([df_train["sex"], df_race["sex"]])

encoder_sex = LabelEncoder().fit(combined_sex)
encoder_session = LabelEncoder().fit(combined_session_types)

# --- Encode categorical variables consistently ---
df_train["sex"] = encoder_sex.transform(df_train["sex"])
df_train["session_type"] = encoder_session.transform(df_train["session_type"])

df_race["sex"] = encoder_sex.transform(df_race["sex"])
df_race["session_type"] = encoder_session.transform(df_race["session_type"])

# --- Select features and target ---
features = [
    "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv", "avg_hr", "max_hr",
    "distance_km", "duration_min", "elevation_gain_m", "sleep_hrs_prior", "hrv_today",
    "temp_c", "session_type"
]
target = "calories_burned"

X_train = df_train[features]
y_train = df_train[target]
X_race = df_race[features]
y_race = df_race[target]

# --- Train the model ---
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# --- Predict on race day data ---
y_race_pred = model.predict(X_race)

mae_race = mean_absolute_error(y_race, y_race_pred)
r2_race = r2_score(y_race, y_race_pred)

print("📊 Performance on Non-Steady State Race Day Data")
print(f"MAE: {mae_race:.2f} kcal")
print(f"R² Score: {r2_race:.2f}")

# --- Attach predictions to dataframe for analysis ---
df_race["actual"] = y_race
df_race["predicted"] = y_race_pred
df_race["error"] = df_race["actual"] - df_race["predicted"]
df_race["abs_error"] = df_race["error"].abs()

# --- Visualization ---

# 1. Predicted vs Actual
plt.figure(figsize=(8, 6))
plt.scatter(df_race["actual"], df_race["predicted"], alpha=0.3, s=10)
plt.plot([df_race["actual"].min(), df_race["actual"].max()],
         [df_race["actual"].min(), df_race["actual"].max()],
         color="red", linestyle="--")
plt.xlabel("Actual Calories Burned")
plt.ylabel("Predicted Calories Burned")
plt.title("Race Day Predictions vs Actuals")
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Residual Histogram
plt.figure(figsize=(8, 5))
plt.hist(df_race["error"], bins=50, color="salmon", edgecolor="black")
plt.axvline(0, color="red", linestyle="--")
plt.title("Race Day Residuals Distribution")
plt.xlabel("Error (Actual - Predicted)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 3. Error vs Duration
plt.figure(figsize=(8, 5))
plt.scatter(df_race["duration_min"], df_race["error"], alpha=0.3, s=10)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Duration (min)")
plt.ylabel("Prediction Error")
plt.title("Prediction Error vs Duration (Race Day)")
plt.grid(True)
plt.tight_layout()
plt.show()
