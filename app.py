import sys, os
import streamlit as st
import pandas as pd

# Allow importing from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from prediction import HousePricePredictor # type: ignore

# Page Configuration
st.set_page_config(
    page_title="House Price Prediction System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Sora:wght@600;700;800&display=swap');

    :root {
        --navy: #0f172a;
        --indigo: #1d4ed8;
        --teal: #0891b2;
        --amber: #f59e0b;
        --text: #0b1220;
        --muted: #546177;
        --panel: rgba(255, 255, 255, 0.84);
        --panel-border: rgba(15, 23, 42, 0.08);
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 10%, rgba(8, 145, 178, 0.30), transparent 34%),
            radial-gradient(circle at 88% 15%, rgba(245, 158, 11, 0.28), transparent 34%),
            linear-gradient(140deg, #f5fbff 0%, #eef6fb 50%, #fef6ec 100%);
        color: var(--text);
        font-family: "Manrope", "Segoe UI", sans-serif;
    }

    .main-header {
        background: linear-gradient(125deg, #0f172a 0%, #1e3a8a 45%, #0369a1 100%);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin-bottom: 1.5rem;
        color: #f8fafc;
        text-align: center;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
        overflow: hidden;
        position: relative;
    }

    .main-header::before,
    .main-header::after {
        content: "";
        position: absolute;
        border-radius: 999px;
        filter: blur(8px);
        z-index: 0;
    }

    .main-header::before {
        width: 260px;
        height: 260px;
        background: rgba(14, 165, 233, 0.28);
        top: -80px;
        right: -40px;
    }

    .main-header::after {
        width: 180px;
        height: 180px;
        background: rgba(245, 158, 11, 0.22);
        bottom: -60px;
        left: -30px;
    }

    .main-header h1,
    .main-header p,
    .model-badge {
        position: relative;
        z-index: 1;
    }

    .main-header h1 {
        font-family: "Sora", "Segoe UI", sans-serif;
        font-size: 2.9rem;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        font-size: 1.15rem;
        color: #dbeafe;
    }

    .model-badge {
        display: inline-block;
        margin-top: 1rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.16);
        border: 1px solid rgba(255, 255, 255, 0.35);
        padding: 0.55rem 1.15rem;
        font-size: 0.95rem;
        backdrop-filter: blur(6px);
    }

    .info-card {
        background: var(--panel);
        border: 1px solid var(--panel-border);
        border-radius: 18px;
        padding: 1.5rem 1.7rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(4px);
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.07);
    }

    .info-card h3 {
        color: var(--navy);
        font-family: "Sora", "Segoe UI", sans-serif;
        font-size: 1.22rem;
        margin-bottom: 0.8rem;
    }

    .info-card ul {
        margin: 0;
        padding-left: 1.15rem;
        color: var(--muted);
        line-height: 1.7;
        font-size: 0.98rem;
    }

    .section-header {
        font-family: "Sora", "Segoe UI", sans-serif;
        color: var(--navy);
        font-size: 1.65rem;
        font-weight: 800;
        margin: 1.4rem 0 1.1rem;
        letter-spacing: -0.02em;
    }

    .input-label {
        color: var(--text);
        font-size: 1rem;
        font-weight: 700;
        margin: 0.45rem 0 0.35rem;
    }

    .stNumberInput {
        background: rgba(255, 255, 255, 0.94);
        border-radius: 14px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        padding: 0.3rem 0.55rem;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
        margin-bottom: 0.8rem;
    }

    .stNumberInput:focus-within {
        border-color: rgba(37, 99, 235, 0.45);
        box-shadow: 0 8px 20px rgba(29, 78, 216, 0.14);
        transform: translateY(-1px);
    }

    .stNumberInput > div > div > input {
        border: none !important;
        background: transparent !important;
        color: var(--text) !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    .stButton > button {
        width: 100%;
        margin-top: 1.2rem !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.95rem 1.25rem !important;
        font-family: "Sora", "Segoe UI", sans-serif !important;
        font-size: 1.06rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
        color: #f8fafc !important;
        background: linear-gradient(120deg, #1d4ed8 0%, #0369a1 60%, #0f766e 100%) !important;
        box-shadow: 0 12px 25px rgba(29, 78, 216, 0.28) !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        filter: saturate(1.08);
        box-shadow: 0 16px 34px rgba(8, 145, 178, 0.32) !important;
    }

    .result-box {
        margin: 1.6rem 0 0.6rem;
        border-radius: 18px;
        padding: 2.1rem 1.2rem;
        text-align: center;
        color: #f8fafc;
        background: linear-gradient(120deg, #0f172a 0%, #155e75 55%, #f59e0b 145%);
        box-shadow: 0 18px 44px rgba(15, 23, 42, 0.27);
        animation: revealUp 420ms ease;
    }

    .result-box h2 {
        margin: 0;
        font-size: 1.3rem;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        opacity: 0.95;
    }

    .result-box .price {
        margin-top: 0.5rem;
        font-family: "Sora", "Segoe UI", sans-serif;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .footer {
        margin-top: 2.4rem;
        text-align: center;
        color: #5b6679;
        font-size: 0.95rem;
        padding: 1.1rem 0.5rem;
        border-top: 1px dashed rgba(15, 23, 42, 0.18);
    }

    @keyframes revealUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .block-container {
        max-width: 1180px !important;
        padding: 1.2rem 1.1rem 2.2rem !important;
    }

    [data-testid="column"] {
        padding: 0 0.6rem;
    }

    .stSpinner > div {
        border-top-color: var(--amber) !important;
    }

    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1.2rem;
            border-radius: 18px;
        }

        .main-header h1 {
            font-size: 2rem;
        }

        .section-header {
            font-size: 1.3rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load Predictor
@st.cache_resource
def load_predictor():
    return HousePricePredictor()

predictor = load_predictor()
model_name = predictor.model_name

# Header
st.markdown(f"""
<div class="main-header">
    <h1>House Price Intelligence Suite</h1>
    <p>AI-driven California property valuation for faster pricing decisions</p>
    <div class="model-badge">
        Current Model: <strong>{model_name}</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# Info Card
st.markdown("""
<div class="info-card">
    <h3>Input Guidelines</h3>
    <ul>
        <li><strong>Median Income:</strong> Enter in tens of thousands, for example 3.5 means $35,000.</li>
        <li><strong>House Age:</strong> Enter total age of nearby homes in years.</li>
        <li><strong>Average Rooms and Bedrooms:</strong> Keep values realistic for your target locality.</li>
        <li><strong>Population and Occupancy:</strong> Use neighborhood-level averages when possible.</li>
        <li><strong>Latitude and Longitude:</strong> Accurate coordinates improve geographic pricing quality.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Section Header
st.markdown('<div class="section-header">Property Feature Inputs</div>', unsafe_allow_html=True)

# Input Form with better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-label">Income Signal  Median Income (in $10k)</div>', unsafe_allow_html=True)
    MedInc = st.number_input("Median Income", value=3.5, step=0.1, format="%.2f", key="medinc", label_visibility="collapsed")
    
    st.markdown('<div class="input-label">Structure Age  House Age (years)</div>', unsafe_allow_html=True)
    HouseAge = st.number_input("House Age", value=30.0, step=1.0, format="%.1f", key="houseage", label_visibility="collapsed")
    
    st.markdown('<div class="input-label">Space Mix  Average Rooms</div>', unsafe_allow_html=True)
    AveRooms = st.number_input("Average Rooms", value=5.0, step=0.1, format="%.1f", key="averrooms", label_visibility="collapsed")
    
    st.markdown('<div class="input-label">Room Ratio  Average Bedrooms</div>', unsafe_allow_html=True)
    AveBedrms = st.number_input("Average Bedrooms", value=1.0, step=0.1, format="%.1f", key="avebedrms", label_visibility="collapsed")

with col2:
    st.markdown('<div class="input-label">Demand Density  Population</div>', unsafe_allow_html=True)
    Population = st.number_input("Population", value=1000.0, step=10.0, format="%.0f", key="population", label_visibility="collapsed")
    
    st.markdown('<div class="input-label">Household Size  Average Occupancy</div>', unsafe_allow_html=True)
    AveOccup = st.number_input("Average Occupancy", value=3.0, step=0.1, format="%.1f", key="aveoccup", label_visibility="collapsed")
    
    st.markdown('<div class="input-label">Geo Northing  Latitude</div>', unsafe_allow_html=True)
    Latitude = st.number_input("Latitude", value=34.05, step=0.01, format="%.2f", key="latitude", label_visibility="collapsed")
    
    st.markdown('<div class="input-label">Geo Easting  Longitude</div>', unsafe_allow_html=True)
    Longitude = st.number_input("Longitude", value=-118.25, step=0.01, format="%.2f", key="longitude", label_visibility="collapsed")

# Predict Button
if st.button("Estimate Market Price"):
    # Create input dataframe
    input_data = pd.DataFrame({
        'MedInc': [MedInc],
        'HouseAge': [HouseAge],
        'AveRooms': [AveRooms],
        'AveBedrms': [AveBedrms],
        'Population': [Population],
        'AveOccup': [AveOccup],
        'Latitude': [Latitude],
        'Longitude': [Longitude]
    })
    
    try:
        # Make prediction
        with st.spinner('🤖 Analyzing property data...'):
            prediction = predictor.predict(input_data)
            price = prediction * 100000
        
        # Display result with animation
        st.markdown(f"""
        <div class="result-box">
            <h2>Estimated Market Price</h2>
            <div class="price">${price:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional info
        st.balloons()
        
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# Footer
st.markdown("""
<div class="footer">
    <p>Designed for modern valuation workflows with Streamlit and machine learning.</p>
    <p>© 2026 House Price Intelligence Suite</p>
</div>
""", unsafe_allow_html=True)