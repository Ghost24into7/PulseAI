"""
PulseAI - Real-Time Indian Financial Intelligence Engine
Main Landing Page
"""

import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="PulseAI - Indian Financial Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Ghost24into7/PulseAI',
        'Report a bug': "https://github.com/Ghost24into7/PulseAI/issues",
        'About': "PulseAI - Real-Time Indian Financial Intelligence Engine"
    }
)

# Load custom CSS
css_file = Path(__file__).parent / "assets" / "custom.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">
            <span class="pulse-icon">📊</span> PulseAI
        </h1>
        <p class="hero-subtitle">Real-Time Indian Financial Intelligence Engine</p>
        <p class="hero-description">
            Powered by Google Gemini 1.5 Flash | Analyzing RBI, NPCI, NSE & AMFI Data
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Key Features Grid
st.markdown("---")
st.markdown("<h2 class='section-title'>🚀 Enterprise-Grade Features</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏠</div>
        <h3>Interactive Dashboard</h3>
        <p>Real-time visualizations of UPI, banking credit, stock markets, and mutual funds with state-wise breakdowns</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🇮🇳</div>
        <h3>India Choropleth Map</h3>
        <p>Geographic insights with drill-down capabilities for credit growth, deposits, and digital adoption</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>AI-Powered RAG Chat</h3>
        <p>Ask questions about RBI policies, UPI trends, market movements in English or Hindi</p>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Auto-Generated Reports</h3>
        <p>One-click boardroom presentations with RBI-style branding and executive summaries</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔮</div>
        <h3>Prophet Forecasting</h3>
        <p>30-day predictions for UPI volumes and credit growth with AI-written narratives</p>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Zero-GPU Architecture</h3>
        <p>CPU-only processing with intelligent caching and free-tier Gemini API integration</p>
    </div>
    """, unsafe_allow_html=True)

# Data Sources
st.markdown("---")
st.markdown("<h2 class='section-title'>📡 Trusted Data Sources</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="data-source-card">
        <h4>🏦 Reserve Bank of India</h4>
        <p>Banking credit, deposits, monetary policy, payment systems</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="data-source-card">
        <h4>💳 NPCI</h4>
        <p>UPI transaction volumes, values, and adoption metrics</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="data-source-card">
        <h4>📈 NSE India</h4>
        <p>Stock market indices, top performers, daily movements</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="data-source-card">
        <h4>💰 AMFI</h4>
        <p>Mutual fund AUM, investor accounts, category trends</p>
    </div>
    """, unsafe_allow_html=True)

# Quick Stats
st.markdown("---")
st.markdown("<h2 class='section-title'>📊 Quick Statistics</h2>", unsafe_allow_html=True)

# Load data for stats
try:
    from utils.data_downloader import load_all_data
    data = load_all_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not data['upi'].empty:
            latest_upi = data['upi'].iloc[-1]
            st.metric(
                "UPI Transactions (Latest Month)",
                f"{latest_upi['Volume_Billion']:.1f}B",
                f"{latest_upi['Month']}"
            )
    
    with col2:
        if not data['upi'].empty:
            st.metric(
                "UPI Value",
                f"₹{latest_upi['Value_LakhCrore']:.2f}L Cr",
                "YoY Growth: ~45%"
            )
    
    with col3:
        if not data['rbi_credit'].empty:
            avg_growth = data['rbi_credit']['Credit_Growth_%'].mean()
            st.metric(
                "Avg Credit Growth",
                f"{avg_growth:.2f}%",
                "Across all states"
            )
    
    with col4:
        if not data['nse'].empty:
            avg_change = data['nse']['Change_%'].mean()
            st.metric(
                "Market Sentiment",
                f"{avg_change:+.2f}%",
                "NSE Top 10 Avg"
            )

except Exception as e:
    st.info("💡 Click on a page in the sidebar to start exploring!")

# Navigation Guide
st.markdown("---")
st.markdown("<h2 class='section-title'>🧭 Navigation Guide</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h3>👈 Use the sidebar to navigate between pages:</h3>
    <ul>
        <li><strong>🏠 Dashboard</strong> - Overview of all key metrics with interactive charts</li>
        <li><strong>🇮🇳 India Map</strong> - Geographic analysis with state-wise drill-down</li>
        <li><strong>💬 Ask RBI Chat</strong> - AI-powered question answering with RAG</li>
        <li><strong>📊 Automated Report</strong> - Generate boardroom presentations in seconds</li>
        <li><strong>🔮 Forecasting</strong> - 30-day predictions with Prophet models</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Tech Stack
st.markdown("---")
st.markdown("<h2 class='section-title'>⚙️ Technology Stack</h2>", unsafe_allow_html=True)

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
    **Frontend & Visualization**
    - Streamlit (Latest)
    - Plotly (Interactive Charts)
    - Custom CSS (Glassmorphism)
    """)

with tech_col2:
    st.markdown("""
    **AI & ML**
    - Google Gemini 1.5 Flash
    - Prophet (Forecasting)
    - RAG (1M Context)
    """)

with tech_col3:
    st.markdown("""
    **Data & Automation**
    - Pandas (Analysis)
    - Python-PPTX (Reports)
    - Smart Caching (24h)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>
        <strong>PulseAI</strong> - Real-Time Indian Financial Intelligence Engine<br>
        Data sourced from RBI, NPCI, NSE, AMFI | For educational and analytical purposes<br>
        November 2025 | Built with ❤️ for India's fintech ecosystem
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    st.markdown("""
    - 📊 View live dashboard
    - 🗺️ Explore state data
    - 💬 Ask AI questions
    - 📄 Generate reports
    - 🔮 See forecasts
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **PulseAI** is a zero-GPU, CPU-only financial intelligence platform 
    designed for Indian markets. It leverages Google Gemini's 1M context 
    window for RAG-based insights without any vector database.
    """)
    
    st.markdown("---")
    st.markdown("### 🔑 Setup")
    st.info("Add your `GEMINI_API_KEY` in `.streamlit/secrets.toml` to enable AI features")
    
    st.markdown("---")
    st.markdown("### 🌟 GitHub")
    st.markdown("[⭐ Star on GitHub](https://github.com/Ghost24into7/PulseAI)")
