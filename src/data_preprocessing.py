import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle


def preprocess_data():
    print("=" * 70)
    print("DATA PREPROCESSING")
    print("=" * 70)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = pd.read_csv(os.path.join(DATA_DIR, "housing.csv"))

    # Auto detect target column
    possible_targets = ["median_house_value", "Price", "price", "target"]

    TARGET = None
    for col in possible_targets:
        if col in df.columns:
            TARGET = col
            break

    if TARGET is None:
        raise Exception(f"No target column found. Available columns: {df.columns.tolist()}")

    print(f"🎯 Using target column: {TARGET}")

    y = df[TARGET]
    X = df.drop(TARGET, axis=1)

    # Feature engineering
    X["RoomsPerHousehold"] = X["AveRooms"] / X["AveBedrms"]
    X["PopulationPerHousehold"] = X["Population"] / X["AveOccup"]
    X["BedroomRatio"] = X["AveBedrms"] / X["AveRooms"]

    X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Save artifacts
    np.save(os.path.join(DATA_DIR, "X_train.npy"), X_train)
    np.save(os.path.join(DATA_DIR, "X_test.npy"), X_test)
    np.save(os.path.join(DATA_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(DATA_DIR, "y_test.npy"), y_test)

    with open(os.path.join(MODEL_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    with open(os.path.join(DATA_DIR, "feature_names.pkl"), "wb") as f:
        pickle.dump(X.columns.tolist(), f)

    print("✅ Preprocessing complete")


if __name__ == "__main__":
    preprocess_data()
