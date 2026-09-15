import pandas as pd


# ============================================================
# LOAD MARKET DATA
# ============================================================

def load_market_data(file_path="market_data.csv"):
    """
    Load market data from CSV
    and clean column names.
    """

    data = pd.read_csv(file_path)

    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return data
def validate_market_data(data):
    """
    Validate the basic structure of the market dataset.
    """

    required_columns = [
        "date",
        "crop",
        "market",
        "price"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        return False, (
            f"Missing required columns: {missing_columns}"
        )

    if data.empty:
        return False, "Market dataset is empty."

    return True, "Market data is valid."

# ============================================================
# GET DATA FOR SELECTED CROP
# ============================================================

def get_crop_data(data, crop):
    """
    Return market data for the selected crop.
    """

    if "crop" not in data.columns:
        raise ValueError(
            "The market dataset must contain a 'crop' column."
        )

    crop_data = data[
        data["crop"].astype(str).str.strip().str.casefold()
        == str(crop).strip().casefold()
    ].copy()

    return crop_data


# ============================================================
# PREPARE PRICE DATA
# ============================================================

def prepare_price_data(data, crop):
    """
    Prepare historical market price data.
    """

    crop_data = get_crop_data(data, crop)

    if crop_data.empty:
        return crop_data

    if "date" not in crop_data.columns:
        raise ValueError(
            "The market dataset must contain a 'date' column."
        )

    if "price" not in crop_data.columns:
        raise ValueError(
            "The market dataset must contain a 'price' column."
        )

    crop_data["date"] = pd.to_datetime(
        crop_data["date"],
        errors="coerce"
    )

    crop_data["price"] = pd.to_numeric(
        crop_data["price"],
        errors="coerce"
    )

    crop_data = crop_data.dropna(
        subset=["date", "price"]
    )

    crop_data = crop_data[
        crop_data["price"] >= 0
    ]

    crop_data = crop_data.sort_values(
        by="date"
    )

    return crop_data


# ============================================================
# PRICE STATISTICS
# ============================================================

def get_price_statistics(data, crop):
    """
    Calculate latest, average, highest,
    and lowest price.
    """

    crop_data = prepare_price_data(data, crop)

    if crop_data.empty:
        return None

    return {
        "latest": float(crop_data["price"].iloc[-1]),
        "average": float(crop_data["price"].mean()),
        "highest": float(crop_data["price"].max()),
        "lowest": float(crop_data["price"].min())
    }


# ============================================================
# MARKET COMPARISON
# ============================================================

def get_market_comparison(data, crop):
    """
    Calculate average price for each market.
    """

    crop_data = prepare_price_data(data, crop)

    if crop_data.empty:
        return pd.Series(dtype="float64")

    if "market" not in crop_data.columns:
        return pd.Series(dtype="float64")

    crop_data["market"] = (
        crop_data["market"]
        .astype(str)
        .str.strip()
    )

    crop_data = crop_data[
        (crop_data["market"].str.lower() != "nan")
        & (crop_data["market"] != "")
    ]

    if crop_data.empty:
        return pd.Series(dtype="float64")

    return (
        crop_data
        .groupby("market")["price"]
        .mean()
        .sort_values(ascending=False)
    )


# ============================================================
# PRICE CHANGE
# ============================================================

def get_price_change(data, crop):
    """
    Calculate price change from first
    recorded price to latest price.
    """

    crop_data = prepare_price_data(data, crop)

    if len(crop_data) < 2:
        return None

    first_price = float(crop_data["price"].iloc[0])
    latest_price = float(crop_data["price"].iloc[-1])

    if first_price == 0:
        return None

    price_change = latest_price - first_price

    percentage_change = (
        price_change / first_price
    ) * 100

    return (
        float(price_change),
        float(percentage_change)
    )


# ============================================================
# PRICE TREND
# ============================================================

def get_price_trend(data, crop):
    """
    Return Increasing, Decreasing,
    Stable, or Insufficient Data.
    """

    result = get_price_change(data, crop)

    if result is None:
        return "Insufficient Data"

    _, percentage_change = result

    if percentage_change > 0:
        return "Increasing"

    elif percentage_change < 0:
        return "Decreasing"

    return "Stable"


# ============================================================
# BEST MARKET
# ============================================================

def get_best_market(data, crop):
    """
    Return the market with the highest
    average price.
    """

    market_prices = get_market_comparison(
        data,
        crop
    )

    if market_prices.empty:
        return None

    best_market = market_prices.index[0]
    best_price = float(market_prices.iloc[0])

    return (
        best_market,
        best_price
    )


# ============================================================
# MARKET SUMMARY
# ============================================================

def get_market_summary(data, crop):
    """
    Return complete market intelligence
    for the selected crop.
    """

    statistics = get_price_statistics(
        data,
        crop
    )

    if statistics is None:
        return None

    price_change = get_price_change(
        data,
        crop
    )

    trend = get_price_trend(
        data,
        crop
    )

    best_market = get_best_market(
        data,
        crop
    )

    summary = {
        "crop": crop,
        "latest_price": statistics["latest"],
        "average_price": statistics["average"],
        "highest_price": statistics["highest"],
        "lowest_price": statistics["lowest"],
        "trend": trend
    }

    if price_change is not None:
        change, percentage = price_change

        summary["price_change"] = change
        summary["percentage_change"] = percentage
    else:
        summary["price_change"] = None
        summary["percentage_change"] = None

    if best_market is not None:
        summary["best_market"] = best_market[0]
        summary["best_market_price"] = best_market[1]
    else:
        summary["best_market"] = None
        summary["best_market_price"] = None

    return summary

# ============================================================
# PRICE VOLATILITY
# ============================================================

def get_price_volatility(data, crop):
    """
    Calculate price volatility using the standard deviation
    of historical prices.
    """

    crop_data = prepare_price_data(data, crop)

    if len(crop_data) < 2:
        return None

    volatility = crop_data["price"].std()

    return float(volatility)
# ============================================================
# MARKET SPREAD
# ============================================================

def get_market_spread(data, crop):
    """
    Calculate the difference between the highest
    and lowest average market prices.
    """

    market_prices = get_market_comparison(data, crop)

    if len(market_prices) < 2:
        return None

    highest_market_price = float(
        market_prices.max()
    )

    lowest_market_price = float(
        market_prices.min()
    )

    spread = (
        highest_market_price
        - lowest_market_price
    )

    return float(spread)
def get_farmer_selling_recommendation(data, crop):
    summary = get_market_summary(data, crop)

    if summary is None:
        return None

    best_market = summary["best_market"]
    best_price = summary["best_market_price"]
    latest_price = summary["latest_price"]
    trend = summary["trend"]

    if best_market is None:
        return {
            "recommendation": "Insufficient market data",
            "reason": "No reliable market comparison is available."
        }

    if trend == "Increasing":
        recommendation = f"Consider selling at {best_market} if transport and other costs are acceptable."
        reason = "The observed price trend is increasing and this market has the highest average price."

    elif trend == "Decreasing":
        recommendation = f"Consider selling sooner at {best_market} rather than waiting too long."
        reason = "The observed price trend is decreasing and this market currently has the highest average price."

    else:
        recommendation = f"Compare selling costs and consider {best_market}."
        reason = "Prices are relatively stable, so transport and transaction costs become important."

    return {
        "recommendation": recommendation,
        "reason": reason,
        "best_market": best_market,
        "best_price": best_price,
        "latest_price": latest_price,
        "trend": trend
    }