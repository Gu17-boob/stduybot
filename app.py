import streamlit as st
import pandas as pd
# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "weather_data" not in st.session_state:
    st.session_state["weather_data"] = None
import requests
from crop_model import (
    train_crop_model,
    predict_crop,
    get_prediction_confidence,
    evaluate_model,
    get_feature_importance,
    get_confusion_matrix
)
from market_model import (
    load_market_data,
    get_crop_data,
    prepare_price_data,
    get_price_statistics,
    get_market_comparison,
    get_price_change,
    get_price_trend,
    get_best_market,
    get_market_summary
)
from market_model import (
    load_market_data,
    validate_market_data,
    get_crop_data,
    prepare_price_data,
    get_price_statistics,
    get_market_comparison,
    get_price_change,
    get_price_trend,
    get_best_market,
    get_market_summary
)
from irrigation_model import calculate_irrigation_need


# -----------------------------
# PAGE SETTINGSfrom crop_model import (
# -----------------------------

st.set_page_config(
    page_title="AI Agriculture",
    page_icon="🌾",
    layout="wide"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🌾 AI Agriculture Intelligence Platform")
st.write(
    "Use soil and environmental information to get an AI-based crop recommendation."
)

st.divider()


# -----------------------------from crop_model import (train_crop_model,
# -----------------------------
# CROP ML MODEL
# -----------------------------

from crop_model import (
    train_crop_model,
    predict_crop,
    get_prediction_confidence
)
# LOAD CROP DATA
# -----------------------------

# -----------------------------
# CROP ML MODEL
# -----------------------------

model, X_test, y_test = train_crop_model()


# -----------------------------
# FARMER INPUT SECTION
# -----------------------------

st.header("🌱 Crop Recommendation")

col1, col2 = st.columns(2)

with col1:
    N = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        value=50.0
    )

    P = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        value=40.0
    )

    K = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        value=40.0
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=25.0
    )

with col2:
    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0
    )

    ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

    rainfall = st.number_input(
        "Recent Rainfall (mm)",
        min_value=0.0,
        value=100.0
    )

    soil_moisture = st.number_input(
        "Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0
    )

growth_stage = st.selectbox(
    "🌱 Crop Growth Stage",
    [
        "Seedling",
        "Vegetative",
        "Flowering",
        "Maturity"
    ]
)

soil_type = st.selectbox(
    "🪨 Soil Type",
    [
        "Sandy",
        "Loamy",
        "Clay",
        "Silty",
        "Black Soil",
        "Red Soil"
    ]
)


# Keep exactly the seven features expected by the crop model.
farmer_data = pd.DataFrame([{
    "N": N,
    "P": P,
    "K": K,
    "temperature": temperature,
    "humidity": humidity,
    "ph": ph,
    "rainfall": rainfall
}])


# -----------------------------
# CROP PREDICTION
# -----------------------------

# ============================================================
# 📊 MARKET INTELLIGENCE
# ============================================================

st.header("📊 Market Intelligence")

