# CVI Risk Predictor: Technical Methodology

**Author:** Barbara D. Gaskins  
**Last Updated:** January 23, 2026

---

## 1. Introduction

This document provides a detailed technical overview of the methodology employed in the **CVI Risk Predictor**, a tool designed to support proactive Community Violence Intervention (CVI) efforts. The framework integrates publicly available data to generate neighborhood-level violence risk assessments, enabling CVI organizations to allocate resources more effectively. The methodology prioritizes transparency, replicability, and ethical application, explicitly rejecting individual-level prediction and surveillance-based approaches.

Our approach is grounded in the public health model of violence prevention, which treats violence as a preventable epidemic. By identifying the environmental and social determinants of violence at a community level, we can support interventions that address root causes rather than merely reacting to incidents. This place-based predictive modeling framework is designed to be a decision-support tool, augmenting the invaluable on-the-ground expertise of CVI practitioners.

---

## 2. Data Acquisition and Integration

The model relies on a diverse set of publicly available and verifiable data sources, which are integrated to create a holistic view of neighborhood-level risk factors. The data pipeline is designed to be adaptable to multiple cities, with an initial focus on Chicago.

### 2.1. Core Data Sources

The primary data categories and their sources are outlined below.

| Data Category             | Source                                      | Description                                                                 | Update Frequency |
| ------------------------- | ------------------------------------------- | --------------------------------------------------------------------------- | ---------------- |
| **Crime Incidents**       | City Open Data Portals (e.g., Chicago [1])  | Reported violent crime incidents (homicide, assault, robbery, etc.)         | Daily            |
| **Gunfire Alerts**        | ShotSpotter Data (via Data Portals [2])     | Acoustic gunshot detection system alerts                                    | Daily            |
| **Socioeconomic Data**    | U.S. Census Bureau (ACS 5-Year [3])         | Demographics, income, poverty, unemployment, education at the census tract level | Annually         |
| **Social Vulnerability**  | CDC Social Vulnerability Index (SVI [4])    | Measures of community resilience to external stressors                      | Every 2 years    |
| **Environmental Disorder**| City Open Data Portals (e.g., Chicago [5])  | 311 service requests for vacant/abandoned buildings                         | Daily            |
| **Infrastructure**        | OpenStreetMap (OSM [6])                     | Locations of schools, parks, transit stops, and other public amenities      | Continuously     |

### 2.2. Data Collection Process

Data is collected through automated scripts that interact with public APIs. The `sodapy` library is used to access Socrata-powered open data portals, while the Census Data API is queried for ACS data. Geographic boundary files (e.g., neighborhood or community area shapefiles) are downloaded directly from city data portals or the U.S. Census Bureau.

> **Note on Data Lag:** Most real-time data sources, such as crime incident reports, have a built-in lag (typically 7 days) for verification and privacy purposes. Our model accounts for this lag in its forecasting.

---

## 3. Feature Engineering

Raw data is transformed into a rich set of features aggregated at the **neighborhood-week** level. This spatio-temporal unit of analysis is granular enough to be actionable for CVI teams while adhering to our ethical commitment to avoid individual-level analysis.

### 3.1. Spatial Aggregation

All point-level data (crime incidents, ShotSpotter alerts, abandoned buildings) are spatially joined to neighborhood boundaries. This process involves:

1.  Converting latitude/longitude coordinates into `shapely` Point objects.
2.  Using `geopandas` to perform a spatial join (`sjoin`) with the neighborhood boundary GeoDataFrame.
3.  Aggregating the points within each neighborhood to generate counts and densities.

### 3.2. Temporal Aggregation

Data is aggregated into weekly time periods. This allows the model to capture short-term trends and fluctuations in risk. Key temporal features include:

-   **Lagged Variables:** Crime counts from previous weeks (e.g., 1, 2, 4, and 12 weeks prior).
-   **Rolling Averages:** Moving averages of crime counts over different time windows (e.g., 4-week and 12-week averages) to smooth out noise.
-   **Trend Features:** The slope of a linear regression fitted to crime counts over the past 12 weeks to capture increasing or decreasing trends.

### 3.3. Feature Categories

The engineered features are grouped into several categories:

| Feature Category           | Example Features                                                                    |
| -------------------------- | ----------------------------------------------------------------------------------- |
| **Crime & Violence**       | `violent_crime_count_lag_1w`, `crime_trend_12w`, `shotspotter_alert_density`        |
| **Environmental Disorder** | `abandoned_building_count`, `311_sanitation_requests_rate`                          |
| **Socioeconomic Status**   | `median_household_income`, `unemployment_rate`, `poverty_rate`                      |
| **Social Vulnerability**   | `svi_overall_score`, `svi_socioeconomic_theme`                                      |
| **Demographics**           | `population_density`, `percent_under_25`                                            |
| **Infrastructure**         | `park_density`, `distance_to_nearest_hospital`                                      |

