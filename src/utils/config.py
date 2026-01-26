"""
Configuration settings for CVI Risk Predictor
Multi-city support with extensible configuration
"""

import os
from typing import Dict, Any

# Base configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
BOUNDARIES_DIR = os.path.join(DATA_DIR, 'boundaries')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# API Configuration
CENSUS_API_KEY = os.getenv('CENSUS_API_KEY', None)
SOCRATA_APP_TOKEN = os.getenv('SOCRATA_APP_TOKEN', None)

# City-specific configurations
CITY_CONFIGS: Dict[str, Dict[str, Any]] = {
    'chicago': {
        'name': 'Chicago',
        'state': 'IL',
        'crime_data': {
            'source': 'socrata',
            'domain': 'data.cityofchicago.org',
            'dataset_id': 'ijzp-q8t2',
            'date_field': 'date',
            'lat_field': 'latitude',
            'lon_field': 'longitude',
            'type_field': 'primary_type',
            'violent_crimes': ['HOMICIDE', 'ASSAULT', 'BATTERY', 'ROBBERY', 
                             'CRIMINAL SEXUAL ASSAULT', 'CRIM SEXUAL ASSAULT']
        },
        'shotspotter_data': {
            'source': 'socrata',
            'domain': 'data.cityofchicago.org',
            'dataset_id': '3h7q-7mdb',
            'date_field': 'date',
            'lat_field': 'latitude',
            'lon_field': 'longitude'
        },
        'abandoned_buildings': {
            'source': 'socrata',
            'domain': 'data.cityofchicago.org',
            'dataset_id': '7nii-7srd',
            'lat_field': 'latitude',
            'lon_field': 'longitude'
        },
        'boundaries': {
            'type': 'community_areas',
            'url': 'https://data.cityofchicago.org/resource/cauq-8yn6.geojson'
        },
        'census': {
            'state_fips': '17',
            'county_fips': '031'  # Cook County
        }
    },
    'new_york': {
        'name': 'New York City',
        'state': 'NY',
        'crime_data': {
            'source': 'socrata',
            'domain': 'data.cityofnewyork.us',
            'dataset_id': '5uac-w243',
            'date_field': 'cmplnt_fr_dt',
            'lat_field': 'latitude',
            'lon_field': 'longitude',
            'type_field': 'ofns_desc',
            'violent_crimes': ['MURDER', 'ASSAULT', 'RAPE', 'ROBBERY', 
                             'FELONY ASSAULT', 'GRAND LARCENY OF MOTOR VEHICLE']
        },
        'boundaries': {
            'type': 'neighborhoods',
            'url': 'https://data.cityofnewyork.us/resource/xyye-rtrs.geojson'
        },
        'census': {
            'state_fips': '36',
            'county_fips': ['061', '047', '081', '005', '085']  # 5 boroughs
        }
    },
    'los_angeles': {
        'name': 'Los Angeles',
        'state': 'CA',
        'crime_data': {
            'source': 'socrata',
            'domain': 'data.lacity.org',
            'dataset_id': '2nrs-mtv8',
            'date_field': 'date_occ',
            'lat_field': 'lat',
            'lon_field': 'lon',
            'type_field': 'crm_cd_desc',
            'violent_crimes': ['CRIMINAL HOMICIDE', 'ASSAULT WITH DEADLY WEAPON', 
                             'RAPE', 'ROBBERY', 'BATTERY']
        },
        'boundaries': {
            'type': 'neighborhoods',
            'url': 'https://data.lacity.org/resource/7jqg-nkf9.geojson'
        },
        'census': {
            'state_fips': '06',
            'county_fips': '037'  # Los Angeles County
        }
    },
    'philadelphia': {
        'name': 'Philadelphia',
        'state': 'PA',
        'crime_data': {
            'source': 'socrata',
            'domain': 'phl.carto.com',
            'dataset_id': 'incidents_part1_part2',
            'date_field': 'dispatch_date_time',
            'lat_field': 'lat',
            'lon_field': 'lng',
            'type_field': 'text_general_code',
            'violent_crimes': ['Homicide', 'Aggravated Assault', 'Rape', 'Robbery']
        },
        'boundaries': {
            'type': 'neighborhoods',
            'url': 'https://opendata.arcgis.com/datasets/neighborhoods.geojson'
        },
        'census': {
            'state_fips': '42',
            'county_fips': '101'  # Philadelphia County
        }
    }
}

# Model Configuration
MODEL_CONFIG = {
    'random_state': 42,
    'test_size': 0.2,
    'cv_folds': 5,
    'n_clusters': 4,  # Low, Moderate, High, Critical risk
    'models': {
        'logistic_regression': {
            'max_iter': 1000,
            'solver': 'lbfgs',
            'class_weight': 'balanced'
        },
        'random_forest': {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 10,
            'min_samples_leaf': 5,
            'class_weight': 'balanced'
        },
        'kmeans': {
            'n_clusters': 4,
            'n_init': 10,
            'max_iter': 300
        }
    }
}

# Feature Engineering Configuration
FEATURE_CONFIG = {
    'temporal_aggregation': 'weekly',  # weekly, monthly
    'spatial_aggregation': 'neighborhood',  # neighborhood, tract, block_group
    'lookback_weeks': 12,  # Historical period for feature creation
    'forecast_weeks': 4,  # Prediction horizon
    'min_population': 500,  # Minimum population for neighborhood inclusion
    'features': {
        'crime_features': [
            'violent_crime_count',
            'violent_crime_rate',
            'crime_trend',
            'weekend_crime_ratio'
        ],
        'environmental_features': [
            'abandoned_building_count',
            'abandoned_building_density'
        ],
        'socioeconomic_features': [
            'median_income',
            'unemployment_rate',
            'poverty_rate',
            'education_less_than_hs'
        ],
        'vulnerability_features': [
            'svi_overall',
            'svi_socioeconomic',
            'svi_household_composition',
            'svi_minority_language',
            'svi_housing_transportation'
        ],
        'infrastructure_features': [
            'school_count',
            'park_count',
            'transit_access'
        ]
    }
}

# Visualization Configuration
VIZ_CONFIG = {
    'color_schemes': {
        'risk_levels': {
            'Low': '#2ecc71',
            'Moderate': '#f39c12',
            'High': '#e67e22',
            'Critical': '#e74c3c'
        }
    },
    'map_style': 'OpenStreetMap',
    'default_zoom': 11
}

# Ethical Safeguards
ETHICAL_CONFIG = {
    'individual_prediction': False,
    'min_aggregation_level': 'neighborhood',
    'min_population_threshold': 500,
    'data_retention_days': 730,  # 2 years
    'intended_use': 'violence_prevention',
    'prohibited_use': ['law_enforcement_surveillance', 'individual_targeting', 
                       'predictive_policing']
}

# API Rate Limits
RATE_LIMITS = {
    'socrata_without_token': 1000,  # requests per day
    'socrata_with_token': 50000,    # requests per day
    'census_api': 500,               # requests per day
    'overpass_api': 10000            # requests per day
}


def get_city_config(city_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific city
    
    Args:
        city_name: Name of the city (lowercase)
        
    Returns:
        Dictionary containing city-specific configuration
    """
    city_key = city_name.lower().replace(' ', '_')
    if city_key not in CITY_CONFIGS:
        raise ValueError(f"City '{city_name}' not configured. "
                        f"Available cities: {list(CITY_CONFIGS.keys())}")
    return CITY_CONFIGS[city_key]


def list_available_cities() -> list:
    """Return list of configured cities"""
    return [config['name'] for config in CITY_CONFIGS.values()]
