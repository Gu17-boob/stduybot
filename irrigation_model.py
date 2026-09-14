def calculate_irrigation_need(
    soil_moisture,
    rainfall,
    temperature,
    humidity,
    growth_stage,
    soil_type,
    forecast_rainfall
):
    """
    Explainable rule-based irrigation decision engine.

    Returns:
        irrigation_level: HIGH / MODERATE / LOW
        score: 0-10
        recommendation: human-readable recommendation
        reasons: list of factors used in the decision
    """

    score = 0
    reasons = []

    # -----------------------------
    # SOIL MOISTURE
    # -----------------------------

    if soil_moisture < 25:
        score += 4
        reasons.append("Very low soil moisture")

    elif soil_moisture < 40:
        score += 3
        reasons.append("Low soil moisture")

    elif soil_moisture < 60:
        score += 1
        reasons.append("Moderate soil moisture")

    else:
        reasons.append("Adequate soil moisture")

    # -----------------------------
    # RECENT RAINFALL
    # -----------------------------

    if rainfall < 10:
        score += 2
        reasons.append("Very little recent rainfall")

    elif rainfall < 50:
        score += 1
        reasons.append("Limited recent rainfall")

    else:
        score -= 1
        reasons.append("Good recent rainfall")

    # -----------------------------
    # FORECAST RAINFALL
    # -----------------------------

    if forecast_rainfall >= 50:
        score -= 3
        reasons.append("Significant rainfall is expected")

    elif forecast_rainfall >= 20:
        score -= 1
        reasons.append("Some rainfall is expected")

    else:
        score += 2
        reasons.append("Little rainfall is expected")

    # -----------------------------
    # TEMPERATURE
    # -----------------------------

    if temperature >= 35:
        score += 3
        reasons.append("High temperature")

    elif temperature >= 30:
        score += 2
        reasons.append("Warm temperature")

    elif temperature < 20:
        score -= 1
        reasons.append("Cool temperature")

    # -----------------------------
    # HUMIDITY
    # -----------------------------

    if humidity < 40:
        score += 2
        reasons.append("Low humidity")

    elif humidity < 60:
        score += 1
        reasons.append("Moderate humidity")

    else:
        score -= 1
        reasons.append("High humidity")

    # -----------------------------
    # CROP GROWTH STAGE
    # -----------------------------

    growth_stage_scores = {
        "Seedling": 1,
        "Vegetative": 2,
        "Flowering": 3,
        "Maturity": 1
    }

    stage_score = growth_stage_scores.get(
        growth_stage,
        1
    )

    score += stage_score
    reasons.append(
        f"{growth_stage} growth stage"
    )

    # -----------------------------
    # SOIL TYPE
    # -----------------------------

    if soil_type == "Sandy":
        score += 2
        reasons.append(
            "Sandy soil drains water quickly"
        )

    elif soil_type == "Loamy":
        reasons.append(
            "Loamy soil generally has balanced water retention"
        )

    elif soil_type == "Clay":
        score -= 1
        reasons.append(
            "Clay soil generally retains water longer"
        )

    elif soil_type == "Silty":
        reasons.append(
            "Silty soil has moderate water retention"
        )

    elif soil_type == "Black Soil":
        score -= 1
        reasons.append(
            "Black soil generally has good water retention"
        )

    elif soil_type == "Red Soil":
        score += 1
        reasons.append(
            "Red soil may have relatively lower water retention"
        )

    # -----------------------------
    # NORMALIZE SCORE
    # -----------------------------

    score = max(
        0,
        min(score, 10)
    )

    # -----------------------------
    # FINAL DECISION
    # -----------------------------

    if score >= 7:
        irrigation_level = "HIGH"
        recommendation = (
            "Irrigation may be required. "
            "Check actual soil moisture before applying water."
        )

    elif score >= 4:
        irrigation_level = "MODERATE"
        recommendation = (
            "Monitor soil moisture and weather conditions "
            "before deciding on irrigation."
        )

    else:
        irrigation_level = "LOW"
        recommendation = (
            "Irrigation demand appears relatively low. "
            "Avoid unnecessary watering."
        )

    return (
        irrigation_level,
        score,
        recommendation,
        reasons
    )
