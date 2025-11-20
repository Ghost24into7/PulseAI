"""
PulseAI - India Choropleth Map
State-wise geographic analysis with drill-down
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from pathlib import Path

# Page config
st.set_page_config(
    page_title="India Map - PulseAI",
    page_icon="🇮🇳",
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
    <h1>🇮🇳 India Geographic Analysis</h1>
    <p>State-wise financial metrics visualization</p>
</div>
""", unsafe_allow_html=True)

# Load data
from utils.data_downloader import load_all_data

data = load_all_data()

# India state codes (simplified mapping)
INDIA_STATE_CODES = {
    'Maharashtra': 'IN-MH', 'Karnataka': 'IN-KA', 'Tamil Nadu': 'IN-TN', 
    'Gujarat': 'IN-GJ', 'Delhi': 'IN-DL', 'Uttar Pradesh': 'IN-UP',
    'West Bengal': 'IN-WB', 'Telangana': 'IN-TG', 'Rajasthan': 'IN-RJ',
    'Madhya Pradesh': 'IN-MP', 'Kerala': 'IN-KL', 'Andhra Pradesh': 'IN-AP',
    'Punjab': 'IN-PB', 'Haryana': 'IN-HR', 'Bihar': 'IN-BR',
    'Odisha': 'IN-OR', 'Assam': 'IN-AS', 'Chhattisgarh': 'IN-CT',
    'Jharkhand': 'IN-JH', 'Uttarakhand': 'IN-UT', 'Himachal Pradesh': 'IN-HP',
    'Goa': 'IN-GA', 'Jammu & Kashmir': 'IN-JK', 'Puducherry': 'IN-PY',
    'Chandigarh': 'IN-CH'
}

# Controls
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    metric_choice = st.selectbox(
        "Select Metric to Visualize",
        ["Credit Growth %", "Deposit Growth %", "CD Ratio", "Digital Adoption %", "UPI Volume"],
        index=0
    )

with col2:
    color_scale = st.selectbox(
        "Color Scheme",
        ["Blues", "Viridis", "RdYlGn", "Plasma", "Turbo"],
        index=0
    )

with col3:
    show_labels = st.checkbox("Show Values", value=True)

# Map metric to column
metric_map = {
    "Credit Growth %": "Credit_Growth_%",
    "Deposit Growth %": "Deposit_Growth_%",
    "CD Ratio": "CD_Ratio",
    "Digital Adoption %": "Digital_Adoption_%",
    "UPI Volume": "UPI_Volume_Crore"
}

selected_column = metric_map[metric_choice]

