import joblib
from sklearn.preprocessing import LabelEncoder

# List the valid session types you want to encode
session_types = ["long_run", "tempo", "intervals"]

# Fit encoder and save
encoder = LabelEncoder()
encoder.fit(session_types)

joblib.dump(encoder, "encoder_session.pkl")
print("✅ Saved updated encoder_session.pkl with:", encoder.classes_)
