import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --- Load your saved dataset ---
df_nonsteady_train = pd.read_csv("nonsteady_train_250k.csv")

# --- Encode categorical variables ---
encoder_sex = LabelEncoder().fit(df_nonsteady_train["sex"])
encoder_session = LabelEncoder().fit(df_nonsteady_train["session_type"])

df_nonsteady_train["sex"] = encoder_sex.transform(df_nonsteady_train["sex"])
df_nonsteady_train["session_type"] = encoder_session.transform(df_nonsteady_train["session_type"])

# --- Select features and target ---
features = [
    "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv", "avg_hr", "max_hr",
    "distance_km", "duration_min", "elevation_gain_m", "sleep_hrs_prior", "hrv_today",
    "temp_c", "session_type"
]
target = "calories_burned"

X_ns = df_nonsteady_train[features]
y_ns = df_nonsteady_train[target]

# --- Train the model ---
model_ns = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model_ns.fit(X_ns, y_ns)

# --- Evaluate model on training set (or split later if you want) ---
y_pred_ns = model_ns.predict(X_ns)
mae_ns = mean_absolute_error(y_ns, y_pred_ns)
r2_ns = r2_score(y_ns, y_pred_ns)

print("📊 Model Trained on Non-Steady State Dataset (250K)")
print(f"MAE: {mae_ns:.2f} kcal")
print(f"R² Score: {r2_ns:.2f}")

from sklearn.model_selection import train_test_split

X_train_ns, X_test_ns, y_train_ns, y_test_ns = train_test_split(X_ns, y_ns, test_size=0.2, random_state=42)

model_ns.fit(X_train_ns, y_train_ns)
y_pred_test_ns = model_ns.predict(X_test_ns)

mae_test = mean_absolute_error(y_test_ns, y_pred_test_ns)
r2_test = r2_score(y_test_ns, y_pred_test_ns)

print("📊 Performance on Non-Steady *Test* Set")
print(f"MAE: {mae_test:.2f} kcal")
print(f"R² Score: {r2_test:.3f}")
