from math import log10


def calculate_BMI(weight, height):
    return round(weight / (height / 100) ** 2, 1)


def calculate_max_heart_rate(age):
    return 220 - age


def calculate_training_heart_rate_min(age):
    return round((220 - age) * 0.65)


def calculate_training_heart_rate_max(age):
    return round((220 - age) * 0.85)


def calculate_water(weight, gender, activity):
    if gender == 'Мужской':
        return round((weight * 34.92 + activity * 251) / 1000, 1)
    else:
        return round((weight * 31.71 + activity * 251) / 1000, 1)


def calculate_physical_activity_quotient(activity):
    if activity == 0:
        return 1.2
    elif activity == 1:
        return 1.375
    elif activity == 2:
        return 1.55
    elif activity == 3:
        return 1.725
    else:
        return 1.9


def calculate_calories(weight, height, age, gender, physical_activity_quotient):
    if gender == 'Мужской':
        return round(
            (((weight * 10) + (height * 6.25) - (age * 5)) + 5) * physical_activity_quotient)
    else:
        return round(
            (((weight * 10) + (height * 6.25) - (age * 5)) - 161) * physical_activity_quotient)


def calculate_body_type(wrists, gender):
    if wrists < 18 and gender == 'Мужской' or wrists < 15 and not gender == 'Мужской':
        return "Эктоморф"
    elif wrists > 20 and gender == 'Мужской' or wrists > 17 and not gender == 'Мужской':
        return 'Эндоморф'
    else:
        return "Мезоморф"


def calculate_body_fat_percent(height, waist, neck, hip, gender):
    if gender == 'Мужской':
        return round(
            495 / (1.0324 - 0.19077 * (log10(waist - neck)) + 0.15456 * (log10(height))) - 450.1, 1)
    else:
        return round(
            495 / (1.29579 - 0.35004 * (log10(waist + hip - neck)) + 0.22100 * (
                log10(height))) - 450, 1)
