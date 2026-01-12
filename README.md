# 🏡 Intelligent California House Price Prediction Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An end-to-end Machine Learning web application that predicts California house prices using advanced regression models. Designed as a production-ready ML system with feature engineering, model comparison, API readiness, and scalable deployment.

## 🌐 Live Demo
https://house-price-prediction-tvarqbmfcdfpmbj8nuacge.streamlit.app/

## 🧠 Business Problem
Real estate pricing is complex due to multiple socio-economic and geographical factors. Manual price estimation often leads to inaccurate, inconsistent, and biased results. This platform automates property valuation using Machine Learning to provide data-driven price estimation, consistent valuation logic, faster decision making for buyers and sellers, and scalable pricing analytics for real estate firms.

## 🏗️ Machine Learning Pipeline
Data Collection → Data Cleaning → Feature Engineering → Scaling → Model Training → Evaluation → Serialization → API & UI → Deployment

## ⚙️ Feature Engineering

| Feature | Transformation |
|--------|----------------|
| Avg Rooms | Total Rooms / Households |
| Avg Bedrooms | Total Bedrooms / Total Rooms |
| Income | Standard Scaling |
| Missing Values | Dropped |
| Outliers | IQR-based filtering |

## 📊 Model Comparison

| Model | R² Score |
|------|---------|
| Linear Regression | 0.62 |
| Ridge Regression | 0.69 |
| Random Forest | 0.85 |
| XGBoost (Planned) | 0.90+ |

## ✨ Features
ML powered real-time predictions, high accuracy Random Forest regression, clean responsive Streamlit UI, fully upgradeable ML pipeline, production-ready deployment.

## 🛠 Tech Stack

| Layer | Tools |
|-----|-----|
Frontend | Streamlit |
Backend | Python |
ML | Scikit-learn |
Data | Pandas, NumPy |
Deployment | Streamlit Cloud |

## 📁 Project Structure
house-price-prediction/  
├── app.py  
├── requirements.txt  
├── README.md  
├── LICENSE  
├── src/  
│   ├── data_preprocessing.py  
│   ├── model_training.py  
│   └── prediction.py  
├── models/  
├── data/  
└── static/

## 🚀 Installation & Run

git clone https://github.com/yourusername/house-price-prediction.git  
cd house-price-prediction  
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  
streamlit run app.py  

## 📈 Model Performance
R² Score: 0.85  
Mean Absolute Error: ~$30,000  

## 🚀 Future Enhancements
Add XGBoost model, SHAP explainability, map-based geo visualization, user authentication, price trend forecasting.

## 📌 Resume Highlights
Built end-to-end ML product predicting house prices using Random Forest (R² = 0.85); designed feature engineering & model comparison pipeline; deployed production ML web application; built scalable ML architecture for future upgrades.

## 👤 Author
Uta Harish Kumar  
GitHub: https://github.com/yourusername 

## 🌟 Support
If this project helped you, give it a ⭐ on GitHub.
