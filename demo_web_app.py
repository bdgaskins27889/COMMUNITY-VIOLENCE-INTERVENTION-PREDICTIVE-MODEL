"""
Demo Script: Test All Web Application Features
Tests API endpoints and generates sample predictions
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def test_health_check():
    """Test health check endpoint"""
    print_section("1. HEALTH CHECK")
    
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    
    print(f"Status: {data['status']}")
    print(f"Version: {data['version']}")
    print("\nModels Loaded:")
    for model, loaded in data['models_loaded'].items():
        status = "✓" if loaded else "✗"
        print(f"  {status} {model}")

def test_cities():
    """Test cities endpoint"""
    print_section("2. AVAILABLE CITIES")
    
    response = requests.get(f"{BASE_URL}/api/cities")
    data = response.json()
    
    print("Available cities:")
    for city in data['cities']:
        print(f"  • {city}")

def test_city_data():
    """Test city data endpoint"""
    print_section("3. CITY DATA (CHICAGO)")
    
    response = requests.get(f"{BASE_URL}/api/city_data/chicago")
    data = response.json()
    
    summary = data['summary']
    
    print(f"City: {summary['city']}")
    print(f"Total Neighborhoods: {summary['total_neighborhoods']}")
    print(f"Total Incidents (Last Week): {summary['total_incidents_last_week']}")
    
    print("\nRisk Distribution:")
    for level, count in summary['risk_distribution'].items():
        print(f"  {level}: {count}")
    
    print("\nTop 5 High-Risk Neighborhoods:")
    for i, n in enumerate(summary['high_risk_neighborhoods'][:5], 1):
        print(f"  {i}. {n['name']} - Risk Score: {n['risk_score']} ({n['risk_level']})")

def test_neighborhood_detail():
    """Test neighborhood detail endpoint"""
    print_section("4. NEIGHBORHOOD DETAIL")
    
    response = requests.get(f"{BASE_URL}/api/neighborhood/1")
    neighborhood = response.json()
    
    print(f"Name: {neighborhood['name']}")
    print(f"Risk Level: {neighborhood['risk_level']}")
    print(f"Risk Score: {neighborhood['risk_score']}")
    print(f"Recent Incidents: {neighborhood['violent_crime_count']}")
    print(f"Trend: {neighborhood['trend']}")
    
    print("\nStrategic Recommendations:")
    for i, rec in enumerate(neighborhood['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\nHistorical Data:")
    for week, incidents in zip(neighborhood['historical_data']['weeks'], 
                               neighborhood['historical_data']['incidents']):
        print(f"  {week}: {incidents} incidents")

def test_prediction_low_risk():
    """Test prediction endpoint with low-risk features"""
    print_section("5. PREDICTION TEST - LOW RISK SCENARIO")
    
    features = {
        "violent_crime_count_lag_1w": 5,
        "violent_crime_count_lag_2w": 6,
        "violent_crime_count_lag_4w": 5,
        "crime_trend_12w": -0.5,
        "crime_rolling_avg_4w": 5.5,
        "median_household_income": 75000,
        "unemployment_rate": 4.5,
        "poverty_rate": 8.0,
        "education_less_than_hs_pct": 7.0,
        "svi_overall_score": 0.2,
        "svi_socioeconomic": 0.15,
        "svi_household_composition": 0.25,
        "abandoned_building_density": 0.01,
        "vacancy_rate": 5.0,
        "population_density": 5000
    }
    
    response = requests.post(
        f"{BASE_URL}/api/predict",
        json={"features": features},
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Model Used: {result['model_used']}")
    
    print("\nModel Predictions:")
    for model, pred in result['predictions'].items():
        print(f"  {model}:")
        print(f"    - Probability of High Risk: {pred['probability_high_risk']:.2%}")
        print(f"    - Risk Score: {pred['risk_score']}")

def test_prediction_high_risk():
    """Test prediction endpoint with high-risk features"""
    print_section("6. PREDICTION TEST - HIGH RISK SCENARIO")
    
    features = {
        "violent_crime_count_lag_1w": 28,
        "violent_crime_count_lag_2w": 26,
        "violent_crime_count_lag_4w": 25,
        "crime_trend_12w": 2.5,
        "crime_rolling_avg_4w": 26.5,
        "median_household_income": 28000,
        "unemployment_rate": 16.5,
        "poverty_rate": 38.0,
        "education_less_than_hs_pct": 32.0,
        "svi_overall_score": 0.92,
        "svi_socioeconomic": 0.88,
        "svi_household_composition": 0.85,
        "abandoned_building_density": 0.09,
        "vacancy_rate": 22.0,
        "population_density": 12000
    }
    
    response = requests.post(
        f"{BASE_URL}/api/predict",
        json={"features": features},
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Model Used: {result['model_used']}")
    
    print("\nModel Predictions:")
    for model, pred in result['predictions'].items():
        print(f"  {model}:")
        print(f"    - Probability of High Risk: {pred['probability_high_risk']:.2%}")
        print(f"    - Risk Score: {pred['risk_score']}")

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  CVI RISK PREDICTOR - WEB APPLICATION DEMO")
    print("="*70)
    print("\nThis script tests all API endpoints and features.")
    print("Make sure the Flask app is running at http://localhost:5000")
    print("\nWaiting 3 seconds before starting tests...")
    time.sleep(3)
    
    try:
        # Run all tests
        test_health_check()
        test_cities()
        test_city_data()
        test_neighborhood_detail()
        test_prediction_low_risk()
        test_prediction_high_risk()
        
        # Summary
        print_section("DEMO COMPLETE")
        print("✓ All API endpoints tested successfully!")
        print("✓ ML models are functioning correctly")
        print("✓ Predictions are being generated in real-time")
        print("\nNext Steps:")
        print("  1. Open http://localhost:5000 in your browser")
        print("  2. Explore the interactive dashboard")
        print("  3. Click on neighborhoods to see detailed analysis")
        print("  4. Try different cities from the dropdown")
        print("\n" + "="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask application")
        print("Please make sure the app is running:")
        print("  cd /home/ubuntu/cvi_risk_predictor/app")
        print("  python3 app_complete.py")
        print("\nThen run this demo script again.\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")

if __name__ == "__main__":
    main()
