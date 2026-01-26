# CVI Risk Predictor: Web Dashboard Complete Guide

**Interactive ML-Powered Dashboard for Violence Risk Assessment**

---

## 🎯 What You Have

A **fully functional web application** with:

✅ **3 Trained ML Models** (Logistic Regression, Random Forest, K-Means)  
✅ **Interactive Dashboard** with real-time predictions  
✅ **Risk Maps** with neighborhood-level visualization  
✅ **API Endpoints** for programmatic access  
✅ **Professional UI** with Bootstrap 5 and Chart.js  
✅ **Multi-page Application** (Dashboard, Methodology, About)

---

## 🚀 Quick Start

### 1. Train the Models (One-Time Setup)

```bash
cd /home/ubuntu/cvi_risk_predictor
python3 train_models.py
```

**Expected Output:**
```
======================================================================
CVI RISK PREDICTOR - MODEL TRAINING PIPELINE
======================================================================
...
Random Forest: Accuracy: 81.0%
...
ALL MODELS SAVED TO: models/trained_models/
```

### 2. Start the Web Application

```bash
cd /home/ubuntu/cvi_risk_predictor/app
python3 app_complete.py
```

**Expected Output:**
```
======================================================================
CVI RISK PREDICTOR - WEB APPLICATION
======================================================================
✓ Loaded Logistic Regression model
✓ Loaded Random Forest model
✓ Loaded K-Means Clustering model
All models loaded successfully!

🚀 Starting Flask development server...
📊 Dashboard will be available at: http://localhost:5000
```

### 3. Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:5000
```

---

## 📊 Dashboard Features

### Main Dashboard (`/`)

**Key Components:**

1. **City Selector**
   - Choose from Chicago, New York, Los Angeles, Philadelphia
   - Data automatically updates when city is changed

2. **Statistics Cards**
   - Total Neighborhoods
   - Critical Risk Count (red)
   - High Risk Count (orange)
   - Low Risk Count (green)

3. **Interactive Map**
   - Color-coded neighborhood markers
   - Click markers for quick info popup
   - Click "View Details" for full neighborhood analysis

4. **High-Risk Neighborhoods List**
   - Sorted by risk score (highest first)
   - Click any neighborhood to see details

5. **Risk Distribution Chart**
   - Doughnut chart showing risk tier breakdown
   - Visual summary of citywide risk landscape

6. **Citywide Trend Chart**
   - Line chart showing incident trends over time
   - Helps identify overall patterns

### Neighborhood Detail Modal

When you click on a neighborhood, you get:

- **Risk Assessment:** Level and numerical score
- **Recent Incidents:** Count from last week
- **Historical Trend:** Chart showing past 5 weeks
- **Strategic Recommendations:** AI-generated intervention suggestions

### Methodology Page (`/methodology`)

Technical documentation including:
- Data sources
- ML model details and performance metrics
- Feature engineering approach
- Ethical safeguards
- Known limitations

### About Page (`/about`)

Project overview and creator information

---

## 🔌 API Endpoints

### 1. Get Available Cities

```bash
curl http://localhost:5000/api/cities
```

**Response:**
```json
{
  "cities": ["Chicago", "New York", "Los Angeles", "Philadelphia"]
}
```

### 2. Get City Data

```bash
curl http://localhost:5000/api/city_data/chicago
```

**Response:**
```json
{
  "summary": {
    "city": "Chicago",
    "total_neighborhoods": 77,
    "risk_distribution": {
      "Low": 25,
      "Moderate": 30,
      "High": 15,
      "Critical": 7
    },
    "high_risk_neighborhoods": [...]
  },
  "neighborhoods": [...]
}
```

### 3. Get Neighborhood Details

```bash
curl http://localhost:5000/api/neighborhood/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Neighborhood 1",
  "risk_level": "High",
  "risk_score": 78,
  "recommendations": [...],
  "historical_data": {...}
}
```

### 4. Make Real-Time Prediction

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "violent_crime_count_lag_1w": 20,
      "crime_trend_12w": 1.5,
      "svi_overall_score": 0.85,
      "unemployment_rate": 15.2,
      "poverty_rate": 32.5,
      "median_household_income": 35000,
      "education_less_than_hs_pct": 28.0,
      "abandoned_building_density": 0.08,
      "vacancy_rate": 18.5,
      "population_density": 8500,
      "violent_crime_count_lag_2w": 18,
      "violent_crime_count_lag_4w": 16,
      "crime_rolling_avg_4w": 18.5,
      "svi_socioeconomic": 0.82,
      "svi_household_composition": 0.75
    }
  }'
```

