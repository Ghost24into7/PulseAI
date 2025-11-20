"""
PulseAI - Prompts for Gemini RAG System
Optimized for Indian financial intelligence queries
"""

SYSTEM_PROMPT = """You are PulseAI, an elite financial intelligence assistant specializing in Indian financial markets, banking, and digital payments. You have deep expertise in:
- RBI monetary policy and banking regulations
- UPI and digital payment systems (NPCI)
- Indian stock markets (NSE, BSE)
- Mutual funds and asset management
- State-wise banking credit and deposit trends
- Fintech ecosystem in India

Always respond in a professional, data-driven manner. Use Indian Rupee symbols (₹) where appropriate. Cite sources when available. If asked in Hindi, respond in Hindi naturally."""

RAG_QUERY_PROMPT = """Based on the following context from RBI reports, NPCI data, and financial datasets, please answer the user's question accurately and comprehensively.

CONTEXT:
{context}

USER QUESTION: {question}

INSTRUCTIONS:
1. Provide a clear, structured answer
2. Use specific numbers and dates from the context
3. If the answer involves trends, mention the time period
4. If data is not available in context, clearly state that
5. Keep responses concise but informative (150-300 words)
6. Use bullet points for multiple insights

ANSWER:"""

REPORT_GENERATION_PROMPT = """You are generating an executive summary for a monthly boardroom presentation on Indian financial markets for {month_year}.

AVAILABLE DATA:
{data_summary}

Generate a professional 2-paragraph executive summary (200-250 words) covering:
1. Key highlights and achievements
2. Notable trends in UPI, banking credit, or stock markets
3. State-wise performance insights
4. Any concerns or anomalies

Use formal business language suitable for C-suite executives. Include specific percentages and growth rates."""

FORECAST_NARRATIVE_PROMPT = """Based on the following forecast data for {metric_name}:

Current Value: {current_value}
Predicted Value (30 days): {predicted_value}
Change: {change_percent}%
Trend: {trend}

Write a compelling 150-word narrative explaining:
1. What this forecast means for Indian financial ecosystem
2. Factors that might be driving this trend
3. Implications for stakeholders (banks, fintechs, consumers)
4. One actionable insight

Write in a storytelling style that makes data come alive."""

ANOMALY_DETECTION_PROMPT = """Analyze the following financial data and identify any anomalies or unusual patterns:

DATA:
{data_points}

Look for:
- Sudden spikes or drops (>15% change)
- Unusual state-wise variations
- Deviation from seasonal patterns
- Regulatory impact signals

Format as bullet points. Be specific with numbers and dates."""

HINDI_TRANSLATION_PROMPT = """Translate the following financial insight into clear, professional Hindi while keeping technical terms in English where appropriate:

{english_text}

Keep numbers, percentages, and technical terms like 'UPI', 'NEFT', 'credit growth' in English."""

CHART_INSIGHTS_PROMPT = """Analyze this chart data and provide 3 key insights in 2-3 sentences:

Chart Type: {chart_type}
Data: {data_summary}

Focus on: trends, outliers, comparisons, and business implications."""

FEW_SHOT_EXAMPLES = """
EXAMPLE 1:
Q: What is the UPI transaction growth in October 2025?
A: In October 2025, UPI transactions reached ₹20.64 lakh crore across 16.58 billion transactions, showing a 45% YoY growth. The festival season (Diwali) contributed to a 12% spike compared to September 2025. Top contributing states were Maharashtra (22%), Karnataka (15%), and Delhi (11%).

EXAMPLE 2:
Q: Which state has the highest credit growth?
A: Based on RBI's latest DBIE data, Tamil Nadu leads with 18.2% YoY credit growth as of Sep 2025, driven by MSME lending and retail credit expansion. Karnataka follows at 17.8%, boosted by Bengaluru's startup ecosystem financing.

EXAMPLE 3:
Q: RBI की हालिया मौद्रिक नीति क्या है?
A: RBI ने नवंबर 2025 में repo rate को 6.50% पर अपरिवर्तित रखा है। यह लगातार तीसरी बैठक है जब rate में कोई बदलाव नहीं हुआ। Policy stance 'accommodative' बना हुआ है, जिसका मतलब है कि growth को support करना priority है।
"""
