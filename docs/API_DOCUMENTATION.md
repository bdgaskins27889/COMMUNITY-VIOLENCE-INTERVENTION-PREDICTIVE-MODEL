_# CVI Risk Predictor: API Documentation

**Version:** 1.0.0  
**Last Updated:** January 23, 2026

---

## 1. Introduction

This document provides technical documentation for the API endpoints exposed by the CVI Risk Predictor web application. The API allows for programmatic interaction with the risk assessment tool, enabling integration with other systems or custom analyses.

The API is built using Flask and follows RESTful principles. All responses are in JSON format.

---

## 2. Base URL

The API is served from the same host as the web application. When running locally, the base URL is:

`http://localhost:5000/api`

---

## 3. Authentication

Currently, the API is open and does not require authentication. In a production environment, API keys would be implemented to manage access and rate limiting.

---

## 4. API Endpoints

### 4.1. City Information

#### `GET /api/cities`

Returns a list of all cities configured in the application.

-   **Method:** `GET`
-   **Success Response (200):**
    ```json
    {
      "cities": [
        "Chicago",
        "New York",
        "Los Angeles",
        "Philadelphia"
      ]
    }
    ```

### 4.2. Risk Assessment

#### `GET /api/risk_map/<city_name>`

Generates and returns the HTML for an interactive risk map for the specified city.

-   **Method:** `GET`
-   **URL Parameters:**
    -   `city_name` (string, required): The name of the city (e.g., `chicago`).
-   **Success Response (200):**
    ```json
    {
      "map_html": "<div id=\"map\">...</div>",
      "city": "Chicago"
    }
    ```
-   **Error Response (404):**
    ```json
    {
      "error": "City not found"
    }
    ```

#### `GET /api/city_summary/<city_name>`

Provides a summary of the risk assessment for the entire city.

-   **Method:** `GET`
-   **URL Parameters:**
    -   `city_name` (string, required): The name of the city.
-   **Success Response (200):**
    ```json
    {
      "city": "Chicago",
      "total_neighborhoods": 77,
      "risk_distribution": {
        "Low": 25,
        "Moderate": 30,
        "High": 15,
        "Critical": 7
      },
      "total_incidents_last_week": 234,
      "trend": "stable",
      "high_risk_neighborhoods": [
        {"id": 1, "name": "West Englewood", "risk_score": 92},
        {"id": 2, "name": "Austin", "risk_score": 88}
      ]
    }
    ```

#### `GET /api/neighborhood_stats/<city_name>/<neighborhood_id>`

Returns detailed statistics for a single neighborhood.

-   **Method:** `GET`
-   **URL Parameters:**
    -   `city_name` (string, required): The name of the city.
    -   `neighborhood_id` (string/integer, required): The unique identifier for the neighborhood.
-   **Success Response (200):**
    ```json
    {
      "neighborhood_id": "1",
      "neighborhood_name": "West Englewood",
      "risk_level": "Critical",
      "risk_score": 92,
      "violent_crime_count": 58,
      "trend": "increasing",
      "recommendations": [
        "Increase outreach presence during evening hours",
        "Focus on conflict mediation services"
      ],
      "historical_data": {
        "weeks": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "incidents": [45, 51, 48, 58]
      }
    }
    ```

### 4.3. Prediction Endpoint

#### `POST /api/predict`

Accepts a set of features for a neighborhood and returns a real-time risk prediction. This is an advanced endpoint for integration with other systems.

-   **Method:** `POST`
-   **Request Body (JSON):**
    ```json
    {
      "features": {
        "violent_crime_count_lag_1w": 50,
        "crime_trend_12w": 0.8,
        "svi_overall_score": 0.91,
        "abandoned_building_density": 0.05
      }
    }
    ```
-   **Success Response (200):**
    ```json
    {
      "risk_score": 92,
      "risk_level": "Critical",
      "confidence": 0.88,
      "top_factors": [
        {"factor": "Recent violent crime trend", "contribution": 0.41},
        {"factor": "Social vulnerability index", "contribution": 0.32}
      ]
    }
    ```
-   **Error Response (400):**
    ```json
    {
      "error": "Invalid input features"
    }
    ```

### 4.4. System Health

#### `GET /health`

A simple health check endpoint to verify that the application is running.

-   **Method:** `GET`
-   **Success Response (200):**
    ```json
    {
      "status": "healthy",
      "version": "1.0.0"
    }
    ```

---

## 5. Rate Limiting

In a production deployment, the following rate limits would be applied:

-   **Unauthenticated Users:** 60 requests per minute.
-   **Authenticated Users:** 300 requests per minute.

Responses for exceeded rate limits will have a `429 Too Many Requests` status code.

---

## 6. Example Usage (cURL)

**Get City Summary for Chicago:**
```bash
curl -X GET http://localhost:5000/api/city_summary/chicago
```

**Get Stats for a Neighborhood:**
```bash
curl -X GET http://localhost:5000/api/neighborhood_stats/chicago/25
```

**Make a Prediction:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"features": {"violent_crime_count_lag_1w": 50, "svi_overall_score": 0.9}}' \
http://localhost:5000/api/predict
```