# Prepare data
if not data['rbi_credit'].empty:
    map_data = data['rbi_credit'].copy()
    map_data['state_code'] = map_data['State'].map(INDIA_STATE_CODES)
    map_data = map_data.dropna(subset=['state_code'])
    
    # Create choropleth map
    st.markdown(f"<h2 class='section-title'>🗺️ {metric_choice} across Indian States</h2>", unsafe_allow_html=True)
    
    fig = go.Figure(go.Choropleth(
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=map_data['State'],
        z=map_data[selected_column],
        colorscale=color_scale,
        colorbar=dict(
            title=metric_choice,
            thickness=15,
            len=0.7,
            x=1.02
        ),
        text=map_data['State'],
        hovertemplate='<b>%{text}</b><br>' + 
                      f'{metric_choice}: %{{z:.2f}}<br>' +
                      '<extra></extra>',
        marker_line_color='white',
        marker_line_width=1.5
    ))
    
    fig.update_geos(
        visible=False,
        fitbounds="locations",
        projection_type="mercator"
    )
    
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='mercator'
        ),
        font=dict(family='Inter, sans-serif', size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics below map
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        max_state = map_data.loc[map_data[selected_column].idxmax()]
        st.metric("Highest", max_state['State'], f"{max_state[selected_column]:.2f}")
    
    with col2:
        min_state = map_data.loc[map_data[selected_column].idxmin()]
        st.metric("Lowest", min_state['State'], f"{min_state[selected_column]:.2f}")
    
    with col3:
        avg_val = map_data[selected_column].mean()
        st.metric("National Average", f"{avg_val:.2f}")
    
    with col4:
        std_val = map_data[selected_column].std()
        st.metric("Std Deviation", f"{std_val:.2f}")
    
    # Top performers
    st.markdown("---")
    st.markdown("<h2 class='section-title'>🏆 Top 10 Performers</h2>", unsafe_allow_html=True)
    
    top10 = map_data.nlargest(10, selected_column)
    
    fig_bar = go.Figure()
    
    fig_bar.add_trace(go.Bar(
        x=top10[selected_column],
        y=top10['State'],
        orientation='h',
        marker=dict(
            color=top10[selected_column],
            colorscale=color_scale,
            showscale=False
        ),
        text=top10[selected_column].apply(lambda x: f"{x:.2f}"),
        textposition='outside'
    ))
    
    fig_bar.update_layout(
        template='plotly_white',
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', size=12),
        xaxis_title=metric_choice,
        yaxis_title=""
    )
    
    fig_bar.update_xaxes(showgrid=True, gridcolor='rgba(200,200,200,0.2)')
    fig_bar.update_yaxes(showgrid=False)
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Comparison matrix
    st.markdown("---")
    st.markdown("<h2 class='section-title'>📊 Multi-Metric Comparison (Top 15 States)</h2>", unsafe_allow_html=True)
    
    # Heatmap of all metrics
    top15_states = map_data.nlargest(15, 'Credit_Growth_%')
    
    heatmap_data = top15_states[[
        'State', 'Credit_Growth_%', 'Deposit_Growth_%', 
        'CD_Ratio', 'Digital_Adoption_%'
    ]].set_index('State')
    
    fig_heat = go.Figure(go.Heatmap(
        z=heatmap_data.T.values,
        x=heatmap_data.index,
        y=['Credit Growth %', 'Deposit Growth %', 'CD Ratio', 'Digital Adoption %'],
        colorscale='Blues',
        text=heatmap_data.T.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
        colorbar=dict(thickness=15, len=0.7)
    ))
    
    fig_heat.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=100),
        font=dict(family='Inter, sans-serif', size=11),
        xaxis=dict(tickangle=-45)
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)
    
    # State selector for detailed view
    st.markdown("---")
    st.markdown("<h2 class='section-title'>🔍 State Deep Dive</h2>", unsafe_allow_html=True)
    
    selected_state = st.selectbox(
        "Select a state for detailed analysis",
        sorted(map_data['State'].unique())
    )
    
    if selected_state:
        state_data = map_data[map_data['State'] == selected_state].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {selected_state} - Banking Metrics")
            
            metrics_html = f"""
            <div class="state-detail-card">
                <div class="detail-row">
                    <span class="detail-label">Credit Outstanding:</span>
                    <span class="detail-value">₹{state_data['Credit_Crore']:,.0f} Cr</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Deposit Outstanding:</span>
                    <span class="detail-value">₹{state_data['Deposit_Crore']:,.0f} Cr</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Credit Growth:</span>
                    <span class="detail-value">{state_data['Credit_Growth_%']:.2f}%</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Deposit Growth:</span>
                    <span class="detail-value">{state_data['Deposit_Growth_%']:.2f}%</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">CD Ratio:</span>
                    <span class="detail-value">{state_data['CD_Ratio']:.2f}%</span>
                </div>
            </div>
            """
            st.markdown(metrics_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### {selected_state} - Digital Metrics")
            
            digital_html = f"""
            <div class="state-detail-card">
                <div class="detail-row">
                    <span class="detail-label">Digital Adoption:</span>
                    <span class="detail-value">{state_data['Digital_Adoption_%']:.2f}%</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">UPI Volume:</span>
                    <span class="detail-value">₹{state_data['UPI_Volume_Crore']:,.2f} Cr</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Data as of:</span>
                    <span class="detail-value">{state_data['As_Of_Date']}</span>
                </div>
            </div>
            """
            st.markdown(digital_html, unsafe_allow_html=True)
            
            # Radial gauge for digital adoption
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=state_data['Digital_Adoption_%'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Digital Adoption Score"},
                delta={'reference': map_data['Digital_Adoption_%'].mean()},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#4267B2"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 70], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': map_data['Digital_Adoption_%'].mean()
                    }
                }
            ))
            
            fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Comparison with national average
        st.markdown("### Comparison with National Average")
        
        comparison_metrics = ['Credit_Growth_%', 'Deposit_Growth_%', 'CD_Ratio', 'Digital_Adoption_%']
        comparison_df = pd.DataFrame({
            'Metric': ['Credit Growth', 'Deposit Growth', 'CD Ratio', 'Digital Adoption'],
            selected_state: [state_data[m] for m in comparison_metrics],
            'National Avg': [map_data[m].mean() for m in comparison_metrics]
        })
        
        fig_compare = go.Figure()
        
        fig_compare.add_trace(go.Bar(
            name=selected_state,
            x=comparison_df['Metric'],
            y=comparison_df[selected_state],
            marker_color='#4267B2'
        ))
        
        fig_compare.add_trace(go.Bar(
            name='National Average',
            x=comparison_df['Metric'],
            y=comparison_df['National Avg'],
            marker_color='#95a5a6'
        ))
        
        fig_compare.update_layout(
            barmode='group',
            template='plotly_white',
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)

else:
    st.error("Unable to load state-wise data")

# Data table
st.markdown("---")
with st.expander("📋 View Complete State-wise Data Table"):
    st.dataframe(
        data['rbi_credit'].sort_values('Credit_Growth_%', ascending=False),
        use_container_width=True,
        height=400
    )

st.caption("Data source: Reserve Bank of India (RBI) - Database on Indian Economy (DBIE)")