try:

    # Load market dataset
    market_data = load_market_data("market_data.csv")

    # Validate dataset
    data_valid, validation_message = validate_market_data(
        market_data
    )

    if not data_valid:

        st.error(
            f"❌ Market data validation failed: "
            f"{validation_message}"
        )

    else:

        st.success(
            f"✅ {validation_message}"
        )

        # Get available crops
        available_crops = sorted(
            market_data["crop"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        if len(available_crops) == 0:

            st.warning(
                "⚠️ No crops are available in the market dataset."
            )

        else:

            selected_market_crop = st.selectbox(
                "🌾 Select Crop for Market Analysis",
                available_crops,
                key="market_crop"
            )

            # Prepare selected crop data
            crop_market_data = prepare_price_data(
                market_data,
                selected_market_crop
            )

            if crop_market_data.empty:

                st.warning(
                    f"⚠️ No valid market data found for "
                    f"{selected_market_crop}."
                )

            else:

                # ------------------------------------------------
                # MARKET SUMMARY
                # ------------------------------------------------

                summary = get_market_summary(
                    market_data,
                    selected_market_crop
                )

                if summary is not None:

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(
                            "💰 Latest Price",
                            f"₹{summary['latest_price']:,.0f}"
                        )

                    with col2:
                        st.metric(
                            "📊 Average Price",
                            f"₹{summary['average_price']:,.0f}"
                        )

                    with col3:
                        st.metric(
                            "⬆️ Highest Price",
                            f"₹{summary['highest_price']:,.0f}"
                        )

                    with col4:
                        st.metric(
                            "⬇️ Lowest Price",
                            f"₹{summary['lowest_price']:,.0f}"
                        )

                    # ------------------------------------------------
                    # PRICE TREND
                    # ------------------------------------------------

                    st.subheader("📈 Price Trend")

                    trend = summary["trend"]

                    if trend == "Increasing":

                        st.success(
                            "📈 Price trend is increasing."
                        )

                    elif trend == "Decreasing":

                        st.warning(
                            "📉 Price trend is decreasing."
                        )

                    elif trend == "Stable":

                        st.info(
                            "➡️ Price trend is stable."
                        )

                    else:

                        st.info(
                            "ℹ️ Insufficient data to determine "
                            "the price trend."
                        )

                    # ------------------------------------------------
                    # PRICE CHANGE
                    # ------------------------------------------------

                    if summary["percentage_change"] is not None:

                        change = summary["price_change"]
                        percentage = summary[
                            "percentage_change"
                        ]

                        st.metric(
                            "📊 Price Change",
                            f"₹{change:,.0f}",
                            f"{percentage:.2f}%"
                        )

                    # ------------------------------------------------
                    # HISTORICAL PRICE CHART
                    # ------------------------------------------------

                    st.subheader(
                        "📈 Historical Price Analysis"
                    )

                    chart_data = crop_market_data[
                        ["date", "price"]
                    ].copy()

                    chart_data = chart_data.set_index(
                        "date"
                    )

                    st.line_chart(
                        chart_data,
                        width="stretch"
                    )

                    # ------------------------------------------------
                    # MARKET COMPARISON
                    # ------------------------------------------------

                    st.subheader(
                        "🏪 Market-wise Price Comparison"
                    )

                    market_prices = get_market_comparison(
                        market_data,
                        selected_market_crop
                    )

                    if not market_prices.empty:

                        market_chart = market_prices.rename(
                            "Average Price"
                        )

                        st.bar_chart(
                            market_chart,
                            width="stretch"
                        )

                        # Best market
                        best_market = get_best_market(
                            market_data,
                            selected_market_crop
                        )

                        if best_market is not None:

                            best_market_name = best_market[0]
                            best_market_price = best_market[1]

                            st.success(
                                f"🏆 Best observed market: "
                                f"**{best_market_name}** "
                                f"with an average price of "
                                f"**₹{best_market_price:,.0f}**."
                            )

                    else:

                        st.info(
                            "No market comparison data available."
                        )

                    # ------------------------------------------------
                    # FARMER MARKET INSIGHT
                    # ------------------------------------------------

                    st.subheader(
                        "🌾 Farmer Market Insight"
                    )

                    latest_price = summary[
                        "latest_price"
                    ]

                    average_price = summary[
                        "average_price"
                    ]

                    if latest_price > average_price:

                        st.info(
                            f"📈 The latest observed price of "
                            f"**₹{latest_price:,.0f}** is above the "
                            f"historical average of "
                            f"**₹{average_price:,.0f}**."
                        )

                    elif latest_price < average_price:

                        st.warning(
                            f"📉 The latest observed price of "
                            f"**₹{latest_price:,.0f}** is below the "
                            f"historical average of "
                            f"**₹{average_price:,.0f}**."
                        )

                    else:

                        st.info(
                            "➡️ The latest observed price is close "
                            "to the historical average."
                        )

                    st.caption(
                        "⚠️ Market insights are based on the "
                        "available historical dataset and are "
                        "not guaranteed future price predictions."
                    )


except FileNotFoundError:

    st.error(
        "❌ market_data.csv was not found. "
        "Make sure it is inside the project folder."
    )

except Exception as e:

    st.error(
        f"❌ Market Intelligence error: {e}"
    )

# -----------------------------
# MARKET INTELLIGENCE
# -----------------------------
st.header("📊 Market Intelligence")

market_data = load_market_data("market_data.csv")

st.divider()
st.header("📊 Market Intelligence")

try:
    market_data = pd.read_csv("market_data.csv")

    st.subheader("Current Crop Prices")
    st.dataframe(
        market_data,
        width="stretch"
    )

    if "Crop" in market_data.columns and "Price" in market_data.columns:
        st.subheader("📈 Crop Price Chart")
        st.bar_chart(
            market_data.set_index("Crop")["Price"]
        )
    else:
        st.warning(
            "market_data.csv must contain 'Crop' and 'Price' columns "
            "to display the price chart."
        )

except FileNotFoundError:
    st.error("❌ market_data.csv was not found.")
except Exception as e:
    st.error(f"❌ Unable to load market data: {e}")


# -----------------------------
# WEATHER INTELLIGENCE
# -----------------------------

st.divider()
st.header("🌦️ Live Weather Intelligence")

st.write(
    "Get current weather information and a 15-day forecast."
)
st.subheader("📍 Farm Location")

city = st.text_input(
    "Enter your city or village",
    value="Guntur",
    
)



if st.button("🌦️ Get Live Weather", key="weather_button"):

    try:
        # -----------------------------
        # STEP 1: FIND CITY COORDINATES
        # -----------------------------

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city.strip(),
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "results" not in geo_data or not geo_data["results"]:
            st.error(
                "❌ City not found. Please enter a valid city name."
            )

        else:
            location = geo_data["results"][0]

            latitude = location["latitude"]
            longitude = location["longitude"]

            city_name = location["name"]
            country = location.get("country", "")

            # -----------------------------
            # STEP 2: GET WEATHER DATA
            # -----------------------------

            weather_url = "https://api.open-meteo.com/v1/forecast"

            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "precipitation,"
                    "rain,"
                    "wind_speed_10m"
                ),
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_sum,"
                    "rain_sum,"
                    "precipitation_probability_max,"
                    "wind_speed_10m_max"
                ),
                "forecast_days": 15,
                "timezone": "auto"
            }

            weather_response = requests.get(
                weather_url,
                params=weather_params,
                timeout=10
            )

            weather_response.raise_for_status()

            weather_data = weather_response.json()

            # Save weather data so Smart Irrigation can use it
            # after Streamlit reruns.
            st.session_state["weather_data"] = weather_data
            st.session_state["weather_city"] = city_name
            st.session_state["weather_country"] = country

            # -----------------------------
            # STEP 3: CURRENT WEATHER
            # -----------------------------

            current = weather_data["current"]

            st.success(
                f"📍 Weather for {city_name}, {country}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🌡️ Temperature",
                    f"{current['temperature_2m']} °C"
                )

            with col2:
                st.metric(
                    "💧 Humidity",
                    f"{current['relative_humidity_2m']} %"
                )

            with col3:
                st.metric(
                    "🌧️ Precipitation",
                    f"{current['precipitation']} mm"
                )

            col4, col5 = st.columns(2)

            with col4:
                st.metric(
                    "🌧️ Rain",
                    f"{current['rain']} mm"
                )

            with col5:
                st.metric(
                    "💨 Wind Speed",
                    f"{current['wind_speed_10m']} km/h"
                )

            # -----------------------------
            # STEP 4: 15-DAY FORECAST
            # -----------------------------


            st.subheader("📅 15-Day Weather Forecast")

            daily = weather_data["daily"]

            forecast_df = pd.DataFrame({
                "Date": daily["time"],
                "Max Temp (°C)": daily["temperature_2m_max"],
                "Min Temp (°C)": daily["temperature_2m_min"],
                "Rain (mm)": daily["rain_sum"],
                "Precipitation (mm)": daily["precipitation_sum"],
                "Rain Probability (%)": daily["precipitation_probability_max"],
                "Max Wind (km/h)": daily["wind_speed_10m_max"]
            })

            st.dataframe(
                forecast_df,
                width="stretch"
            )

            # -----------------------------
            # STEP 5: TEMPERATURE CHART
            # -----------------------------

            st.subheader("🌡️ 15-Day Temperature Forecast")

            temperature_chart = forecast_df.set_index("Date")[
                [
                    "Max Temp (°C)",
                    "Min Temp (°C)"
                ]
            ]

            st.line_chart(temperature_chart)

            # -----------------------------
            # STEP 6: RAINFALL CHART
            # -----------------------------

            st.subheader("🌧️ 15-Day Rainfall Forecast")

            rainfall_chart = forecast_df.set_index("Date")[
                [
                    "Rain (mm)",
                    "Precipitation (mm)"
                ]
            ]

            st.bar_chart(rainfall_chart)

            # -----------------------------
            # STEP 7: FARMING WEATHER ALERT
            # -----------------------------

            st.subheader("🌾 Farming Weather Alert")

            max_rain_probability = max(
                daily["precipitation_probability_max"]
            )

            total_rain = sum(daily["rain_sum"])

            if max_rain_probability >= 70:
                st.warning(
                    f"🌧️ High rain probability detected "
                    f"({max_rain_probability}%). "
                    "Monitor rainfall before irrigation."
                )

            elif total_rain < 20:
                st.warning(
                    "💧 Low rainfall is expected over the "
                    "15-day forecast period. "
                    "Monitor soil moisture."
                )

            else:
                st.success(
                    "🌱 Weather conditions appear relatively moderate. "
                    "Continue monitoring weather updates."
                )

    except requests.exceptions.RequestException as e:
        st.error(
            f"❌ Weather API connection error: {e}"
        )

    except (KeyError, TypeError, ValueError) as e:
        st.error(
            f"❌ Unexpected weather data format: {e}"
        )

    except Exception as e:
        st.error(
            f"❌ Unable to process weather data: {e}"
        )


