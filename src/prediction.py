import os
import pickle
import numpy as np
import pandas as pd

class HousePricePredictor:
    def __init__(self):
        ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MODEL_DIR = os.path.join(ROOT, "models")

        MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
        SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
        NAME_PATH = os.path.join(MODEL_DIR, "model_name.txt")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Missing model: {MODEL_PATH}")
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Missing scaler: {SCALER_PATH}")
        if not os.path.exists(NAME_PATH):
            raise FileNotFoundError(f"Missing model name: {NAME_PATH}")

        with open(MODEL_PATH, "rb") as f:
            self.model = pickle.load(f)

        with open(SCALER_PATH, "rb") as f:
            self.scaler = pickle.load(f)

        with open(NAME_PATH, "r") as f:
            self.model_name = f.read().strip()

    def predict(self, df: pd.DataFrame):
        df = df.copy()

        # Feature Engineering (must match training)
        df["RoomsPerHousehold"] = df["AveRooms"] / df["AveBedrms"]
        df["PopulationPerHousehold"] = df["Population"] / df["AveOccup"]
        df["BedroomRatio"] = df["AveBedrms"] / df["AveRooms"]

        df = df.replace([np.inf, -np.inf], 0).fillna(0)

        df_scaled = self.scaler.transform(df)

        return float(self.model.predict(df_scaled)[0])
