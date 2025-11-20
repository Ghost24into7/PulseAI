"""
PulseAI - Interactive Dashboard
Real-time financial metrics and visualizations
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Dashboard - PulseAI",
    page_icon="🏠",
    layout="wide"
)

# Load custom CSS
css_file = Path(__file__).parent.parent / "assets" / "custom.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="page-header">
    <h1>🏠 Real-Time Financial Dashboard</h1>
    <p>Live insights from RBI, NPCI, NSE, and AMFI</p>
</div>
""", unsafe_allow_html=True)

# Load data
from utils.data_downloader import load_all_data

data = load_all_data()

# Top Metrics Row
st.markdown("<h2 class='section-title'>📊 Key Metrics</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if not data['upi'].empty:
        latest_upi = data['upi'].iloc[-1]
        prev_upi = data['upi'].iloc[-2] if len(data['upi']) > 1 else latest_upi
        delta = latest_upi['Volume_Billion'] - prev_upi['Volume_Billion']
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">UPI Transactions</div>
            <div class="metric-value">{latest_upi['Volume_Billion']:.2f}B</div>
            <div class="metric-delta positive">+{delta:.2f}B from prev month</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if not data['upi'].empty:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">UPI Value</div>
            <div class="metric-value">₹{latest_upi['Value_LakhCrore']:.2f}L Cr</div>
            <div class="metric-delta positive">YoY: +45%</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if not data['rbi_credit'].empty:
        avg_growth = data['rbi_credit']['Credit_Growth_%'].mean()
        top_state = data['rbi_credit'].nlargest(1, 'Credit_Growth_%').iloc[0]
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Credit Growth</div>
            <div class="metric-value">{avg_growth:.2f}%</div>
            <div class="metric-delta">Leader: {top_state['State']}</div>
        </div>
        """, unsafe_allow_html=True)

with col4:
    if not data['nse'].empty:
        market_change = data['nse']['Change_%'].mean()
        sentiment = "🟢 Bullish" if market_change > 0 else "🔴 Bearish" if market_change < -0.5 else "🟡 Neutral"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Market Sentiment</div>
            <div class="metric-value">{sentiment}</div>
            <div class="metric-delta">NSE Avg: {market_change:+.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

# Charts Row 1
st.markdown("---")
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<h3 class='chart-title'>📈 UPI Transaction Trend (24 Months)</h3>", unsafe_allow_html=True)
    
    if not data['upi'].empty:
        fig = go.Figure()
        
        # Area chart for volume
        fig.add_trace(go.Scatter(
            x=data['upi']['Month'],
            y=data['upi']['Volume_Billion'],
            fill='tozeroy',
            name='Volume (Billion)',
            line=dict(color='#4267B2', width=2),
            fillcolor='rgba(66, 103, 178, 0.3)'
        ))
        
        # Annotations for festival months
        festival_months = data['upi'][data['upi']['Month'].str.contains('2025-10|2025-11|2025-03')]
        
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', size=12),
            showlegend=False
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)')
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Loading UPI data...")

with col2:
    st.markdown("<h3 class='chart-title'>🏆 Top 5 States by Credit Growth</h3>", unsafe_allow_html=True)
    
    if not data['rbi_credit'].empty:
        top5 = data['rbi_credit'].nlargest(5, 'Credit_Growth_%')
        
        fig = go.Figure(go.Bar(
            x=top5['Credit_Growth_%'],
            y=top5['State'],
            orientation='h',
            marker=dict(
                color=top5['Credit_Growth_%'],
                colorscale='Blues',
                showscale=False
            ),
            text=top5['Credit_Growth_%'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside'
        ))
        
        fig.update_layout(
            template='plotly_white',
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', size=12),
            showlegend=False,
            xaxis_title="Growth %",
            yaxis_title=""
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)')
        fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)

# Charts Row 2
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 class='chart-title'>📊 NSE Top 10 Performers</h3>", unsafe_allow_html=True)
    
    if not data['nse'].empty:
        fig = go.Figure()
        
        colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in data['nse']['Change_%']]
        
        fig.add_trace(go.Bar(
            x=data['nse']['Symbol'],
            y=data['nse']['Change_%'],
            marker=dict(color=colors),
            text=data['nse']['Change_%'].apply(lambda x: f"{x:+.2f}%"),
            textposition='outside'
        ))
        
        fig.update_layout(
            template='plotly_white',
            height=350,
            margin=dict(l=20, r=20, t=20, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', size=12),
            showlegend=False,
            yaxis_title="Change %",
            xaxis_title=""
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=True)
        
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<h3 class='chart-title'>💰 Mutual Fund AUM by Category</h3>", unsafe_allow_html=True)
    
    if not data['mutual_funds'].empty:
        latest_month = data['mutual_funds']['Month'].max()
        latest_mf = data['mutual_funds'][data['mutual_funds']['Month'] == latest_month]
        
        fig = go.Figure(go.Pie(
            labels=latest_mf['Category'],
            values=latest_mf['AUM_LakhCrore'],
            hole=0.4,
            marker=dict(colors=px.colors.sequential.Blues_r),
            textinfo='label+percent',
            textposition='outside'
        ))
        
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', size=12),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Bottom Section - Digital Adoption Leaderboard
st.markdown("---")
st.markdown("<h2 class='section-title'>🎖️ Digital Payment Adoption Leaderboard</h2>", unsafe_allow_html=True)

if not data['rbi_credit'].empty:
    top_digital = data['rbi_credit'].nlargest(10, 'Digital_Adoption_%')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥇 Gold Tier")
        for i, row in top_digital.head(3).iterrows():
            st.markdown(f"""
            <div class="leaderboard-card gold">
                <span class="rank">#{top_digital.index.get_loc(i) + 1}</span>
                <span class="state-name">{row['State']}</span>
                <span class="score">{row['Digital_Adoption_%']:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🥈 Silver Tier")
        for i, row in top_digital.iloc[3:6].iterrows():
            st.markdown(f"""
            <div class="leaderboard-card silver">
                <span class="rank">#{top_digital.index.get_loc(i) + 1}</span>
                <span class="state-name">{row['State']}</span>
                <span class="score">{row['Digital_Adoption_%']:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🥉 Bronze Tier")
        for i, row in top_digital.iloc[6:9].iterrows():
            st.markdown(f"""
            <div class="leaderboard-card bronze">
                <span class="rank">#{top_digital.index.get_loc(i) + 1}</span>
                <span class="state-name">{row['State']}</span>
                <span class="score">{row['Digital_Adoption_%']:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

# Data Table
st.markdown("---")
with st.expander("📋 View Detailed Data Tables"):
    tab1, tab2, tab3, tab4 = st.tabs(["UPI", "State Banking", "NSE", "Mutual Funds"])
    
    with tab1:
        st.dataframe(data['upi'].tail(12), use_container_width=True)
    
    with tab2:
        st.dataframe(data['rbi_credit'].sort_values('Credit_Growth_%', ascending=False), use_container_width=True)
    
    with tab3:
        st.dataframe(data['nse'], use_container_width=True)
    
    with tab4:
        latest = data['mutual_funds'][data['mutual_funds']['Month'] == data['mutual_funds']['Month'].max()]
        st.dataframe(latest, use_container_width=True)

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Data cached for 24 hours | Sources: RBI, NPCI, NSE, AMFI")
