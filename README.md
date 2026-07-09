# CVI Risk Predictor

**Neighborhood Violence Risk Assessment Tool for Community Violence Intervention Organizations**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21271446.svg)](https://doi.org/10.5281/zenodo.21271446)[![ORCID](https://img.shields.io/badge/ORCID-0009--0007--9915--944X-green)](https://orcid.org/0009-0007-9915-944X)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 📋 Project Overview

The **CVI Risk Predictor** is a data science tool designed to support Community Violence Intervention (CVI) organizations in making proactive, data-driven decisions about resource allocation and intervention strategies. By analyzing publicly available crime, socioeconomic, and environmental data at the neighborhood level, this tool provides actionable risk assessments that help CVI teams anticipate and prevent violence.

### 🛡️ Integration with BIAS-VI API

This predictive model is designed to operate in tandem with the [**BIAS-VI API**](https://github.com/bdgaskins27889/bias-vi-api) (Behavioral Indicators and Stress Variables – Violence Intervention). While this repository handles the macro-level spatial and socioeconomic risk predictions, the BIAS-VI API serves as the upstream cultural safety layer—ensuring that any natural language processing or field notes analyzed within these risk zones are free from cultural misclassification and false positives. Together, they form a complete, anti-surveillance intelligence suite for CVI operations.

### Key Features

✅ **Multi-City Support** - Adaptable to Chicago, New York, Los Angeles, Philadelphia, and other cities✅ **Real-Time Data Collection** - Automated data pipelines from public APIs✅ **Machine Learning Models** - Logistic Regression, Random Forest, and K-Means Clustering✅ **Interactive Web Dashboard** - User-friendly interface for non-technical users✅ **Ethical AI Framework** - Neighborhood-level only, no individual predictions✅ **Fully Replicable** - Complete documentation and setup instructions

---

## 🎯 Purpose and Use Cases

### Intended Use

- **Community Violence Intervention (CVI) Programs** - Prioritize outreach and mediation efforts

- **Public Health Departments** - Allocate violence prevention resources

- **Nonprofit Organizations** - Support grant applications with data-driven insights

- **Researchers** - Study place-based violence prevention strategies

### Prohibited Use

❌ **Law enforcement surveillance**❌ **Individual-level predictions**❌ **Predictive policing**❌ **Discriminatory targeting**

---

## 🏗️ Architecture

```
cvi-risk-predictor/
├── data/                          # Data storage
│   ├── raw/                       # Raw data downloads
│   ├── processed/                 # Cleaned and processed data
│   └── boundaries/                # Geographic boundary files
├── src/                           # Source code
│   ├── data_collection/           # API data fetchers
│   ├── preprocessing/             # Data cleaning and feature engineering
│   ├── modeling/                  # Machine learning models
│   ├── visualization/             # Plotting and mapping
│   └── utils/                     # Configuration and helpers
├── models/                        # Trained model files
├── notebooks/                     # Jupyter notebooks for analysis
├── app/                           # Web application
│   ├── app.py                     # Flask application
│   ├── templates/                 # HTML templates
│   └── static/                    # CSS, JS, images
├── tests/                         # Unit tests
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher

- pip package manager

- (Optional) Census API key - [Get free key here](https://api.census.gov/data/key_signup.html)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/bdgaskins27889/COMMUNITY-VIOLENCE-INTERVENTION-PREDICTIVE-MODEL.git
cd COMMUNITY-VIOLENCE-INTERVENTION-PREDICTIVE-MODEL
```

1. **Create virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

1. **Set up environment variables** (optional )

```bash
# Create .env file
echo "CENSUS_API_KEY=your_key_here" > .env
echo "SOCRATA_APP_TOKEN=your_token_here" >> .env
```

### Running the Application

#### Option 1: Web Dashboard

```bash
cd app
python app.py
```

Then open your browser to `http://localhost:5000`

#### Option 2: Command Line Analysis

```bash
python -m src.data_collection.crime_data --city chicago --start-date 2023-01-01 --end-date 2024-01-01
```

#### Option 3: Jupyter Notebooks

```bash
jupyter notebook notebooks/
```

---

## 📊 Data Sources

All data sources are **publicly available** and **verifiable**:

### Crime Data

- **Chicago**: [Chicago Data Portal](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)

- **New York**: [NYC Open Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date/5uac-w243)

- **Los Angeles**: [LA Open Data](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8)

- **Philadelphia**: [OpenDataPhilly](https://opendataphilly.org/datasets/crime-incidents/)

### Socioeconomic Data

- **US Census Bureau**: [American Community Survey (ACS)](https://www.census.gov/data/developers/data-sets/acs-5year.html)

- **CDC**: [Social Vulnerability Index (SVI)](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html)

### Environmental Data

- **OpenStreetMap**: [Overpass API](https://overpass-api.de/)

- **City Open Data Portals**: Abandoned buildings, infrastructure

---

## 🤖 Methodology

### Feature Engineering

**Temporal Features:**

- Weekly crime counts and trends

- Seasonal patterns

- Day-of-week distributions

**Spatial Features:**

- Neighborhood-level aggregation

- Spatial density calculations

- Geographic clustering

**Socioeconomic Features:**

- Median household income

- Unemployment rate

- Poverty rate

- Educational attainment

**Vulnerability Features:**

- CDC Social Vulnerability Index (overall and by theme)

- Housing vacancy rates

- Environmental disorder indicators

### Machine Learning Models

#### 1. Logistic Regression

- **Purpose**: Interpretable baseline model

- **Advantages**: Transparent coefficients, fast training

- **Use Case**: Understanding key risk factors

#### 2. Random Forest Classifier

- **Purpose**: Capture complex non-linear patterns

- **Advantages**: High accuracy, feature importance

- **Use Case**: Operational predictions

#### 3. K-Means Clustering

- **Purpose**: Group neighborhoods into risk tiers

- **Advantages**: Unsupervised, intuitive groupings

- **Use Case**: Resource allocation prioritization

### Model Evaluation

- **Accuracy, Precision, Recall, F1-Score**

- **Cross-validation** (5-fold)

- **Confusion matrices**

- **Feature importance analysis**

---

## 🛡️ Ethical Framework

### Core Principles

1. **Prevention, Not Punishment** - Focus on community care, not surveillance

1. **Transparency** - Open methodology and interpretable models

1. **Community Benefit** - Designed for CVI organizations, not law enforcement

1. **Bias Awareness** - Acknowledge and document data limitations

1. **Privacy Protection** - No individual-level data or predictions

### Implementation Safeguards

✅ Neighborhood-level aggregation only (minimum population: 500)✅ No individual identifiers in datasets✅ Explicit rejection of predictive policing applications✅ Clear documentation of intended use cases✅ Regular bias audits and model fairness assessments

---

## 📈 Example Usage

### Fetch Crime Data for Chicago

```python
from src.data_collection.crime_data import CrimeDataCollector
from src.utils.config import get_city_config

# Load city configuration
city_config = get_city_config('chicago')

# Initialize collector
collector = CrimeDataCollector(city_config)

# Fetch data
crime_df = collector.fetch_crime_data(
    start_date='2023-01-01',
    end_date='2024-01-01'
)

# Save to CSV
collector.save_to_csv(crime_df, 'data/raw/chicago_crime_2023.csv')
```

### Train Risk Prediction Model

```python
from src.modeling.risk_models import RandomForestRiskModel
from src.utils.config import MODEL_CONFIG

# Prepare data (assumes features_df is already created)
X = features_df[feature_columns]
y = features_df['high_risk']

# Initialize model
model = RandomForestRiskModel(MODEL_CONFIG['models']['random_forest'])

# Train
X_train, X_test, y_train, y_test = model.train_test_split_data(X, y)
model.train(X_train, y_train)

# Evaluate
predictions, probabilities = model.predict(X_test)
metrics = model.evaluate_model(y_test, predictions, probabilities)

print(f"Accuracy: {metrics['accuracy']:.3f}")
print(f"F1-Score: {metrics['f1_score']:.3f}")

# Save model
model.save_model('models/trained_models/rf_model.pkl')
```

### Generate Risk Map

```python
from src.visualization.risk_maps import create_risk_map

# Create interactive map
risk_map = create_risk_map(
    predictions_df=predictions,
    boundaries_gdf=boundaries,
    output_path='outputs/chicago_risk_map.html'
)
```

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=src tests/
```

---

## 📚 Documentation

- [**Methodology**](docs/METHODOLOGY.md) - Detailed technical methodology

- [**Ethical Framework**](docs/ETHICAL_FRAMEWORK.md) - Ethical guidelines and safeguards

- [**User Guide**](docs/USER_GUIDE.md) - Step-by-step instructions for CVI organizations

- [**API Documentation**](docs/API_DOCUMENTATION.md) - API reference for developers

- [**Data Sources**](data/DATA_SOURCES.md) - Complete data source documentation

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository

1. Create a feature branch (`git checkout -b feature/amazing-feature`)

1. Commit your changes (`git commit -m 'Add amazing feature'`)

1. Push to the branch (`git push origin feature/amazing-feature`)

1. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Barbara D. Gaskins**Founder & Lead Researcher, ETV Institute | Center for Decision ScienceData Science Graduate Student | Criminal Justice Reform Advocate

- 📧 Email: [bdgaskins27889@gmail.com](mailto:bdgaskins27889@gmail.com)

- 💼 LinkedIn: [linkedin.com/in/barbara-gaskins](https://linkedin.com/in/barbara-gaskins)

- 🐙 GitHub: [github.com/bdgaskins27889](https://github.com/bdgaskins27889)

- 🌐 ORCID: [0009-0007-9915-944X](https://orcid.org/0009-0007-9915-944X)

---

## 🙏 Acknowledgments

- **End The Violence (ETV)** - Founded by Dr. Sean Stevenson

- **City of Chicago** - Open data portal and crime statistics

- **US Census Bureau** - American Community Survey data

- **CDC/ATSDR** - Social Vulnerability Index

- **Community Violence Intervention Organizations** - Inspiration and real-world insights

---

## 📖 Citation

If you use this tool in your research or practice, please cite:

```
@software{gaskins2026cvi_predictor,
  author = {Gaskins, Barbara D.},
  title = {CVI Risk Predictor: Neighborhood Violence Risk Assessment Tool},
  year = {2026},
  url = {https://github.com/bdgaskins27889/COMMUNITY-VIOLENCE-INTERVENTION-PREDICTIVE-MODEL},
  doi = {10.5281/zenodo.21271446}
}
```

---

## ⚠️ Disclaimer

This tool is provided for educational and violence prevention purposes only. Predictions are based on historical data and should be used as one input among many in decision-making processes. The tool does not guarantee prevention of violence and should be combined with community knowledge, lived experience, and professional judgment. Users are responsible for ensuring ethical and appropriate use of this tool.

---

## 📞 Support

For questions, issues, or collaboration inquiries:

- **Open an issue** on GitHub

- **Email**: [bdgaskins27889@gmail.com](mailto:bdgaskins27889@gmail.com)

- **Documentation**: See [docs/](docs/) folder

---

**Built with ❤️ for Community Violence Intervention**

## 🏗️ Architecture

```
cvi-risk-predictor/
├── data/                          # Data storage
│   ├── raw/                       # Raw data downloads
│   ├── processed/                 # Cleaned and processed data
│   └── boundaries/                # Geographic boundary files
├── src/                           # Source code
│   ├── data_collection/           # API data fetchers
│   ├── preprocessing/             # Data cleaning and feature engineering
│   ├── modeling/                  # Machine learning models
│   ├── visualization/             # Plotting and mapping
│   └── utils/                     # Configuration and helpers
├── models/                        # Trained model files
├── notebooks/                     # Jupyter notebooks for analysis
├── app/                           # Web application
│   ├── app.py                     # Flask application
│   ├── templates/                 # HTML templates
│   └── static/                    # CSS, JS, images
├── tests/                         # Unit tests
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager
- (Optional) Census API key - [Get free key here](https://api.census.gov/data/key_signup.html)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cvi-risk-predictor.git
cd cvi-risk-predictor
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (optional)
```bash
# Create .env file
echo "CENSUS_API_KEY=your_key_here" > .env
echo "SOCRATA_APP_TOKEN=your_token_here" >> .env
```

### Running the Application

#### Option 1: Web Dashboard
```bash
cd app
python app.py
```
Then open your browser to `http://localhost:5000`

#### Option 2: Command Line Analysis
```bash
python -m src.data_collection.crime_data --city chicago --start-date 2023-01-01 --end-date 2024-01-01
```

#### Option 3: Jupyter Notebooks
```bash
jupyter notebook notebooks/
```

---

## 📊 Data Sources

All data sources are **publicly available** and **verifiable**:

### Crime Data
- **Chicago**: [Chicago Data Portal](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)
- **New York**: [NYC Open Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date/5uac-w243)
- **Los Angeles**: [LA Open Data](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8)
- **Philadelphia**: [OpenDataPhilly](https://opendataphilly.org/datasets/crime-incidents/)

### Socioeconomic Data
- **US Census Bureau**: [American Community Survey (ACS)](https://www.census.gov/data/developers/data-sets/acs-5year.html)
- **CDC**: [Social Vulnerability Index (SVI)](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html)

### Environmental Data
- **OpenStreetMap**: [Overpass API](https://overpass-api.de/)
- **City Open Data Portals**: Abandoned buildings, infrastructure

---

## 🤖 Methodology

### Feature Engineering

**Temporal Features:**
- Weekly crime counts and trends
- Seasonal patterns
- Day-of-week distributions

**Spatial Features:**
- Neighborhood-level aggregation
- Spatial density calculations
- Geographic clustering

**Socioeconomic Features:**
- Median household income
- Unemployment rate
- Poverty rate
- Educational attainment

**Vulnerability Features:**
- CDC Social Vulnerability Index (overall and by theme)
- Housing vacancy rates
- Environmental disorder indicators

### Machine Learning Models

#### 1. Logistic Regression
- **Purpose**: Interpretable baseline model
- **Advantages**: Transparent coefficients, fast training
- **Use Case**: Understanding key risk factors

#### 2. Random Forest Classifier
- **Purpose**: Capture complex non-linear patterns
- **Advantages**: High accuracy, feature importance
- **Use Case**: Operational predictions

#### 3. K-Means Clustering
- **Purpose**: Group neighborhoods into risk tiers
- **Advantages**: Unsupervised, intuitive groupings
- **Use Case**: Resource allocation prioritization

### Model Evaluation

- **Accuracy, Precision, Recall, F1-Score**
- **Cross-validation** (5-fold)
- **Confusion matrices**
- **Feature importance analysis**

---

## 🛡️ Ethical Framework

### Core Principles

1. **Prevention, Not Punishment** - Focus on community care, not surveillance
2. **Transparency** - Open methodology and interpretable models
3. **Community Benefit** - Designed for CVI organizations, not law enforcement
4. **Bias Awareness** - Acknowledge and document data limitations
5. **Privacy Protection** - No individual-level data or predictions

### Implementation Safeguards

✅ Neighborhood-level aggregation only (minimum population: 500)  
✅ No individual identifiers in datasets  
✅ Explicit rejection of predictive policing applications  
✅ Clear documentation of intended use cases  
✅ Regular bias audits and model fairness assessments  

---

## 📈 Example Usage

### Fetch Crime Data for Chicago
```python
from src.data_collection.crime_data import CrimeDataCollector
from src.utils.config import get_city_config

# Load city configuration
city_config = get_city_config('chicago')

# Initialize collector
collector = CrimeDataCollector(city_config)

# Fetch data
crime_df = collector.fetch_crime_data(
    start_date='2023-01-01',
    end_date='2024-01-01'
)

# Save to CSV
collector.save_to_csv(crime_df, 'data/raw/chicago_crime_2023.csv')
```

### Train Risk Prediction Model
```python
from src.modeling.risk_models import RandomForestRiskModel
from src.utils.config import MODEL_CONFIG

# Prepare data (assumes features_df is already created)
X = features_df[feature_columns]
y = features_df['high_risk']

# Initialize model
model = RandomForestRiskModel(MODEL_CONFIG['models']['random_forest'])

# Train
X_train, X_test, y_train, y_test = model.train_test_split_data(X, y)
model.train(X_train, y_train)

# Evaluate
predictions, probabilities = model.predict(X_test)
metrics = model.evaluate_model(y_test, predictions, probabilities)

print(f"Accuracy: {metrics['accuracy']:.3f}")
print(f"F1-Score: {metrics['f1_score']:.3f}")

# Save model
model.save_model('models/trained_models/rf_model.pkl')
```

### Generate Risk Map
```python
from src.visualization.risk_maps import create_risk_map

# Create interactive map
risk_map = create_risk_map(
    predictions_df=predictions,
    boundaries_gdf=boundaries,
    output_path='outputs/chicago_risk_map.html'
)
```

---

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=src tests/
```

---

## 📚 Documentation

- **[Methodology](docs/METHODOLOGY.md)** - Detailed technical methodology
- **[Ethical Framework](docs/ETHICAL_FRAMEWORK.md)** - Ethical guidelines and safeguards
- **[User Guide](docs/USER_GUIDE.md)** - Step-by-step instructions for CVI organizations
- **[API Documentation](docs/API_DOCUMENTATION.md)** - API reference for developers
- **[Data Sources](data/DATA_SOURCES.md)** - Complete data source documentation

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Barbara D. Gaskins**  
Data Science Graduate Student | Criminal Justice Reform Advocate | AI & Justice Researcher

- 📧 Email: bdgaskins27889@gmail.com
- 📱 Phone: 252.495.3173
- 💼 LinkedIn: [linkedin.com/in/barbara-gaskins](https://linkedin.com/in/barbara-gaskins)
- 🐙 GitHub: [github.com/yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **City of Chicago** - Open data portal and crime statistics
- **US Census Bureau** - American Community Survey data
- **CDC/ATSDR** - Social Vulnerability Index
- **Community Violence Intervention Organizations** - Inspiration and real-world insights
- **Bellevue University** - Academic support and guidance

---

## 📖 Citation

If you use this tool in your research or practice, please cite:

```bibtex
@software{gaskins2026cvi,
  author = {Gaskins, Barbara D.},
  title = {CVI Risk Predictor: Neighborhood Violence Risk Assessment Tool},
  year = {2026},
  url = {https://github.com/yourusername/cvi-risk-predictor}
}
```

---

## ⚠️ Disclaimer

This tool is provided for educational and violence prevention purposes only. Predictions are based on historical data and should be used as one input among many in decision-making processes. The tool does not guarantee prevention of violence and should be combined with community knowledge, lived experience, and professional judgment. Users are responsible for ensuring ethical and appropriate use of this tool.

---

## 📞 Support

For questions, issues, or collaboration inquiries:

- **Open an issue** on GitHub
- **Email**: bdgaskins27889@gmail.com
- **Documentation**: See [docs/](docs/) folder

---

**Built with ❤️ for Community Violence Intervention**