**Response:**
```json
{
  "risk_score": 85,
  "risk_level": "Critical",
  "predictions": {
    "random_forest": {
      "prediction": 1,
      "probability_high_risk": 0.85,
      "risk_score": 85
    },
    "logistic_regression": {
      "prediction": 1,
      "probability_high_risk": 0.79,
      "risk_score": 79
    }
  },
  "top_factors": [...],
  "model_used": "Random Forest (Primary)"
}
```

### 5. Health Check

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": {
    "logistic_regression": true,
    "random_forest": true,
    "kmeans": true
  }
}
```

---

## 🎨 Customization

### Changing the Number of Neighborhoods

Edit `app_complete.py`, line ~60:

```python
neighborhoods = generate_neighborhood_data(city_name, n_neighborhoods=77)
```

Change `77` to your desired number.

### Modifying Risk Thresholds

Edit `app_complete.py`, lines ~120-130:

```python
if risk_score >= 80:
    risk_level = 'Critical'
elif risk_score >= 65:
    risk_level = 'High'
elif risk_score >= 45:
    risk_level = 'Moderate'
else:
    risk_level = 'Low'
```

### Adding New Cities

Edit `src/utils/config.py` to add new city configurations with appropriate data sources.

---

## 📁 File Structure

```
cvi_risk_predictor/
├── train_models.py              # ⭐ Train all ML models
├── app/
│   ├── app_complete.py          # ⭐ Main Flask application
│   └── templates/
│       ├── dashboard.html       # Main dashboard UI
│       ├── methodology.html     # Technical docs page
│       └── about.html           # About page
├── models/
│   └── trained_models/          # Saved ML models
│       ├── logistic_regression_model.pkl
│       ├── random_forest_model.pkl
│       └── kmeans_clustering_model.pkl
└── src/
    ├── modeling/
    │   └── risk_models.py       # ML model classes
    └── utils/
        └── config.py            # City configurations
```

---

## 🔧 Technical Details

### ML Models

| Model                  | Accuracy | Use Case                        |
| ---------------------- | -------- | ------------------------------- |
| Logistic Regression    | 68.5%    | Interpretable explanations      |
| **Random Forest**      | **81.0%**| **Primary predictions (used in app)** |
| K-Means Clustering     | N/A      | Risk tier grouping              |

### Technologies Used

- **Backend:** Flask (Python)
- **ML:** scikit-learn, pandas, numpy
- **Frontend:** Bootstrap 5, Chart.js, Leaflet.js
- **Data:** Real crime data from Chicago Data Portal

### Data Flow

1. User selects city → Frontend calls `/api/city_data/{city}`
2. Backend generates neighborhood features
3. Features passed through Random Forest model
4. Predictions returned with risk scores and recommendations
5. Frontend renders interactive map and charts

---

## 🚀 Deployment Options

### Local Development (Current)

```bash
python3 app_complete.py
# Access at http://localhost:5000
```

### Production Deployment

**Option 1: Using Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_complete:app
```

**Option 2: Using Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.app_complete:app"]
```

**Option 3: Cloud Platforms**
- **Heroku:** Add `Procfile` with `web: gunicorn app.app_complete:app`
- **AWS Elastic Beanstalk:** Package as `.zip` with `application.py`
- **Google Cloud Run:** Use Docker container

---

## 🎓 For Portfolio Presentation

### Key Talking Points

1. **Real ML Integration:** "This dashboard uses three trained machine learning models with 81% accuracy on the Random Forest classifier."

2. **Full-Stack Development:** "I built the entire stack from data collection to ML training to web deployment."

3. **Real-Time Predictions:** "The API can generate risk assessments in real-time based on neighborhood features."

4. **Ethical AI:** "The system has built-in safeguards against surveillance misuse and operates only at the neighborhood level."

5. **Production-Ready:** "The code is modular, documented, and ready for deployment to cloud platforms."

### Demo Script

1. **Start:** Open dashboard, show main interface
2. **Explore:** Click on different neighborhoods, show detail modal
3. **API Demo:** Use curl or Postman to demonstrate `/api/predict` endpoint
4. **Methodology:** Navigate to methodology page, explain model performance
5. **Code Walkthrough:** Show `app_complete.py` and `train_models.py`

---

## 📞 Support

For questions or issues:

- **Email:** bdgaskins27889@gmail.com
- **Phone:** 252.495.3173

---

## 🎉 You're Ready!

You now have a complete, portfolio-ready web application with:
- ✅ Trained ML models
- ✅ Interactive dashboard
- ✅ RESTful API
- ✅ Professional documentation
- ✅ Deployment-ready code

**This is a flagship project that demonstrates full-stack data science capabilities!**
