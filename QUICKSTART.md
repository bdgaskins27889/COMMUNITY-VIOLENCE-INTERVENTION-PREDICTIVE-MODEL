# CVI Risk Predictor: Quick Start Guide

**Get up and running in 5 minutes!**

---

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Internet connection (for data collection)

---

## Installation Steps

### 1. Extract the Project

```bash
tar -xzf cvi_risk_predictor_portfolio.tar.gz
cd cvi_risk_predictor
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- pandas, numpy, scikit-learn (data science)
- geopandas, shapely, folium (geospatial)
- flask (web application)
- sodapy (data collection)

---

## Running the Demo

### Option 1: Data Collection Demo (Recommended First Step)

This script fetches **real crime data** from Chicago's public API:

```bash
python demo_data_collection.py
```

**Expected Output:**
```
======================================================================
CVI RISK PREDICTOR - DATA COLLECTION DEMO
======================================================================
📍 City: Chicago
📅 Time Period: Last 30 days
...
Successfully fetched 3,391 crime records
✓ Data saved to: data/raw/chicago_crime_demo_20260123.csv
======================================================================
DEMO COMPLETE!
======================================================================
```

### Option 2: Launch Web Application

```bash
cd app
python app.py
```

Then open your browser to: **http://localhost:5000**

You'll see:
- Interactive risk map
- City-wide statistics dashboard
- Neighborhood-level risk assessments

---

## Project Structure Overview

```
cvi_risk_predictor/
├── README.md                    # Full project documentation
├── PORTFOLIO_SUMMARY.md         # Portfolio presentation
├── demo_data_collection.py      # ⭐ Start here!
├── requirements.txt             # Python dependencies
├── data/
│   ├── DATA_SOURCES.md          # Data documentation
│   └── raw/                     # Downloaded data goes here
├── src/
│   ├── data_collection/         # Data fetching scripts
│   ├── preprocessing/           # Feature engineering
│   ├── modeling/                # ML models
│   └── utils/                   # Configuration
├── app/
│   ├── app.py                   # Web application
│   └── templates/               # HTML interface
└── docs/
    ├── METHODOLOGY.md           # Technical details
    ├── ETHICAL_FRAMEWORK.md     # Ethical guidelines
    ├── USER_GUIDE.md            # For CVI practitioners
    └── API_DOCUMENTATION.md     # API reference
```

---

## Next Steps

1. **Review the Data:** Check `data/raw/` for the collected crime data
2. **Read the Docs:** Explore `docs/METHODOLOGY.md` for technical details
3. **Customize:** Edit `src/utils/config.py` to add new cities
4. **Train Models:** Use the collected data to train ML models
5. **Deploy:** Follow deployment instructions in `README.md`

---

## Common Issues

### Issue: "ModuleNotFoundError"
**Solution:** Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

### Issue: "API rate limit exceeded"
**Solution:** 
- Get a free Socrata app token: https://dev.socrata.com/
- Set environment variable: `export SOCRATA_APP_TOKEN=your_token`

### Issue: "No data returned"
**Solution:** Check your internet connection and verify the Chicago Data Portal is accessible

---

## Getting Help

- **Full Documentation:** See `README.md`
- **Email:** bdgaskins27889@gmail.com
- **GitHub Issues:** Open an issue on the repository

---

**Ready to make an impact? Let's get started!** 🚀
