import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from lightgbm import LGBMRegressor

# --- Load engineered dataset ---
df = pd.read_csv("combined_with_engineered_features.csv")

# --- Encode categorical variables ---
encoder_sex = LabelEncoder().fit(df["sex"])
encoder_session = LabelEncoder().fit(df["session_type"])
df["sex"] = encoder_sex.transform(df["sex"])
df["session_type"] = encoder_session.transform(df["session_type"])

# --- Feature list (includes engineered features) ---
features = [
    "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv",
    "avg_hr", "max_hr", "distance_km", "duration_min", "elevation_gain_m",
    "sleep_hrs_prior", "hrv_today", "temp_c", "session_type",
    "hr_fluctuation", "fatigue_index", "depletion_score"
]
target = "calories_burned"

# --- Train/test split ---
X = df[features]
y = df[target]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# --- LightGBM model (tuned params) ---
model = LGBMRegressor(
    n_estimators=300,
    learning_rate=0.03,
    max_depth=7,
    num_leaves=32,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# --- Evaluate on validation set ---
y_val_pred = model.predict(X_val)
mae_val = mean_absolute_error(y_val, y_val_pred)
r2_val = r2_score(y_val, y_val_pred)

print("📊 LightGBM (Engineered Features) — Validation Set")
print(f"MAE: {mae_val:.2f} kcal")
print(f"R² Score: {r2_val:.3f}")

import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load your trained model
model = joblib.load("lightgbm_calorie_model.pkl")

# Match feature list used during training
features = [
    "age", "sex", "weight_kg", "vo2_max", "resting_hr", "baseline_hrv",
    "avg_hr", "max_hr", "distance_km", "duration_min", "elevation_gain_m",
    "sleep_hrs_prior", "hrv_today", "temp_c", "session_type",
    "hr_fluctuation", "fatigue_index", "depletion_score"
]

# Create importance dataframe
importances = model.feature_importances_
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=importance_df, x="Importance", y="Feature", palette="viridis")
plt.title("🔍 Feature Importance — LightGBM Calorie Model")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()
plt.grid(True)
plt.show()


#import joblib

# Save the trained model to a file
#joblib.dump(model, "lightgbm_calorie_model.pkl")
#print("✅ Model saved as 'lightgbm_calorie_model.pkl'")
#joblib.dump(encoder_sex, "encoder_sex.pkl")
#joblib.dump(encoder_session, "encoder_session.pkl")

