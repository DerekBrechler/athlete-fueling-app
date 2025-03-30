# plot_log.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the logged fueling sessions
log_file = "fueling_log.csv"
df = pd.read_csv(log_file)

# Optional: sort by timestamp if you add one later
# df = df.sort_values("timestamp")

# Line plot: Calories Burned Over Sessions
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x=range(len(df)), y="calories_burned", marker="o")
plt.title("Calories Burned Over Logged Sessions")
plt.xlabel("Session Number")
plt.ylabel("Calories Burned (kcal)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Bar plot: Macronutrient Breakdown per Session
df_plot = df[["carbs_g", "protein_g", "fat_g"]]
df_plot.plot(kind="bar", stacked=True, figsize=(10, 6))
plt.title("Macronutrient Breakdown Per Session")
plt.xlabel("Session Number")
plt.ylabel("Grams of Macronutrients")
plt.legend(title="Macros")
plt.tight_layout()
plt.show()