# -----------------------------
# AI AGRICULTURE ASSISTANT
# -----------------------------

st.divider()
st.header("🤖 AI Agriculture Assistant")

st.write(
    "Ask a question about crops, soil, rainfall, or basic farming decisions."
)

question = st.text_input(
    "Enter your agriculture question:"
)

if st.button("🤖 Ask Assistant", key="assistant_button"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:
        q = question.lower()

        if "rice" in q:
            answer = (
                "Rice generally requires sufficient water and warm growing "
                "conditions. The exact suitability depends on soil, rainfall, "
                "temperature, and local conditions."
            )

        elif "wheat" in q:
            answer = (
                "Wheat generally prefers cooler growing conditions and "
                "well-drained soil. Local climate and soil conditions should "
                "be considered before planting."
            )

        elif "rainfall" in q or "rain" in q:
            answer = (
                "Rainfall is an important factor in crop selection. Too little "
                "water can cause water stress, while excessive rainfall can "
                "cause waterlogging and other problems."
            )

        elif "soil" in q:
            answer = (
                "Soil properties such as nitrogen, phosphorus, potassium, "
                "pH, and moisture are important factors for crop growth."
            )

        elif "fertilizer" in q:
            answer = (
                "Fertilizer requirements depend on the crop and soil condition. "
                "A soil test is recommended before applying fertilizers."
            )

        else:
            answer = (
                "I can help with basic questions about crops, soil, rainfall, "
                "fertilizers, and crop selection. For specific agricultural "
                "problems, consult a qualified local agriculture professional."
            )

        st.success(answer)


# -----------------------------
# AGRICULTURE INSIGHTS
# -----------------------------

st.divider()
st.header("🌱 Agriculture Insights")

st.write(
    "Get a simple explanation based on the farmer's entered conditions."
)

if st.button("📊 Generate Agriculture Insights", key="insights_button"):

    probabilities = model.predict_proba(farmer_data)
    max_probability = probabilities.max()
    confidence = max_probability * 100

    st.subheader("🤖 Model Confidence")
    st.progress(int(confidence))
    st.write(f"Prediction Confidence: {confidence:.2f}%")

    st.subheader("🌧️ Rainfall Analysis")

    if rainfall < 50:
        st.warning("Low rainfall detected. Irrigation may be required.")

    elif rainfall < 150:
        st.info("Moderate rainfall conditions detected.")

    else:
        st.success("High rainfall conditions detected.")

    st.subheader("🧪 Soil Analysis")

    if 6 <= ph <= 7.5:
        st.success("Soil pH is within a generally favorable range.")

    elif ph < 6:
        st.warning(
            "Soil is acidic. Consider soil testing before making amendments."
        )

    else:
        st.warning(
            "Soil is alkaline. Consider soil testing before making amendments."
        )

    st.subheader("💧 Humidity Analysis")

    if humidity < 40:
        st.warning("Low humidity detected.")

    elif humidity <= 80:
        st.success("Humidity is within a moderate range.")

    else:
        st.warning("High humidity detected.")


# -----------------------------
# SMART FARMING RECOMMENDATION
# -----------------------------

st.divider()
st.header("🌾 Smart Farming Recommendation")

st.write(
    "Generate a simple farming recommendation using "
    "the crop prediction and farmer input."
)

if st.button("🌾 Generate Smart Recommendation", key="smart_recommendation_button"):

    recommended_crop = predict_crop(
    model,
    farmer_data
)

    st.subheader("🌱 Recommended Crop")

    st.success(
        f"Based on the entered conditions, the recommended crop is: "
        f"**{recommended_crop.upper()}**"
    )

    # Soil analysis
    st.subheader("🧪 Soil Condition")

    if 6 <= ph <= 7.5:
        soil_status = "Generally favorable"
        st.success(
            f"pH {ph} → {soil_status}"
        )
    else:
        st.warning(
            f"pH {ph} → Soil condition needs attention."
        )

    # Rainfall analysis
    st.subheader("🌧️ Rainfall Condition")

    if rainfall < 50:
        st.warning(
            "Low rainfall. Irrigation may be required."
        )

    elif rainfall <= 150:
        st.info(
            "Moderate rainfall condition."
        )

    else:
        st.warning(
            "High rainfall. Monitor waterlogging risk."
        )

    # Humidity analysis
    st.subheader("💧 Humidity Condition")

    if humidity < 40:
        st.warning("Low humidity detected.")

    elif humidity <= 80:
        st.success(
            "Humidity is within a moderate range."
        )

    else:
        st.warning("High humidity detected.")

    # Final recommendation
    st.subheader("💡 Final Recommendation")

    if rainfall < 50:
        recommendation = (
            f"Consider irrigation planning for {recommended_crop}. "
            "Monitor soil moisture regularly."
        )

    elif rainfall > 150:
        recommendation = (
            f"Monitor excess water conditions for {recommended_crop}. "
            "Ensure proper drainage."
        )

    else:
        recommendation = (
            f"Current rainfall conditions appear reasonable for "
            f"{recommended_crop}. Continue monitoring soil and weather."
        )

    st.info(recommendation)

    st.caption(
        "⚠️ This is an educational decision-support system. "
        "For real farming decisions, verify recommendations with local "
        "agricultural experts and soil/weather data."
    )


# -----------------------------
# SMART IRRIGATION
# -----------------------------

st.divider()
st.header("💧 Smart Irrigation Recommendation")

st.write(
    "Estimate irrigation need using soil moisture, rainfall, "
    "temperature, humidity, crop stage, soil type, and forecast conditions."
)

if st.button(
    "💧 Check Irrigation Need",
    key="irrigation_button"
):

    weather_data = st.session_state.get("weather_data")

    if weather_data is None:
        st.warning(
            "🌦️ Please click 'Get Live Weather' first so the "
            "irrigation module can use the forecast rainfall."
        )

    else:
        try:
            forecast_rainfall = sum(
                weather_data["daily"]["rain_sum"][:3]
            )

            result = calculate_irrigation_need(
                soil_moisture=soil_moisture,
                rainfall=rainfall,
                temperature=temperature,
                humidity=humidity,
                growth_stage=growth_stage,
                soil_type=soil_type,
                forecast_rainfall=forecast_rainfall
            )

            irrigation_level, irrigation_score, recommendation, reasons = result

            st.subheader("💧 Irrigation Status")

            if irrigation_level == "HIGH":
                st.error(
                    f"Irrigation Level: {irrigation_level}"
                )
            elif irrigation_level == "MODERATE":
                st.warning(
                    f"Irrigation Level: {irrigation_level}"
                )
            else:
                st.success(
                    f"Irrigation Level: {irrigation_level}"
                )

            st.metric(
                "Irrigation Score",
                f"{irrigation_score}/10"
            )

            st.subheader("🌧️ Forecast Rainfall")

            st.info(
                f"Expected rainfall over the next 3 days: "
                f"{forecast_rainfall:.1f} mm"
            )

            st.subheader("💡 Recommendation")
            st.info(recommendation)

            st.subheader("🔍 Decision Factors")

            for reason in reasons:
                st.write("•", reason)

            st.caption(
                "⚠️ This is an educational decision-support model. "
                "Actual irrigation should consider crop type, soil moisture, "
                "soil type, growth stage, local weather, and irrigation system."
            )

        except (KeyError, TypeError, ValueError) as e:
            st.error(
                f"❌ Irrigation calculation error: {e}"
            )

        except Exception as e:
            st.error(
                f"❌ Unable to calculate irrigation need: {e}"
            )
            # -----------------------------
# ML MODEL EVALUATION
# -----------------------------

st.divider()

st.header("📊 Crop Model Evaluation")

st.write(
    "Evaluate the performance of the Random Forest crop recommendation model."
)

if st.button(
    "📊 Evaluate Crop Model",
    key="evaluate_crop_model_button"
):

    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    st.subheader("📈 Model Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Accuracy",
            f"{metrics['accuracy'] * 100:.2f}%"
        )

    with col2:
        st.metric(
            "Precision",
            f"{metrics['precision'] * 100:.2f}%"
        )

    with col3:
        st.metric(
            "Recall",
            f"{metrics['recall'] * 100:.2f}%"
        )

    with col4:
        st.metric(
            "F1 Score",
            f"{metrics['f1_score'] * 100:.2f}%"
        )

    # -----------------------------
    # FEATURE IMPORTANCE
    # -----------------------------

    st.subheader("🔍 Feature Importance")

    feature_importance = get_feature_importance(model)

    st.dataframe(
        feature_importance,
        width="stretch"
    )

    st.bar_chart(
        feature_importance.set_index("Feature")
    )
    # ============================================================
# 📊 STEP 4.1 - DATASET ANALYSIS
# ============================================================

st.divider()

st.header("📊 Crop Dataset Analysis")

crop_data = pd.read_csv("crop_recommendation.csv")
duplicate_count = crop_data.duplicated().sum()

st.metric(
    "🔁 Duplicate Rows",
    duplicate_count
)

# Basic information
total_records = len(crop_data)
total_features = len(crop_data.columns) - 1
total_crops = crop_data["label"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📁 Total Records", total_records)

with col2:
    st.metric("🔢 Input Features", total_features)

with col3:
    st.metric("🌾 Crop Classes", total_crops)

# Dataset preview
st.subheader("👀 Dataset Preview")

st.dataframe(
    crop_data.head(10),
    width="stretch"
)

# Crop distribution
st.subheader("🌾 Crop Distribution")

crop_distribution = crop_data["label"].value_counts()

st.bar_chart(crop_distribution)

# Missing values
st.subheader("⚠️ Missing Value Analysis")

missing_values = crop_data.isnull().sum()

missing_df = pd.DataFrame({
    "Column": missing_values.index,
    "Missing Values": missing_values.values
})

st.dataframe(
    missing_df,
    width="stretch"
)
features = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]
duplicate_features = crop_data.duplicated(
    subset=features,
    keep=False
).sum()

st.metric(
    "🔁 Duplicate Feature Rows",
    duplicate_features
)
st.subheader("🔍 Accuracy Investigation")

if duplicate_count == 0:
    st.success(
        "✅ No completely duplicate rows were found in the dataset."
    )
else:
    st.warning(
        f"⚠️ {duplicate_count} duplicate rows were found. "
        "Further investigation is recommended."
    )
if duplicate_features == 0:
    st.success(
        "✅ No duplicate feature combinations were found."
    )
else:
    st.warning(
        f"⚠️ {duplicate_features} duplicate feature rows were found."
    )
    st.subheader("🌧️ Rainfall Intelligence")
    forecast_rainfall = sum(
    weather_data["daily"]["rain_sum"][:3]
)
    st.metric(
    "🌧️ Expected Rainfall — Next 3 Days",
    f"{forecast_rainfall:.1f} mm"
)
    weather_data = st.session_state.get("weather_data")

weather_data = st.session_state.get("weather_data")

if weather_data is not None:
    forecast_rainfall = sum(
        weather_data["daily"]["rain_sum"][:3]
    )






selected_crop = st.selectbox(
    "🌾 Select Crop",
    available_crops
)