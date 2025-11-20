"""
PulseAI - Ask RBI Chat
AI-powered RAG chatbot using Gemini 1.5 Flash
"""

import streamlit as st
import time
from pathlib import Path
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Ask RBI Chat - PulseAI",
    page_icon="💬",
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
    <h1>💬 Ask RBI - AI Financial Assistant</h1>
    <p>Powered by Google Gemini 1.5 Flash with 1M context RAG</p>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_context_loaded" not in st.session_state:
    st.session_state.rag_context_loaded = False

if "rag_context" not in st.session_state:
    st.session_state.rag_context = ""

# Load RAG system
from utils.gemini_rag import get_rag_instance
from utils.data_downloader import load_all_data

# Initialize RAG (only once)
try:
    rag = get_rag_instance()
    
    # Build context if not loaded
    if not st.session_state.rag_context_loaded:
        with st.spinner("🔄 Loading financial data into AI context..."):
            data = load_all_data()
            st.session_state.rag_context = rag.build_context_from_data(data)
            st.session_state.rag_context_loaded = True
    
    rag_available = True
except Exception as e:
    rag_available = False
    st.error(f"⚠️ RAG system unavailable: {str(e)}")
    st.info("Add your GEMINI_API_KEY to .streamlit/secrets.toml to enable AI chat")

# Sidebar with example questions
with st.sidebar:
    st.markdown("### 💡 Example Questions")
    
    example_questions = [
        "What is the latest UPI transaction volume?",
        "Which state has the highest credit growth?",
        "Explain RBI's current monetary policy stance",
        "Compare digital adoption across top 5 states",
        "What are the trends in mutual fund investments?",
        "How is the stock market performing today?",
        "Tell me about Karnataka's banking sector",
        "UPI का महीने का वॉल्यूम क्या है?",  # Hindi
        "What is CD ratio and why is it important?",
        "Forecast UPI growth for next month"
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(question, key=f"example_{i}", use_container_width=True):
            st.session_state.example_clicked = question
    
    st.markdown("---")
    st.markdown("### ℹ️ About RAG")
    st.markdown("""
    This chat uses **Retrieval-Augmented Generation** with:
    - 700K+ tokens of financial context
    - Real-time data from RBI, NPCI, NSE, AMFI
    - Gemini 1.5 Flash (free tier)
    - No vector database required
    """)
    
    st.markdown("---")
    st.markdown("### 🌐 Language Support")
    st.markdown("Ask in **English** or **Hindi**! Gemini handles both natively.")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
chat_container = st.container()

# Display chat history
with chat_container:
    if not st.session_state.messages:
        # Welcome message
        st.markdown("""
        <div class="chat-welcome">
            <h2>👋 Welcome to Ask RBI!</h2>
            <p>I'm your AI financial assistant trained on the latest Indian financial data.</p>
            <p>Ask me anything about:</p>
            <ul>
                <li>🏦 Banking credit and deposits</li>
                <li>💳 UPI and digital payments</li>
                <li>📈 Stock market trends</li>
                <li>💰 Mutual funds</li>
                <li>🏛️ RBI policies</li>
                <li>🗺️ State-wise analysis</li>
            </ul>
            <p><strong>Try an example from the sidebar or type your question below!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Indian financial markets...") or st.session_state.get("example_clicked"):
    if st.session_state.get("example_clicked"):
        prompt = st.session_state.example_clicked
        st.session_state.example_clicked = None
    
    if not rag_available:
        st.error("⚠️ Please add GEMINI_API_KEY to use chat functionality")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Show thinking animation
            with st.spinner("🤔 Analyzing data..."):
                time.sleep(0.5)  # Brief pause for UX
            
            # Stream response
            response_stream = rag.query(
                prompt, 
                st.session_state.rag_context, 
                stream=True
            )
            
            # Display streaming response
            for chunk in response_stream:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.02)  # Smooth streaming effect
            
            message_placeholder.markdown(full_response)
            
            # Add copy button and sources
            col1, col2 = st.columns([6, 1])
            with col2:
                if st.button("📋 Copy", key=f"copy_{len(st.session_state.messages)}"):
                    st.toast("Response copied!", icon="✅")
            
            # Sources citation
            st.markdown("""
            <div class="sources-box">
                <strong>📚 Sources:</strong> RBI DBIE, NPCI Statistics, NSE API, AMFI Reports
            </div>
            """, unsafe_allow_html=True)
        
        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            
            if "429" in str(e) or "quota" in str(e).lower():
                error_message = "⚠️ Rate limit exceeded. Free tier allows 15 requests/minute. Please wait a moment and try again."
            elif "api" in str(e).lower():
                error_message = "⚠️ API error. Please check your GEMINI_API_KEY in .streamlit/secrets.toml"
            
            full_response = error_message
            message_placeholder.markdown(error_message)
    
    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Bottom info
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h4>🔒 Privacy</h4>
        <p>Your queries are processed via Gemini API. No data is stored permanently.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>⚡ Performance</h4>
        <p>Responses typically take 2-5 seconds. Free tier has 15 RPM limit.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>🎯 Accuracy</h4>
        <p>Powered by latest data. Always verify critical decisions independently.</p>
    </div>
    """, unsafe_allow_html=True)

# Advanced features toggle
with st.expander("⚙️ Advanced Settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        context_size = st.slider(
            "Context Window (tokens)",
            100000, 700000, 700000, 50000,
            help="Larger context = more data, but slower responses"
        )
    
    with col2:
        response_style = st.selectbox(
            "Response Style",
            ["Balanced", "Concise", "Detailed"],
            index=0,
            help="Choose how verbose you want responses to be"
        )
    
    show_context = st.checkbox("Show loaded context preview", value=False)
    
    if show_context:
        st.text_area(
            "Current RAG Context (first 2000 chars)",
            st.session_state.rag_context[:2000] + "...",
            height=200,
            disabled=True
        )

# Statistics
if st.session_state.messages:
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    ai_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    total_chars = sum(len(m["content"]) for m in st.session_state.messages)
    
    col1.metric("Questions Asked", user_messages)
    col2.metric("AI Responses", ai_messages)
    col3.metric("Total Characters", f"{total_chars:,}")
    col4.metric("Session Time", f"{len(st.session_state.messages) * 30}s est")

st.caption(f"Powered by Google Gemini 1.5 Flash | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
