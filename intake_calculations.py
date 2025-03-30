# This is meant to find the daily rec. calories for an individual based on these insights
def finding_rec_calories(age, sex, height, weight, goal, sport):
    # Calculate BMR using Mifflin-St Jeor
    if sex == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == 'female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return None

    # Adjust based on goal
    if goal == 'maintain':
        rec_cals = bmr
    elif goal == 'cutting':
        rec_cals = bmr - 200
    elif goal == 'bulking':
        rec_cals = bmr + 200
    else:
        return None

    return rec_cals


#Checking if body_weight == protein grams and what type is less important
def protein_intake_calculator(body_weight, type, grams, sport):
    if type == 'plant':
        target = body_weight * 1.2
        if grams >= target:
            return 'You have met your ' + str(grams) + ' grams of protein goal for the day!'
    elif type == 'animal':
        target = body_weight
        if grams >= target:
            return 'You have met your ' + str(grams) + ' grams of protein goal for the day!'
    else:
        return 'Invalid protein type!'

print(protein_intake_calculator(150, 'animal', 150, 'marathon_running'))

# Add function that adds calories needed after a workout
def calculate_kcal_advanced(hr, age, weight, duration_min, sex,
                            vo2_max=None, hrv=None, baseline_hrv=None):
    # Step 1: Base kcal/min
    if sex == 'male':
        kcal_per_min = (-55.0969 + 0.6309 * hr + 0.1988 * weight + 0.2017 * age) / 4.184
    elif sex == 'female':
        kcal_per_min = (-20.4022 + 0.4472 * hr - 0.1263 * weight + 0.074 * age) / 4.184
    else:
        return None

    # Step 2: VO2max adjustment
    vo2_efficiency_factor = 1.0
    if vo2_max:
        if vo2_max >= 60:
            vo2_efficiency_factor = 0.92
        elif vo2_max >= 50:
            vo2_efficiency_factor = 0.96
        elif vo2_max < 40:
            vo2_efficiency_factor = 1.05

    # Step 3: HRV recovery adjustment
    hrv_factor = 1.0
    if hrv and baseline_hrv:
        hrv_ratio = hrv / baseline_hrv
        if hrv_ratio < 0.85:
            hrv_factor = 1.08
        elif hrv_ratio > 1.10:
            hrv_factor = 0.95

    # Step 4: Combine all
    total_kcal = kcal_per_min * duration_min * vo2_efficiency_factor * hrv_factor

    return round(total_kcal, 2)
print(calculate_kcal_advanced(173, 23, 74.84, 24.35, 'male', 52, 78, 82))