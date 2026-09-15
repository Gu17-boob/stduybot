# 🌾 AI Agriculture Intelligence Platform

An AI-powered agriculture intelligence platform designed to help farmers make better decisions using **Machine Learning, weather intelligence, market analysis, and smart irrigation recommendations**.

The platform combines multiple agriculture-focused modules into a single Streamlit application.

---

## 🎯 Problem Statement

Farmers often face difficulties in making timely decisions about:

- 🌱 Which crop to grow
- 🌦️ How weather conditions may affect farming
- 💧 When irrigation may be required
- 📊 Which market may offer better prices
- 📈 Understanding crop price trends

This project aims to provide these insights through a simple and accessible digital platform.

---

## ✨ Features

### 🌱 1. Crop Recommendation

Uses a **Random Forest Classifier** to recommend a suitable crop based on:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

The model also provides prediction confidence and evaluation metrics.

---

### 🌦️ 2. Live Weather Intelligence

Provides live weather information using the **Open-Meteo API**.

The application can display:

- Current temperature
- Weather conditions
- Rainfall information
- Humidity
- Weather alerts

---

### 📅 3. Weather Forecast

Provides a multi-day weather forecast to help farmers understand upcoming conditions.

The system analyzes expected rainfall and temperature conditions.

---

### 🌧️ 4. Rainfall Analysis

Analyzes expected rainfall and provides farming-oriented insights.

Example:

- Significant rainfall → avoid unnecessary irrigation
- Moderate rainfall → monitor soil moisture
- Low rainfall → monitor irrigation requirements

---

### 🌡️ 5. Temperature Intelligence

The application analyzes temperature conditions and provides farming alerts.

For example:

- High temperature → possible heat stress
- Warm conditions → monitor soil moisture
- Moderate temperature → relatively normal conditions

---

### 💧 6. Smart Irrigation

The Smart Irrigation module uses a transparent rule-based decision engine.

It considers:

- Soil moisture
- Recent rainfall
- Expected rainfall
- Temperature
- Humidity
- Crop growth stage
- Soil type

The system generates:

- Irrigation level
- Irrigation score
- Recommendation
- Reasons behind the recommendation

Possible outputs:

- 🟢 LOW
- 🟡 MODERATE
- 🔴 HIGH

> The irrigation module currently uses a rule-based approach rather than claiming an ML model without a suitable irrigation dataset.

---

### 📊 7. Market Intelligence

The Market Intelligence module analyzes crop price data.

It provides:

- Latest observed price
- Average price
- Highest price
- Lowest price
- Historical price trend
- Market comparison
- Best observed market
- Price volatility
- Market price spread
- Farmer-oriented market insights
- Selling recommendation

---

### 🤖 8. AI Agriculture Assistant

Provides agriculture-oriented assistance using the information available within the application.

The assistant is designed as a foundation for future **Generative AI and Agentic AI capabilities**.

---

### 📈 9. ML Model Evaluation

The crop recommendation model includes evaluation capabilities such as:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
- Feature Importance
- Cross-validation

---

### 📊 10. Dataset Analysis

The application provides analysis of the crop recommendation dataset to understand:

- Dataset characteristics
- Feature distributions
- Crop classes
- Important features
- Model-related patterns

---

## 🏗️ Project Architecture

```text
                    🌾 AI Agriculture Intelligence
                              │
                              ▼
                       Streamlit Application
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    🌱 Crop ML          🌦️ Weather          📊 Market
    Recommendation      Intelligence        Intelligence
          │                   │                   │
          ▼                   ▼                   ▼
   Random Forest        Open-Meteo API       Market Dataset
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                       💧 Smart Irrigation
                              │
                              ▼
                     🌾 Farmer Insights