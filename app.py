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
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container */
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem auto;
        max-width: 1400px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
        animation: pulse 3s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    .model-badge {
        background: rgba(255,255,255,0.25);
        padding: 0.7rem 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        display: inline-block;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.4);
        font-size: 1.05rem;
        position: relative;
        z-index: 1;
    }
    
    /* Info box with card design */
    .info-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .info-card h3 {
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .info-card ul {
        margin-left: 1.5rem;
        color: #555;
        line-height: 1.8;
    }
    
    .info-card li {
        margin: 8px 0;
        font-size: 1.05rem;
    }
    
    .info-card li strong {
        color: #333;
    }
    
    /* Section headers */
    .section-header {
        color: #333;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Input field container */
    .input-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 2px solid #e9ecef;
        transition: all 0.3s;
    }
    
    .input-container:hover {
        border-color: #667eea;
        background: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    /* Input labels */
    .input-label {
        color: #333;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .input-label .emoji {
        font-size: 1.8rem;
    }
    
    /* Streamlit input styling */
    .stNumberInput > div > div > input {
        background: white !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        background: white !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px);
    }
    
    .stNumberInput > div > div > input:hover {
        border-color: #667eea !important;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 1.2rem 3rem !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        transition: all 0.3s !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        margin-top: 2rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 3rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 2.5rem 0;
        box-shadow: 0 15px 40px rgba(17, 153, 142, 0.4);
        animation: slideIn 0.6s ease;
        position: relative;
        overflow: hidden;
    }
    
    .result-box::before {
        content: '✨';
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 3rem;
        animation: sparkle 2s infinite;
    }
    
    @keyframes sparkle {
        0%, 100% {
            transform: scale(1) rotate(0deg);
            opacity: 0.6;
        }
        50% {
            transform: scale(1.3) rotate(180deg);
            opacity: 1;
        }
    }
    
    .result-box h2 {
        font-size: 1.8rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .result-box .price {
        font-size: 4rem;
        font-weight: 900;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
        animation: countUp 0.8s ease;
        letter-spacing: 2px;
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.3);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: #666;
        margin-top: 3rem;
        border-top: 3px solid #667eea;
        font-size: 1.05rem;
    }
    
    .footer p {
        margin: 8px 0;
    }
    
    .footer .heart {
        color: #ff6b6b;
        animation: heartbeat 1.5s infinite;
        font-size: 1.2rem;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        10%, 30% { transform: scale(1.15); }
        20%, 40% { transform: scale(1); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Container styling */
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
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
    <h1>🏠 House Price Prediction System</h1>
    <p>ML-Powered Real Estate Valuation</p>
    <div class="model-badge">
        <strong>Current Model:</strong> {model_name}
    </div>
</div>
""", unsafe_allow_html=True)

# Info Card
st.markdown("""
<div class="info-card">
    <h3>📊 Input Guidelines</h3>
    <ul>
        <li><strong>Median Income:</strong> In tens of thousands (e.g., 3.5 = $35,000)</li>
        <li><strong>House Age:</strong> Age of the house in years</li>
        <li><strong>Avg Rooms:</strong> Average number of rooms per household</li>
        <li><strong>Avg Bedrooms:</strong> Average number of bedrooms per household</li>
        <li><strong>Population:</strong> Block population</li>
        <li><strong>Avg Occupancy:</strong> Average household members</li>
        <li><strong>Latitude/Longitude:</strong> Geographic coordinates</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Section Header
st.markdown('<div class="section-header">🏘️ Enter Property Details</div>', unsafe_allow_html=True)

# Input Form with better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="input-label"><span class="emoji">💰</span> Median Income (in $10k)</div>', unsafe_allow_html=True)
    MedInc = st.number_input("", value=3.5, step=0.1, format="%.2f", key="medinc", label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="emoji">🏗️</span> House Age (years)</div>', unsafe_allow_html=True)
    HouseAge = st.number_input("", value=30.0, step=1.0, format="%.1f", key="houseage", label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="emoji">🚪</span> Average Rooms</div>', unsafe_allow_html=True)
    AveRooms = st.number_input("", value=5.0, step=0.1, format="%.1f", key="averrooms", label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="emoji">🛏️</span> Average Bedrooms</div>', unsafe_allow_html=True)
    AveBedrms = st.number_input("", value=1.0, step=0.1, format="%.1f", key="avebedrms", label_visibility="collapsed")

with col2:
    st.markdown('<div class="input-label"><span class="emoji">👥</span> Population</div>', unsafe_allow_html=True)
    Population = st.number_input("", value=1000.0, step=10.0, format="%.0f", key="population", label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="emoji">🏘️</span> Average Occupancy</div>', unsafe_allow_html=True)
    AveOccup = st.number_input("", value=3.0, step=0.1, format="%.1f", key="aveoccup", label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="emoji">🌍</span> Latitude</div>', unsafe_allow_html=True)
    Latitude = st.number_input("", value=34.05, step=0.01, format="%.2f", key="latitude", label_visibility="collapsed")
    
    st.markdown('<div class="input-label"><span class="emoji">🧭</span> Longitude</div>', unsafe_allow_html=True)
    Longitude = st.number_input("", value=-118.25, step=0.01, format="%.2f", key="longitude", label_visibility="collapsed")

# Predict Button
if st.button("🔮 Predict House Price"):
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
            <h2>✨ Predicted House Price</h2>
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
    <p>Built with <span class="heart">❤️</span> using Streamlit & Machine Learning</p>
    <p>© 2026 House Price Prediction System</p>
</div>
""", unsafe_allow_html=True)