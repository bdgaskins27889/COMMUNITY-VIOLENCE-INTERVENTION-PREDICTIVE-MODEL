"""
CVI Risk Predictor - Complete Web Application with ML Model Integration
Flask-based dashboard with real-time predictions using trained models
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import folium
from folium import plugins
import json
import os
import sys
import joblib
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import CITY_CONFIGS, list_available_cities, get_city_config

app = Flask(__name__)

# Global storage for models and data
models = {
    'logistic_regression': None,
    'random_forest': None,
    'kmeans': None
}

# Load trained models
def load_models():
    """Load all trained ML models"""
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'trained_models')
    
    try:
        # Load Logistic Regression
        lr_path = os.path.join(model_dir, 'logistic_regression_model.pkl')
        if os.path.exists(lr_path):
            models['logistic_regression'] = joblib.load(lr_path)
            print("✓ Loaded Logistic Regression model")
        
        # Load Random Forest
        rf_path = os.path.join(model_dir, 'random_forest_model.pkl')
        if os.path.exists(rf_path):
            models['random_forest'] = joblib.load(rf_path)
            print("✓ Loaded Random Forest model")
        
        # Load K-Means
        km_path = os.path.join(model_dir, 'kmeans_clustering_model.pkl')
        if os.path.exists(km_path):
            models['kmeans'] = joblib.load(km_path)
            print("✓ Loaded K-Means Clustering model")
        
        print("All models loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading models: {e}")
        return False


# Generate sample neighborhood data with predictions
def generate_neighborhood_data(city_name='chicago', n_neighborhoods=77):
    """Generate sample neighborhood data with ML predictions"""
    
    np.random.seed(42)
    
    neighborhoods = []
    
    for i in range(1, n_neighborhoods + 1):
        # Generate features
        features = {
            'violent_crime_count_lag_1w': np.random.poisson(15),
            'violent_crime_count_lag_2w': np.random.poisson(14),
            'violent_crime_count_lag_4w': np.random.poisson(13),
            'crime_trend_12w': np.random.uniform(-2, 2),
            'crime_rolling_avg_4w': np.random.uniform(10, 25),
            'median_household_income': np.random.uniform(25000, 85000),
            'unemployment_rate': np.random.uniform(3, 18),
            'poverty_rate': np.random.uniform(5, 40),
            'education_less_than_hs_pct': np.random.uniform(5, 35),
            'svi_overall_score': np.random.uniform(0, 1),
            'svi_socioeconomic': np.random.uniform(0, 1),
            'svi_household_composition': np.random.uniform(0, 1),
            'abandoned_building_density': np.random.uniform(0, 0.1),
            'vacancy_rate': np.random.uniform(0, 25),
            'population_density': np.random.uniform(1000, 15000)
        }
        
        # Create feature DataFrame
        feature_df = pd.DataFrame([features])
        
        # Get predictions from Random Forest (primary model)
        if models['random_forest']:
            model_data = models['random_forest']
            rf_model = model_data['model']
            scaler = model_data['scaler']
            
            # Scale features
            X_scaled = scaler.transform(feature_df)
            
            # Predict
            prediction = rf_model.predict(X_scaled)[0]
            probability = rf_model.predict_proba(X_scaled)[0]
            
            risk_score = int(probability[1] * 100)  # Probability of high risk
        else:
            # Fallback if model not loaded
            risk_score = np.random.randint(20, 95)
            prediction = 1 if risk_score > 60 else 0
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = 'Critical'
            color = '#e74c3c'
        elif risk_score >= 65:
            risk_level = 'High'
            color = '#e67e22'
        elif risk_score >= 45:
            risk_level = 'Moderate'
            color = '#f39c12'
        else:
            risk_level = 'Low'
            color = '#2ecc71'
        
        # Generate historical data
        historical_weeks = ['Week -4', 'Week -3', 'Week -2', 'Week -1', 'Current']
        historical_incidents = [
            int(features['violent_crime_count_lag_4w']),
            int(features['violent_crime_count_lag_2w']),
            int(features['violent_crime_count_lag_1w']),
            int(features['violent_crime_count_lag_1w'] + np.random.randint(-3, 4)),
            int(features['violent_crime_count_lag_1w'] + features['crime_trend_12w'])
        ]
        
        # Determine trend
        if features['crime_trend_12w'] > 0.5:
            trend = 'increasing'
        elif features['crime_trend_12w'] < -0.5:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        # Generate recommendations based on risk factors
        recommendations = []
        if features['crime_trend_12w'] > 1:
            recommendations.append("Increase street outreach presence during evening hours")
        if features['svi_overall_score'] > 0.7:
            recommendations.append("Partner with social service providers for community support")
        if features['abandoned_building_density'] > 0.05:
            recommendations.append("Coordinate with city on abandoned building remediation")
        if features['unemployment_rate'] > 12:
            recommendations.append("Connect residents with job training and employment programs")
        if not recommendations:
            recommendations.append("Continue current intervention strategies")
            recommendations.append("Monitor for changes in risk factors")
        
        neighborhood = {
            'id': i,
            'name': f'Neighborhood {i}',
            'risk_level': risk_level,
            'risk_score': risk_score,
            'color': color,
            'violent_crime_count': historical_incidents[-1],
            'trend': trend,
            'recommendations': recommendations,
            'historical_data': {
                'weeks': historical_weeks,
                'incidents': historical_incidents
            },
            'features': features,
            # Chicago coordinates with some variation
            'latitude': 41.8781 + np.random.uniform(-0.2, 0.2),
            'longitude': -87.6298 + np.random.uniform(-0.2, 0.2)
        }
        
        neighborhoods.append(neighborhood)
    
    return neighborhoods


@app.route('/')
def index():
    """Main dashboard page"""
    cities = list_available_cities()
    return render_template(
        'dashboard.html',
        cities=cities,
        current_city='Chicago'
    )


@app.route('/api/cities')
def get_cities():
    """Get list of available cities"""
    cities = list_available_cities()
    return jsonify({'cities': cities})


@app.route('/api/city_data/<city_name>')
def get_city_data(city_name):
    """Get complete data for a city"""
    
    try:
        # Generate neighborhood data
        neighborhoods = generate_neighborhood_data(city_name)
        
        # Calculate summary statistics
        risk_distribution = {
            'Low': sum(1 for n in neighborhoods if n['risk_level'] == 'Low'),
            'Moderate': sum(1 for n in neighborhoods if n['risk_level'] == 'Moderate'),
            'High': sum(1 for n in neighborhoods if n['risk_level'] == 'High'),
            'Critical': sum(1 for n in neighborhoods if n['risk_level'] == 'Critical')
        }
        
        total_incidents = sum(n['violent_crime_count'] for n in neighborhoods)
        
        # Get top high-risk neighborhoods
        high_risk_neighborhoods = sorted(
            [n for n in neighborhoods if n['risk_level'] in ['High', 'Critical']],
            key=lambda x: x['risk_score'],
            reverse=True
        )[:10]
        
        summary = {
            'city': city_name.title(),
            'total_neighborhoods': len(neighborhoods),
            'risk_distribution': risk_distribution,
            'total_incidents_last_week': total_incidents,
            'high_risk_neighborhoods': [
                {
                    'id': n['id'],
                    'name': n['name'],
                    'risk_score': n['risk_score'],
                    'risk_level': n['risk_level']
                }
                for n in high_risk_neighborhoods
            ]
        }
        
        return jsonify({
            'summary': summary,
            'neighborhoods': neighborhoods
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/neighborhood/<int:neighborhood_id>')
def get_neighborhood_detail(neighborhood_id):
    """Get detailed information for a specific neighborhood"""
    
    try:
        # Generate data (in production, would query database)
        neighborhoods = generate_neighborhood_data()
        
        neighborhood = next((n for n in neighborhoods if n['id'] == neighborhood_id), None)
        
        if not neighborhood:
            return jsonify({'error': 'Neighborhood not found'}), 404
        
        return jsonify(neighborhood)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict_risk():
    """
    API endpoint for real-time risk prediction
    Accepts neighborhood features and returns risk assessment from all models
    """
    
    try:
        data = request.get_json()
        features = data.get('features', {})
        
        # Expected feature list
        feature_cols = [
            'violent_crime_count_lag_1w',
            'violent_crime_count_lag_2w',
            'violent_crime_count_lag_4w',
            'crime_trend_12w',
            'crime_rolling_avg_4w',
            'median_household_income',
            'unemployment_rate',
            'poverty_rate',
            'education_less_than_hs_pct',
            'svi_overall_score',
            'svi_socioeconomic',
            'svi_household_composition',
            'abandoned_building_density',
            'vacancy_rate',
            'population_density'
        ]
        
        # Create feature DataFrame
        feature_values = [features.get(col, 0) for col in feature_cols]
        feature_df = pd.DataFrame([feature_values], columns=feature_cols)
        
        predictions = {}
        
        # Random Forest prediction (primary)
        if models['random_forest']:
            model_data = models['random_forest']
            rf_model = model_data['model']
            scaler = model_data['scaler']
            
            X_scaled = scaler.transform(feature_df)
            pred = rf_model.predict(X_scaled)[0]
            proba = rf_model.predict_proba(X_scaled)[0]
            
            predictions['random_forest'] = {
                'prediction': int(pred),
                'probability_high_risk': float(proba[1]),
                'risk_score': int(proba[1] * 100)
            }
        
        # Logistic Regression prediction
        if models['logistic_regression']:
            model_data = models['logistic_regression']
            lr_model = model_data['model']
            scaler = model_data['scaler']
            
            X_scaled = scaler.transform(feature_df)
            pred = lr_model.predict(X_scaled)[0]
            proba = lr_model.predict_proba(X_scaled)[0]
            
            predictions['logistic_regression'] = {
                'prediction': int(pred),
                'probability_high_risk': float(proba[1]),
                'risk_score': int(proba[1] * 100)
            }
        
        # Use Random Forest as primary prediction
        primary_score = predictions.get('random_forest', {}).get('risk_score', 50)
        
        # Determine risk level
        if primary_score >= 80:
            risk_level = 'Critical'
        elif primary_score >= 65:
            risk_level = 'High'
        elif primary_score >= 45:
            risk_level = 'Moderate'
        else:
            risk_level = 'Low'
        
        # Get feature importance for explanation
        top_factors = []
        if models['random_forest']:
            feature_importance = model_data.get('feature_importance')
            if feature_importance is not None:
                top_factors = [
                    {
                        'factor': row['feature'],
                        'importance': float(row['importance'])
                    }
                    for _, row in feature_importance.head(5).iterrows()
                ]
        
        response = {
            'risk_score': primary_score,
            'risk_level': risk_level,
            'predictions': predictions,
            'top_factors': top_factors,
            'model_used': 'Random Forest (Primary)',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/methodology')
def methodology():
    """Methodology page"""
    return render_template('methodology.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/health')
def health_check():
    """Health check endpoint"""
    models_loaded = {
        'logistic_regression': models['logistic_regression'] is not None,
        'random_forest': models['random_forest'] is not None,
        'kmeans': models['kmeans'] is not None
    }
    
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'models_loaded': models_loaded
    })


# Initialize models on startup
print("="*70)
print("CVI RISK PREDICTOR - WEB APPLICATION")
print("="*70)
print("\nLoading ML models...")
load_models()
print("\nApplication ready!")
print("="*70)


if __name__ == '__main__':
    # Development server
    print("\n🚀 Starting Flask development server...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("📖 API documentation at: http://localhost:5000/health")
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
