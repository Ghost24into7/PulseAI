# 📊 PulseAI - Real-Time Indian Financial Intelligence Engine

<div align="center">

![PulseAI Banner](https://img.shields.io/badge/PulseAI-Financial_Intelligence-gold?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAowAAAKMB8MeazgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADJSURBVCiRY2AYBaNgFAyEwP///xkYGBj+//8P)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-4285F4?style=flat-square&logo=google)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Enterprise-grade financial analytics platform for Indian markets • Zero-GPU • CPU-only • Free-tier AI**

[🚀 Live Demo](#) | [📖 Documentation](#features) | [🤝 Contributing](#contributing)

</div>

---

## 🌟 What is PulseAI?

PulseAI is a **production-ready, zero-GPU financial intelligence platform** designed specifically for Indian financial markets. Built with enterprise-grade standards, it delivers real-time insights from RBI, NPCI, NSE, and AMFI using **Google Gemini 1.5 Flash's 1-million token context window** without any vector database.

### 💎 Why PulseAI Stands Out

- ✅ **Zero Infrastructure Costs** - Runs on CPU, no GPU required
- ✅ **Free AI Integration** - Gemini 1.5 Flash free tier (15 RPM)
- ✅ **No Vector DB** - Pure RAG with 1M context stuffing
- ✅ **One-Click Deploy** - Streamlit Community Cloud ready
- ✅ **RBI-Grade Design** - Premium navy blue + gold theme
- ✅ **Production Ready** - Caching, error handling, rate limiting
- ✅ **Mobile Responsive** - Perfect on all devices

---

## 🎯 Key Features

### 🏠 Interactive Dashboard
- Real-time UPI transaction trends (24-month history)
- State-wise banking credit & deposit analysis
- NSE top 10 stock performance
- Mutual fund AUM breakdown
- Animated leaderboards with tier classification

### 🇮🇳 India Choropleth Map
- Geographic visualization of financial metrics
- State-wise drill-down capabilities
- Toggle between credit growth, deposits, CD ratio, digital adoption
- Heatmap comparison matrix
- Interactive gauge charts

### 💬 Ask RBI Chat (AI-Powered RAG)
- ChatGPT-style interface with streaming responses
- 700K+ tokens of financial context
- Bilingual support (English + Hindi)
- Example questions library
- Sources citation for transparency

### 📊 Automated Boardroom Reports
- One-click PowerPoint generation (12+ slides)
- RBI-themed professional design
- AI-written executive summaries
- Auto-generated charts and insights
- Anomaly detection alerts
- 30-day forecast integration

### 🔮 Forecasting Engine
- Time-series predictions for UPI, credit, markets
- 95% confidence intervals
- AI-generated business narratives
- Interactive visualizations
- Exportable CSV forecasts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PulseAI Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [Streamlit UI] ← Custom CSS (Glassmorphism + RBI Theme)    │
│         ↓                                                     │
│  [Data Layer] → Smart Caching (24h) + Polite Scraping       │
│         ↓                                                     │
│  ┌─────────────────┬──────────────────┬──────────────────┐ │
│  │   RBI DBIE      │   NPCI UPI       │   NSE Stocks     │ │
│  │   (Banking)     │   (Payments)     │   (Markets)      │ │
│  └─────────────────┴──────────────────┴──────────────────┘ │
│         ↓                                                     │
│  [Gemini 1.5 Flash] → 1M Context RAG (No Vector DB)         │
│         ↓                                                     │
│  [Analysis & Forecasting] → Exponential Smoothing            │
│         ↓                                                     │
│  [PowerPoint Generator] → python-pptx with RBI Template      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Tech Stack:**
- **Frontend:** Streamlit 1.39.0, Plotly, Custom CSS
- **AI:** Google Gemini 1.5 Flash (free tier)
- **Data:** Pandas, NumPy, Requests
- **Reports:** python-pptx
- **Deployment:** CPU-only, no Docker needed

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Google Gemini API key (free tier)
- Git

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/Ghost24into7/PulseAI.git
cd PulseAI/pulseai
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the `pulseai` directory:
```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` and add your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

Get your free API key: [Google AI Studio](https://aistudio.google.com/app/apikey)

**⚠️ IMPORTANT:** Never commit `.env` file to GitHub! It's already in `.gitignore`.

5. **Run the app**
```bash
streamlit run app.py
```

6. **Open in browser**
```
http://localhost:8501
```

---

## ☁️ Deploy to Streamlit Cloud (One-Click)

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your forked repository
5. Set main file path: `pulseai/app.py`
6. Add secrets in "Advanced settings" → "Secrets":
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
7. Click "Deploy"

🎉 Your app will be live in 2-3 minutes!

---

## 📸 Screenshots

### Dashboard
![Dashboard Preview](https://via.placeholder.com/800x450/0f1b3d/d4af37?text=Dashboard+Preview)
*Real-time financial metrics with interactive charts*

### India Map
![India Map](https://via.placeholder.com/800x450/0f1b3d/d4af37?text=Interactive+India+Map)
*State-wise geographic analysis*

### AI Chat
![AI Chat](https://via.placeholder.com/800x450/0f1b3d/d4af37?text=AI+Powered+Chat)
*RAG-based question answering*

### Report Generator
![Report](https://via.placeholder.com/800x450/0f1b3d/d4af37?text=Boardroom+Reports)
*One-click PowerPoint generation*

### Forecasting
![Forecasting](https://via.placeholder.com/800x450/0f1b3d/d4af37?text=30-Day+Forecasts)
*AI-narrated predictions*

---

## 📊 Data Sources

| Source | Data | Update Frequency |
|--------|------|------------------|
| **RBI DBIE** | Banking credit, deposits, monetary policy | Monthly |
| **NPCI** | UPI transactions, volumes, values | Monthly |
| **NSE** | Stock indices, top performers | Daily |
| **AMFI** | Mutual fund AUM, categories | Monthly |

All data is **cached for 24 hours** to respect rate limits and improve performance.

---

## 🎨 Design Philosophy

PulseAI follows **RBI's visual identity**:
- **Primary Color:** Navy Blue (#0f1b3d) - Trust & authority
- **Accent Color:** Gold (#d4af37) - Premium & excellence
- **Typography:** Inter font family
- **Effects:** Glassmorphism, subtle animations, responsive design

Designed to look professional in:
- Board meetings
- Investor presentations
- Regulatory reports
- Executive dashboards

---

## 🔑 Configuration

### Streamlit Config (`.streamlit/config.toml`)
```toml
[theme]
primaryColor = "#d4af37"        # Gold
backgroundColor = "#0f1b3d"     # Navy Blue
secondaryBackgroundColor = "#1a2847"
textColor = "#ecf0f1"

[server]
headless = true
port = 8501
```

### Environment Variables
- `GEMINI_API_KEY` - Your Google Gemini API key (required)

---

## 📁 Project Structure

```
pulseai/
├── app.py                      # Main landing page
├── pages/
│   ├── 1_🏠_Dashboard.py       # Interactive dashboard
│   ├── 2_🇮🇳_India_Map.py      # Geographic analysis
│   ├── 3_💬_Ask_RBI_Chat.py    # AI chatbot
│   ├── 4_📊_Automated_Report.py # PPT generator
│   └── 5_🔮_Forecasting.py     # Predictions
├── utils/
│   ├── data_downloader.py      # Data fetching + caching
│   ├── gemini_rag.py           # RAG engine
│   ├── ppt_generator.py        # PowerPoint creation
│   └── prompts.py              # AI prompts
├── assets/
│   ├── custom.css              # Premium styling (200+ lines)
│   └── logo.png.txt            # Logo placeholder
├── data/
│   ├── raw/                    # Downloaded CSVs (gitignored)
│   └── processed/              # Cleaned data
├── .streamlit/
│   ├── config.toml             # Theme configuration
│   └── secrets.toml            # API keys (gitignored)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🛠️ Advanced Usage

### Custom Data Sources
Add new data sources in `utils/data_downloader.py`:
```python
def download_custom_data():
    cache_file = DATA_DIR / "custom_data.csv"
    if is_cache_valid(cache_file):
        return pd.read_csv(cache_file)
    # Your download logic
    return df
```

### Custom AI Prompts
Modify prompts in `utils/prompts.py`:
```python
CUSTOM_PROMPT = """Your custom prompt template..."""
```

### Styling
Edit `assets/custom.css` to match your brand colors.

---

## 🚨 Troubleshooting

### API Key Issues
```
⚠️ GEMINI_API_KEY not found!
```
**Solution:** Add your API key to `.streamlit/secrets.toml`

### Rate Limit Exceeded
```
⚠️ Rate limit exceeded. Free tier allows 15 requests/minute.
```
**Solution:** Wait 60 seconds between requests. Upgrade to paid tier if needed.

### Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Run `pip install -r requirements.txt`

### Data Not Loading
**Solution:** Check internet connection. Data sources may be temporarily unavailable.

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Areas for contribution:**
- Additional data sources (RBI reports, SEBI data)
- More forecasting models
- Enhanced visualizations
- Multi-language support
- Unit tests
- Documentation improvements

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**Important:** PulseAI is designed for **educational and analytical purposes only**. 

- Not financial advice
- Data may have delays or inaccuracies
- Always verify critical decisions independently
- Not affiliated with RBI, NPCI, NSE, or AMFI
- Use at your own risk

---

## 🙏 Acknowledgments

- **Google Gemini** for free-tier AI access
- **Streamlit** for the amazing framework
- **RBI, NPCI, NSE, AMFI** for public data
- **Open-source community** for libraries

---

## 📧 Contact & Support

- **GitHub Issues:** [Report a bug](https://github.com/Ghost24into7/PulseAI/issues)
- **Email:** your.email@example.com
- **LinkedIn:** [Your Profile](#)

---

## 🌟 Star History

If PulseAI helped you, please ⭐ star this repository!

[![Star History Chart](https://api.star-history.com/svg?repos=Ghost24into7/PulseAI&type=Date)](https://star-history.com/#Ghost24into7/PulseAI&Date)

---

<div align="center">

**Built with ❤️ for India's fintech ecosystem**

**November 2025**

[⬆ Back to Top](#-pulseai---real-time-indian-financial-intelligence-engine)

</div>