---

## 4. Predictive Modeling

We employ a suite of machine learning models to provide a comprehensive risk assessment. This multi-model approach balances interpretability with predictive power.

### 4.1. Target Variable Definition

The primary target variable is a binary indicator of a **high-risk week** for a given neighborhood. A neighborhood-week is classified as high-risk if its violent crime count exceeds the **75th percentile** of all neighborhood-week crime counts in the training dataset. This percentile-based thresholding makes the model robust to overall increases or decreases in crime and focuses on identifying periods of unusually high activity relative to the norm.

### 4.2. Model Suite

1.  **Logistic Regression:** This model serves as an interpretable baseline. The coefficients of the logistic regression model provide clear insights into the direction and magnitude of the relationship between each feature and the likelihood of a high-risk week. This is crucial for explaining *why* a neighborhood is flagged as high-risk.

2.  **Random Forest Classifier:** This ensemble model is used for its high predictive accuracy and ability to capture complex, non-linear interactions between features. While less directly interpretable than logistic regression, the Random Forest model provides a robust measure of **feature importance**, which helps identify the key drivers of risk in a given prediction.

3.  **K-Means Clustering:** This unsupervised learning model is used to group neighborhoods into distinct **risk tiers** (e.g., Low, Moderate, High, Critical) based on their long-term feature profiles. This provides a strategic, high-level overview of the city's risk landscape, which is useful for long-term resource allocation and planning.

### 4.3. Model Training and Evaluation

The models are trained on historical data, typically a rolling 2-3 year period. The dataset is split into a training set (80%) and a testing set (20%) for evaluation. We use a time-based split to ensure the model is tested on its ability to predict future events.

Model performance is assessed using a standard set of classification metrics:

-   **Accuracy:** Overall correctness of predictions.
-   **Precision:** The proportion of predicted high-risk weeks that were actually high-risk. (Minimizes false positives).
-   **Recall:** The proportion of actual high-risk weeks that were correctly identified. (Minimizes false negatives).
-   **F1-Score:** The harmonic mean of precision and recall, providing a balanced measure.
-   **ROC-AUC:** The area under the ROC curve, measuring the model's ability to distinguish between classes.

All models undergo 5-fold cross-validation to ensure their performance is stable and generalizable.

---

## 5. Ethical Safeguards and Limitations

Methodological choices are guided by a strict ethical framework to prevent misuse.

-   **Aggregation:** All analysis is conducted at the neighborhood level, with a minimum population threshold, to prevent individual identification.
-   **Transparency:** The use of interpretable models (Logistic Regression) and feature importance analysis ensures that predictions can be explained.
-   **Bias Acknowledgment:** We explicitly acknowledge that crime data is a reflection of reporting and enforcement patterns, not a perfect measure of all criminal activity. The model's documentation highlights these potential biases.

**Limitations:** The model's accuracy is dependent on the quality and availability of public data. It cannot predict specific incidents or account for the complex human factors that are the domain of CVI professionals. It is a tool to augment, not replace, human expertise.

---

## 6. References

[1] City of Chicago. (2023). *Crimes - 2001 to Present*. Chicago Data Portal. [https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)

[2] City of Chicago. (2023). *Violence Reduction - Shotspotter Alerts*. Chicago Data Portal. [https://data.cityofchicago.org/Public-Safety/Violence-Reduction-Shotspotter-Alerts/3h7q-7mdb](https://data.cityofchicago.org/Public-Safety/Violence-Reduction-Shotspotter-Alerts/3h7q-7mdb)

[3] U.S. Census Bureau. (2022). *American Community Survey (ACS)*. [https://www.census.gov/programs-surveys/acs](https://www.census.gov/programs-surveys/acs)

[4] Centers for Disease Control and Prevention/ATSDR. (2022). *CDC/ATSDR Social Vulnerability Index (SVI)*. [https://www.atsdr.cdc.gov/placeandhealth/svi/index.html](https://www.atsdr.cdc.gov/placeandhealth/svi/index.html)

[5] City of Chicago. (2023). *311 Service Requests – Vacant and Abandoned Buildings*. Chicago Data Portal. [https://data.cityofchicago.org/Service-Requests/311-Service-Requests-Vacant-and-Abandoned-Buildin/7nii-7srd](https://data.cityofchicago.org/Service-Requests/311-Service-Requests-Vacant-and-Abandoned-Buildin/7nii-7srd)

[6] OpenStreetMap Foundation. (2023). *OpenStreetMap*. [https://www.openstreetmap.org](https://www.openstreetmap.org)
