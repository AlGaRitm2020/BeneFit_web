from math import log10


def calculate_BMI(weight: int, height: int) -> float:
    return round(weight / (height / 100) ** 2, 1)


def calculate_max_heart_rate(age: int) -> int:
    return 220 - age


def calculate_training_heart_rate_min(age: int) -> int:
    return round((220 - age) * 0.65)


def calculate_training_heart_rate_max(age: int) -> int:
    return round((220 - age) * 0.85)


def calculate_water(weight: int, gender: str, activity: int) -> float:
    if gender == 'Мужской':
        return round((weight * 34.92 + activity * 251) / 1000, 1)
    else:
        return round((weight * 31.71 + activity * 251) / 1000, 1)


def calculate_physical_activity_quotient(activity: int) -> float:
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


def calculate_calories(weight: int, height: int, age: int, gender: str,
                       physical_activity_quotient: float) -> float:
    if gender == 'Мужской':
        return round(
            (((weight * 10) + (height * 6.25) - (age * 5)) + 5) * physical_activity_quotient)
    else:
        return round(
            (((weight * 10) + (height * 6.25) - (age * 5)) - 161) * physical_activity_quotient)


def calculate_body_type(wrists: int, gender: str) -> str:
    if wrists < 18 and gender == 'Мужской' or wrists < 15 and not gender == 'Мужской':
        return "Эктоморф"
    elif wrists > 20 and gender == 'Мужской' or wrists > 17 and not gender == 'Мужской':
        return 'Эндоморф'
    else:
        return "Мезоморф"

def calculate_body_fat_percent(height: int, waist: int, neck: int, hip: int, gender: str) -> float:
    if gender == 'Мужской':
        return round(
            495 / (1.0324 - 0.19077 * (log10(waist - neck)) + 0.15456 * (log10(height))) - 450.1, 1)
    else:
        return round(
            495 / (1.29579 - 0.35004 * (log10(waist + hip - neck)) + 0.22100 * (
                log10(height))) - 450, 1)
