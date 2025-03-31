# 🏃‍♂️ Endurithm

**Precision fueling. Powered by your physiology.**

Endurithm is a smart athlete fueling platform designed for endurance sports. It uses a machine learning engine trained on thousands of synthetic and non-steady state workout sessions to estimate calories burned and generate personalized macronutrient breakdowns — tailored to your goal, sport, and session type.

---

## 🚀 Features

- ⚙️ **LightGBM-powered calorie prediction model**
- 🧍 **User-driven athlete profiles** (age, weight, VO₂ max, HR, etc.)
- 📊 **Custom workout input** (duration, HR, session type, elevation, sleep, etc.)
- 🧠 **SHAP-based transparency** showing what drove the prediction
- 🧪 **Goal-aware macro planner** (cutting, maintain, bulking)
- 📝 **Fueling session logger + visualization**
- ☁️ Deployed via Streamlit for accessible web-based use

---

## 🧬 How It Works

1. **You enter** your athlete profile + specific workout session.
2. **Endurithm predicts** how many calories you burned using its trained ML model.
3. **It recommends** how much to replenish — and how to split it into carbs, protein, and fats based on your sport and goals.
4. **You get SHAP feedback** to understand why that prediction was made.

---

## 🖥 Tech Stack

- `Python` · `pandas` · `LightGBM` · `scikit-learn`
- `SHAP` for model interpretation
- `Streamlit` for frontend
- `joblib` for model + encoder storage

---

## 📂 Repository Structure

├── app.py # Streamlit UI ├── lightgbm_calorie_model.pkl ├── encoder_sex.pkl ├── encoder_session.pkl ├── fueling_engine.py # Macro + goal logic ├── goal_logic.py # Validation for goal and weight ├── rebuild_encoder.py # Regenerates label encoders  └── requirements.txt

----
🧭 Roadmap

🥗 Meal recommendation from macro output
📅 Weekly fueling planner
⌚ Garmin/WHOOP integration comparison mode
📲 Mobile layout optimization
📤 CSV batch prediction uploads



🧠 Built by

Derek Brechler

Founder of Endurithm
