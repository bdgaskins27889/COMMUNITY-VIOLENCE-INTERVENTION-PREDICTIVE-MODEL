"""
CVI Risk Predictor Web Application
Flask-based dashboard for neighborhood violence risk assessment
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.config import CITY_CONFIGS, list_available_cities

app = Flask(__name__)

# Global data storage (in production, use database)
app_data = {
    'current_city': 'chicago',
    'risk_predictions': None,
    'boundaries': None,
    'crime_data': None
}


@app.route('/')
def index():
    """Main dashboard page"""
    cities = list_available_cities()
    return render_template(
        'index.html',
        cities=cities,
        current_city=app_data['current_city']
    )


@app.route('/api/cities')
def get_cities():
    """Get list of available cities"""
    cities = list_available_cities()
    return jsonify({'cities': cities})


@app.route('/api/risk_map/<city_name>')
def get_risk_map(city_name):
    """Generate risk map for specified city"""
    
    try:
        # Load city data (placeholder - in production, load from database)
        city_config = CITY_CONFIGS.get(city_name.lower().replace(' ', '_'))
        
        if not city_config:
            return jsonify({'error': 'City not found'}), 404
        
        # Create base map
        m = folium.Map(
            location=[41.8781, -87.6298] if city_name == 'chicago' else [40.7128, -74.0060],
            zoom_start=11,
            tiles='OpenStreetMap'
        )
        
        # Add sample data (in production, use real predictions)
        sample_data = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {
                        'name': 'Sample Neighborhood',
                        'risk_level': 'Moderate',
                        'risk_score': 65
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-87.6298, 41.8781]
                    }
                }
            ]
        }
        
        # Add choropleth layer (placeholder)
        folium.GeoJson(
            sample_data,
            name='Risk Levels',
            style_function=lambda x: {
                'fillColor': '#3186cc',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.5
            }
        ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Convert to HTML
        map_html = m._repr_html_()
        
        return jsonify({
            'map_html': map_html,
            'city': city_config['name']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/neighborhood_stats/<city_name>/<neighborhood_id>')
def get_neighborhood_stats(city_name, neighborhood_id):
    """Get statistics for a specific neighborhood"""
    
    # Placeholder data
    stats = {
        'neighborhood_id': neighborhood_id,
        'neighborhood_name': f'Neighborhood {neighborhood_id}',
        'risk_level': 'Moderate',
        'risk_score': 65,
        'violent_crime_count': 42,
        'trend': 'decreasing',
        'recommendations': [
            'Increase outreach presence during evening hours',
            'Focus on conflict mediation services',
            'Coordinate with local community organizations'
        ],
        'historical_data': {
            'weeks': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'incidents': [12, 10, 8, 12]
        }
    }
    
    return jsonify(stats)


@app.route('/api/city_summary/<city_name>')
def get_city_summary(city_name):
    """Get overall city statistics"""
    
    summary = {
        'city': city_name,
        'total_neighborhoods': 77,
        'risk_distribution': {
            'Low': 25,
            'Moderate': 30,
            'High': 15,
            'Critical': 7
        },
        'total_incidents_last_week': 234,
        'trend': 'stable',
        'high_risk_neighborhoods': [
            {'id': 1, 'name': 'West Englewood', 'risk_score': 92},
            {'id': 2, 'name': 'Austin', 'risk_score': 88},
            {'id': 3, 'name': 'Englewood', 'risk_score': 85}
        ]
    }
    
    return jsonify(summary)


@app.route('/methodology')
def methodology():
    """Methodology and ethical framework page"""
    return render_template('methodology.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/api/predict', methods=['POST'])
def predict_risk():
    """
    API endpoint for risk prediction
    Accepts neighborhood features and returns risk assessment
    """
    
    try:
        data = request.get_json()
        
        # Extract features
        features = data.get('features', {})
        
        # Placeholder prediction logic
        # In production, load trained model and make real predictions
        risk_score = 65  # Placeholder
        risk_level = 'Moderate'
        
        response = {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'confidence': 0.82,
            'top_factors': [
                {'factor': 'Recent violent crime trend', 'contribution': 0.35},
                {'factor': 'Social vulnerability index', 'contribution': 0.28},
                {'factor': 'Environmental disorder', 'contribution': 0.22}
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)
