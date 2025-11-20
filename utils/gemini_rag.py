"""
PulseAI - Gemini RAG Engine (1M Context Window)
Zero vector DB, pure context stuffing with intelligent chunking
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from .prompts import (
    SYSTEM_PROMPT, RAG_QUERY_PROMPT, REPORT_GENERATION_PROMPT,
    FORECAST_NARRATIVE_PROMPT, ANOMALY_DETECTION_PROMPT, FEW_SHOT_EXAMPLES
)

# Load environment variables from .env file
load_dotenv()


class GeminiRAG:
    def __init__(self, api_key=None):
        """Initialize Gemini with free tier limits"""
        # Try multiple sources for API key (secure priority order)
        self.api_key = (
            api_key or 
            os.getenv("GEMINI_API_KEY") or  # From .env file
            st.secrets.get("GEMINI_API_KEY")  # From Streamlit secrets (cloud deployment)
        )
        
        if not self.api_key:
            st.error("⚠️ GEMINI_API_KEY not found! Add it to .streamlit/secrets.toml")
            st.stop()
        
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.5 Flash - latest model with enhanced capabilities
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
        
        # Rate limiting (15 RPM free tier)
        self.last_request_time = 0
        self.min_request_interval = 4  # seconds (15 RPM = 4s interval)
    
    def _rate_limit(self):
        """Enforce free tier rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def build_context_from_data(self, data_dict, max_tokens=700000):
        """Build comprehensive context from all datasets"""
        context_parts = []
        
        # Add few-shot examples first
        context_parts.append("=== REFERENCE EXAMPLES ===\n" + FEW_SHOT_EXAMPLES)
        
        # UPI Data Summary
        if 'upi' in data_dict and not data_dict['upi'].empty:
            df = data_dict['upi']
            recent = df.tail(12)
            
            upi_summary = f"""
=== UPI TRANSACTION DATA (Last 12 Months) ===
Latest Month: {recent.iloc[-1]['Month']}
Latest Volume: {recent.iloc[-1]['Volume_Billion']:.2f} billion transactions
Latest Value: ₹{recent.iloc[-1]['Value_LakhCrore']:.2f} lakh crore
Average Transaction Size: ₹{recent.iloc[-1]['Avg_Transaction_Size']:.2f}

Monthly Trend:
{recent[['Month', 'Volume_Billion', 'Value_LakhCrore']].to_string(index=False)}

Key Insights:
- YoY Growth: {((recent.iloc[-1]['Volume_Billion'] / recent.iloc[-12]['Volume_Billion'] - 1) * 100):.1f}%
- Peak Month: {recent.loc[recent['Volume_Billion'].idxmax(), 'Month']}
- Average Monthly Volume: {recent['Volume_Billion'].mean():.2f} billion
"""
            context_parts.append(upi_summary)
        
        # RBI Credit Data
        if 'rbi_credit' in data_dict and not data_dict['rbi_credit'].empty:
            df = data_dict['rbi_credit']
            top_states = df.nlargest(10, 'Credit_Crore')
            
            credit_summary = f"""
=== RBI STATE-WISE BANKING DATA (As of {df.iloc[0]['As_Of_Date']}) ===
Total States Covered: {len(df)}

Top 10 States by Credit Outstanding:
{top_states[['State', 'Credit_Crore', 'Credit_Growth_%', 'CD_Ratio', 'Digital_Adoption_%']].to_string(index=False)}

National Averages:
- Average Credit Growth: {df['Credit_Growth_%'].mean():.2f}%
- Average CD Ratio: {df['CD_Ratio'].mean():.2f}%
- Average Digital Adoption: {df['Digital_Adoption_%'].mean():.2f}%

Fastest Growing States (Credit):
{df.nlargest(5, 'Credit_Growth_%')[['State', 'Credit_Growth_%']].to_string(index=False)}

Highest Digital Adoption:
{df.nlargest(5, 'Digital_Adoption_%')[['State', 'Digital_Adoption_%']].to_string(index=False)}
"""
            context_parts.append(credit_summary)
        
        # NSE Stocks
        if 'nse' in data_dict and not data_dict['nse'].empty:
            df = data_dict['nse']
            
            nse_summary = f"""
=== NSE TOP 10 STOCKS (As of {df.iloc[0]['Date']}) ===
{df[['Symbol', 'LTP', 'Change_%', 'High', 'Low']].to_string(index=False)}

Market Snapshot:
- Top Gainer: {df.loc[df['Change_%'].idxmax(), 'Symbol']} ({df['Change_%'].max():.2f}%)
- Top Loser: {df.loc[df['Change_%'].idxmin(), 'Symbol']} ({df['Change_%'].min():.2f}%)
- Average Change: {df['Change_%'].mean():.2f}%
"""
            context_parts.append(nse_summary)
        
        # Mutual Funds
        if 'mutual_funds' in data_dict and not data_dict['mutual_funds'].empty:
            df = data_dict['mutual_funds']
            latest_month = df['Month'].max()
            latest_data = df[df['Month'] == latest_month]
            
            mf_summary = f"""
=== MUTUAL FUND AUM DATA ({latest_month}) ===
Category-wise AUM:
{latest_data[['Category', 'AUM_LakhCrore', 'Accounts_Lakh']].to_string(index=False)}

Total Industry AUM: ₹{latest_data['AUM_LakhCrore'].sum():.2f} lakh crore
Total Investor Accounts: {latest_data['Accounts_Lakh'].sum():.2f} lakh
"""
            context_parts.append(mf_summary)
        
        # RBI Policy
        if 'rbi_policy' in data_dict and not data_dict['rbi_policy'].empty:
            df = data_dict['rbi_policy']
            latest = df.iloc[-1]
            
            policy_summary = f"""
=== RBI MONETARY POLICY (Latest: {latest['Date']}) ===
Current Rates:
- Repo Rate: {latest['Repo_Rate']}%
- Reverse Repo Rate: {latest['Reverse_Repo']}%
- CRR: {latest['CRR']}%
- SLR: {latest['SLR']}%
- Policy Stance: {latest['Policy_Stance']}

Recent Changes:
{df.tail(6)[['Date', 'Repo_Rate', 'Policy_Stance']].to_string(index=False)}
"""
            context_parts.append(policy_summary)
        
        # Join all parts
        full_context = "\n\n".join(context_parts)
        
        # Truncate if needed (rough estimate: 1 token ≈ 4 chars)
        max_chars = max_tokens * 4
        if len(full_context) > max_chars:
            full_context = full_context[:max_chars] + "\n\n[Context truncated to fit token limit]"
        
        return full_context
    
    def query(self, question, context, stream=False):
        """Query Gemini with RAG context"""
        self._rate_limit()
        
        # Build prompt
        prompt = RAG_QUERY_PROMPT.format(context=context, question=question)
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
        
        try:
            if stream:
                response = self.model.generate_content(full_prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            else:
                response = self.model.generate_content(full_prompt)
                return response.text
        
        except Exception as e:
            error_msg = f"Error querying Gemini: {str(e)}"
            if "429" in str(e) or "quota" in str(e).lower():
                error_msg = "⚠️ Rate limit exceeded. Free tier allows 15 requests/minute. Please wait..."
            return error_msg
    
    def generate_report_summary(self, data_summary, month_year):
        """Generate executive summary for boardroom report"""
        self._rate_limit()
        
        prompt = REPORT_GENERATION_PROMPT.format(
            month_year=month_year,
            data_summary=data_summary
        )
        
        try:
            response = self.model.generate_content(f"{SYSTEM_PROMPT}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def generate_forecast_narrative(self, metric_name, current_value, predicted_value, change_percent, trend):
        """Generate storytelling narrative for forecasts"""
        self._rate_limit()
        
        prompt = FORECAST_NARRATIVE_PROMPT.format(
            metric_name=metric_name,
            current_value=current_value,
            predicted_value=predicted_value,
            change_percent=change_percent,
            trend=trend
        )
        
        try:
            response = self.model.generate_content(f"{SYSTEM_PROMPT}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Error generating narrative: {str(e)}"
    
    def detect_anomalies(self, data_points):
        """Detect anomalies in financial data"""
        self._rate_limit()
        
        prompt = ANOMALY_DETECTION_PROMPT.format(data_points=data_points)
        
        try:
            response = self.model.generate_content(f"{SYSTEM_PROMPT}\n\n{prompt}")
            return response.text
        except Exception as e:
            return f"Error detecting anomalies: {str(e)}"
    
    def get_chart_insights(self, chart_type, data_summary):
        """Generate insights from chart data"""
        self._rate_limit()
        
        prompt = f"""Analyze this {chart_type} and provide 3 key business insights:

Data Summary:
{data_summary}

Provide insights in this format:
• [Insight 1]
• [Insight 2]
• [Insight 3]
"""
        
        try:
            response = self.model.generate_content(f"{SYSTEM_PROMPT}\n\n{prompt}")
            return response.text
        except Exception as e:
            return "Unable to generate insights at this time."


# Global instance (initialized in app)
_rag_instance = None

def get_rag_instance():
    """Get or create RAG instance"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = GeminiRAG()
    return _rag_instance


if __name__ == "__main__":
    # Test RAG
    rag = GeminiRAG()
    test_context = "UPI transactions in Oct 2025: 16.5 billion, ₹20.64 lakh crore"
    response = rag.query("What was UPI volume in Oct 2025?", test_context)
    print(response)
