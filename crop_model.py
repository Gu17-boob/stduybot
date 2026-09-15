import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# =========================================================
# 1. LOAD DATASET
# =========================================================

def load_crop_data(file_path="crop_recommendation.csv"):

    data = pd.read_csv(file_path)

    X = data.drop("label", axis=1)
    y = data["label"]

    print("Dataset loaded successfully!")

    return X, y


# =========================================================
# 2. TRAIN CROP MODEL
# =========================================================

def train_crop_model(file_path="crop_recommendation.csv"):

    X, y = load_crop_data(file_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    print("Model trained successfully!")

    return model, X_test, y_test


# =========================================================
# 3. PREDICT CROP
# =========================================================

def predict_crop(model, farmer_data):

    prediction = model.predict(farmer_data)

    return prediction[0]


# =========================================================
# 4. GET PREDICTION CONFIDENCE
# =========================================================

def get_prediction_confidence(model, farmer_data):

    probabilities = model.predict_proba(farmer_data)

    confidence = probabilities.max() * 100

    return confidence


# =========================================================
# 5. MODEL EVALUATION
# =========================================================

def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


# =========================================================
# 6. FEATURE IMPORTANCE
# =========================================================

def get_feature_importance(model):

    feature_importance = pd.DataFrame({
        "Feature": model.feature_names_in_,
        "Importance": model.feature_importances_
    })

    feature_importance = feature_importance.sort_values(
        by="Importance",
        ascending=False
    )

    return feature_importance


# =========================================================
# 7. TEST THE MODEL
# =========================================================

if __name__ == "__main__":

    print("\n======================================")
    print("🌾 AI AGRICULTURE CROP MODEL")
    print("======================================")

    # Train model
    model, X_test, y_test = train_crop_model()

    # Evaluate model
    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    print("\n======================================")
    print("📊 MODEL PERFORMANCE")
    print("======================================")

    print(
        f"Accuracy: {metrics['accuracy'] * 100:.2f}%"
    )

    print(
        f"Precision: {metrics['precision'] * 100:.2f}%"
    )

    print(
        f"Recall: {metrics['recall'] * 100:.2f}%"
    )

    print(
        f"F1 Score: {metrics['f1_score'] * 100:.2f}%"
    )

    # Feature importance
    print("\n======================================")
    print("🔍 FEATURE IMPORTANCE")
    print("======================================")

    print(
        get_feature_importance(model).to_string(
            index=False
        )
    )
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average="weighted")
    recall = recall_score(y_test, predictions, average="weighted")
    f1 = f1_score(y_test, predictions, average="weighted")

    return accuracy, precision, recall, f1

def get_confusion_matrix(model, X_test, y_test):
    predictions = model.predict(X_test)

    matrix = confusion_matrix(y_test, predictions)

    return matrix


def cross_validate_model(X, y, cv=5):
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    scores = cross_val_score(
        model,
        X,
        y,
        cv=cv,
        scoring="accuracy"
    )

    return scores