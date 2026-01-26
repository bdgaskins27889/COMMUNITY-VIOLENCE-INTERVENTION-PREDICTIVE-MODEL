# CVI Risk Predictor - Portfolio Project Design

## Project Overview

**Project Name:** CVI Risk Predictor - Neighborhood Violence Risk Assessment Tool

**Author:** Barbara D. Gaskins

**Purpose:** Transform the academic research on predictive modeling for Community Violence Intervention into a fully functional, replicable data science tool that can be used by CVI organizations, public health departments, and violence prevention practitioners.

---

## Project Architecture

### 1. **Core Components**

#### A. Data Pipeline
- **Data Sources (All Publicly Available & Verifiable):**
  - Chicago Crime Data Portal (crime incidents)
  - ShotSpotter Alerts (gunfire detection)
  - Chicago Abandoned Buildings Dataset
  - OpenStreetMap API (infrastructure features)
  - CDC Social Vulnerability Index (SVI)
  - U.S. Census Bureau American Community Survey (ACS) data

#### B. Analysis Engine
- **Preprocessing Module:**
  - Geocoding and spatial alignment
  - Temporal aggregation (weekly)
  - Feature engineering
  - Data normalization and imputation

- **Modeling Module:**
  - Logistic Regression (interpretable baseline)
  - Random Forest Classification (complex patterns)
  - K-Means Clustering (risk tier grouping)

#### C. Visualization & Reporting
- Interactive maps (choropleth, heatmaps)
- Risk dashboards
- Exportable reports for CVI organizations

#### D. Web Application Interface
- User-friendly dashboard for non-technical users
- Neighborhood risk lookup
- Historical trend analysis
- Resource allocation recommendations

---

## Technical Stack

### Backend
- **Python 3.11+**
- **Core Libraries:**
  - `pandas`, `numpy` - Data manipulation
  - `geopandas`, `shapely` - Geospatial analysis
  - `scikit-learn` - Machine learning models
  - `requests` - API data retrieval
  - `sqlalchemy` - Database management

### Frontend
- **Web Framework:** Flask or FastAPI
- **Visualization:** Plotly, Folium (interactive maps)
- **UI:** HTML/CSS/JavaScript with Bootstrap

### Data Storage
- **SQLite** (for portability) or **PostgreSQL** (for production)
- **GeoJSON** files for spatial boundaries

---

## Key Features

### 1. **Automated Data Collection**
- Scripts to pull latest data from public APIs
- Scheduled updates (weekly/monthly)
- Data validation and quality checks

### 2. **Neighborhood Risk Scoring**
- Multi-factor risk assessment
- Interpretable risk scores (0-100 scale)
- Risk tier classification (Low, Moderate, High, Critical)

### 3. **Predictive Analytics**
- 1-week and 4-week risk forecasts
- Emerging hotspot identification
- Temporal pattern analysis

### 4. **Interactive Visualizations**
- Geographic heatmaps
- Time-series trends
- Feature importance charts
- Comparative neighborhood analysis

### 5. **Ethical Safeguards**
- No individual-level predictions
- Neighborhood-level aggregation only
- Transparent model explanations
- Bias acknowledgment documentation

### 6. **Replication Toolkit**
- Complete setup instructions
- Environment configuration files
- Sample datasets
- Step-by-step tutorial

---

## Project Structure

```
cvi-risk-predictor/
├── data/
│   ├── raw/                    # Raw data downloads
│   ├── processed/              # Cleaned and processed data
│   ├── boundaries/             # Neighborhood boundary files
│   └── README.md              # Data documentation
├── src/
│   ├── data_collection/       # API scripts and data downloaders
│   ├── preprocessing/         # Data cleaning and feature engineering
│   ├── modeling/              # ML model training and evaluation
│   ├── visualization/         # Plotting and mapping functions
│   └── utils/                 # Helper functions
├── models/
│   ├── trained_models/        # Saved model files
│   └── model_evaluation/      # Performance metrics
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_results_analysis.ipynb
├── app/
│   ├── static/                # CSS, JS, images
│   ├── templates/             # HTML templates
│   └── app.py                 # Web application
├── tests/
│   └── test_*.py              # Unit tests
├── docs/
│   ├── METHODOLOGY.md         # Detailed methodology
│   ├── ETHICAL_FRAMEWORK.md   # Ethical guidelines
│   ├── USER_GUIDE.md          # End-user documentation
│   └── API_DOCUMENTATION.md   # API reference
├── requirements.txt           # Python dependencies
├── environment.yml            # Conda environment
├── setup.py                   # Package installation
├── README.md                  # Project overview
└── LICENSE                    # Open source license
```

---

## Deliverables

### 1. **Functional Code Repository**
- Complete, documented, and tested codebase
- GitHub repository with clear README
- All code follows PEP 8 standards

### 2. **Interactive Web Application**
- Deployed locally or on cloud platform
- User-friendly interface for CVI practitioners
- Real-time risk assessment capabilities

### 3. **Comprehensive Documentation**
- Technical documentation for developers
- User guide for CVI organizations
- Ethical framework document
- Replication guide

### 4. **Portfolio Presentation Materials**
- Project overview document
- Key visualizations and findings
- Demo video or screenshots
- Link to live application (if deployed)

### 5. **Academic-Quality Report**
- Methodology documentation
- Model evaluation results
- Limitations and future work
- References and citations (APA format)

---

## Ethical Considerations

### Core Principles
1. **Prevention, Not Punishment:** Focus on community care, not surveillance
2. **Transparency:** Open methodology and interpretable models
3. **Community Benefit:** Designed to support CVI organizations, not law enforcement
4. **Bias Awareness:** Acknowledge and document data limitations
5. **Privacy Protection:** No individual-level data or predictions

### Implementation Safeguards
- Neighborhood-level aggregation (minimum population thresholds)
- Explicit rejection of individual risk scoring
- Clear documentation of intended use cases
- Community stakeholder input (documented in methodology)

---

## Success Metrics

### Technical Metrics
- Model accuracy, precision, recall (documented)
- Cross-validation performance
- Computational efficiency

### Practical Metrics
- Usability for non-technical users
- Replicability (can others run the code?)
- Adaptability (can it be used in other cities?)

### Portfolio Impact
- Demonstrates real-world data science application
- Shows ethical AI implementation
- Highlights domain expertise (criminal justice + data science)
- Provides tangible tool for social good

---

## Timeline Estimate

1. **Data Collection & Preparation:** 2-3 days
2. **Model Development & Training:** 2-3 days
3. **Web Application Development:** 3-4 days
4. **Documentation & Testing:** 2-3 days
5. **Final Review & Deployment:** 1-2 days

**Total:** ~10-15 days for complete implementation

---

## Next Steps

1. Confirm project scope and requirements with user
2. Set up project repository structure
3. Begin data collection from public sources
4. Develop data pipeline and preprocessing scripts
5. Train and evaluate models
6. Build web application interface
7. Create comprehensive documentation
8. Test replication process
9. Finalize portfolio materials

---

*This design document serves as the blueprint for transforming academic research into a production-ready data science portfolio project.*
