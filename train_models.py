"""
Complete ML Training Pipeline for CVI Risk Predictor
Trains all three models (Logistic Regression, Random Forest, K-Means) and saves them
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.modeling.risk_models import (
    LogisticRiskModel, 
    RandomForestRiskModel, 
    RiskClusteringModel,
    create_binary_target
)
from src.utils.config import MODEL_CONFIG

def create_sample_training_data(n_samples=1000):
    """
    Create synthetic training data for demonstration
    In production, this would load real processed data
    """
    print("Generating sample training data...")
    
    np.random.seed(42)
    
    # Generate features
    data = {
        # Crime features
        'violent_crime_count_lag_1w': np.random.poisson(15, n_samples),
        'violent_crime_count_lag_2w': np.random.poisson(14, n_samples),
        'violent_crime_count_lag_4w': np.random.poisson(13, n_samples),
        'crime_trend_12w': np.random.uniform(-2, 2, n_samples),
        'crime_rolling_avg_4w': np.random.uniform(10, 25, n_samples),
        
        # Socioeconomic features
        'median_household_income': np.random.uniform(25000, 85000, n_samples),
        'unemployment_rate': np.random.uniform(3, 18, n_samples),
        'poverty_rate': np.random.uniform(5, 40, n_samples),
        'education_less_than_hs_pct': np.random.uniform(5, 35, n_samples),
        
        # Vulnerability features
        'svi_overall_score': np.random.uniform(0, 1, n_samples),
        'svi_socioeconomic': np.random.uniform(0, 1, n_samples),
        'svi_household_composition': np.random.uniform(0, 1, n_samples),
        
        # Environmental features
        'abandoned_building_density': np.random.uniform(0, 0.1, n_samples),
        'vacancy_rate': np.random.uniform(0, 25, n_samples),
        
        # Population
        'population_density': np.random.uniform(1000, 15000, n_samples),
        
        # Target variable (current week crime count)
        'violent_crime_count': np.random.poisson(16, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Add some realistic correlations
    df.loc[df['svi_overall_score'] > 0.7, 'violent_crime_count'] += np.random.poisson(5, sum(df['svi_overall_score'] > 0.7))
    df.loc[df['unemployment_rate'] > 12, 'violent_crime_count'] += np.random.poisson(3, sum(df['unemployment_rate'] > 12))
    df.loc[df['crime_trend_12w'] > 1, 'violent_crime_count'] += np.random.poisson(4, sum(df['crime_trend_12w'] > 1))
    
    # Add neighborhood IDs
    df['neighborhood_id'] = range(1, n_samples + 1)
    df['neighborhood_name'] = [f'Neighborhood {i}' for i in range(1, n_samples + 1)]
    
    print(f"✓ Generated {len(df)} training samples")
    return df


def train_logistic_regression(X_train, y_train, X_test, y_test):
    """Train and evaluate Logistic Regression model"""
    print("\n" + "="*70)
    print("TRAINING LOGISTIC REGRESSION MODEL")
    print("="*70)
    
    model = LogisticRiskModel(MODEL_CONFIG['models']['logistic_regression'])
    
    # Train
    train_metrics = model.train(X_train, y_train)
    
    # Evaluate on test set
    predictions, probabilities = model.predict(X_test)
    test_metrics = model.evaluate_model(y_test, predictions, probabilities)
    
    print("\nTest Set Performance:")
    print(f"  Accuracy:  {test_metrics['accuracy']:.3f}")
    print(f"  Precision: {test_metrics['precision']:.3f}")
    print(f"  Recall:    {test_metrics['recall']:.3f}")
    print(f"  F1-Score:  {test_metrics['f1_score']:.3f}")
    if 'roc_auc' in test_metrics:
        print(f"  ROC-AUC:   {test_metrics['roc_auc']:.3f}")
    
    print("\nTop 10 Most Important Features:")
    print(model.feature_importance.head(10).to_string(index=False))
    
    # Save model
    model_path = 'models/trained_models/logistic_regression_model.pkl'
    model.save_model(model_path)
    
    return model, test_metrics


def train_random_forest(X_train, y_train, X_test, y_test):
    """Train and evaluate Random Forest model"""
    print("\n" + "="*70)
    print("TRAINING RANDOM FOREST MODEL")
    print("="*70)
    
    model = RandomForestRiskModel(MODEL_CONFIG['models']['random_forest'])
    
    # Train
    train_metrics = model.train(X_train, y_train)
    
    # Evaluate on test set
    predictions, probabilities = model.predict(X_test)
    test_metrics = model.evaluate_model(y_test, predictions, probabilities)
    
    print("\nTest Set Performance:")
    print(f"  Accuracy:  {test_metrics['accuracy']:.3f}")
    print(f"  Precision: {test_metrics['precision']:.3f}")
    print(f"  Recall:    {test_metrics['recall']:.3f}")
    print(f"  F1-Score:  {test_metrics['f1_score']:.3f}")
    if 'roc_auc' in test_metrics:
        print(f"  ROC-AUC:   {test_metrics['roc_auc']:.3f}")
    
    print("\nTop 10 Most Important Features:")
    print(model.feature_importance.head(10).to_string(index=False))
    
    # Save model
    model_path = 'models/trained_models/random_forest_model.pkl'
    model.save_model(model_path)
    
    return model, test_metrics


def train_clustering(X_full):
    """Train K-Means clustering model"""
    print("\n" + "="*70)
    print("TRAINING K-MEANS CLUSTERING MODEL")
    print("="*70)
    
    model = RiskClusteringModel(
        n_clusters=MODEL_CONFIG['models']['kmeans']['n_clusters']
    )
    
    # Train
    cluster_info = model.train(X_full)
    
    print("\nCluster Mapping:")
    for cluster_id, label in cluster_info['cluster_mapping'].items():
        print(f"  Cluster {cluster_id}: {label}")
    
    print(f"\nModel Inertia: {cluster_info['inertia']:.2f}")
    
    # Save model
    model_path = 'models/trained_models/kmeans_clustering_model.pkl'
    model.save_model(model_path)
    
    return model, cluster_info


def main():
    """Main training pipeline"""
    print("="*70)
    print("CVI RISK PREDICTOR - MODEL TRAINING PIPELINE")
    print("="*70)
    print()
    
    # Create output directories
    os.makedirs('models/trained_models', exist_ok=True)
    os.makedirs('models/model_evaluation', exist_ok=True)
    
    # Generate or load training data
    df = create_sample_training_data(n_samples=1000)
    
    # Define feature columns
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
    
    # Create binary target (high risk = 1, low risk = 0)
    df['high_risk'] = create_binary_target(
        df, 
        'violent_crime_count', 
        percentile=75
    )
    
    # Prepare features and target
    X = df[feature_cols]
    y = df['high_risk']
    
    # Train-test split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nDataset Split:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples:  {len(X_test)}")
    print(f"  High-risk ratio:  {y.mean():.2%}")
    
    # Train all models
    results = {}
    
    # 1. Logistic Regression
    lr_model, lr_metrics = train_logistic_regression(X_train, y_train, X_test, y_test)
    results['logistic_regression'] = lr_metrics
    
    # 2. Random Forest
    rf_model, rf_metrics = train_random_forest(X_train, y_train, X_test, y_test)
    results['random_forest'] = rf_metrics
    
    # 3. K-Means Clustering
    kmeans_model, cluster_info = train_clustering(X)
    results['kmeans'] = cluster_info
    
    # Save results summary
    print("\n" + "="*70)
    print("TRAINING COMPLETE - MODEL COMPARISON")
    print("="*70)
    
    comparison = pd.DataFrame({
        'Model': ['Logistic Regression', 'Random Forest'],
        'Accuracy': [
            results['logistic_regression']['accuracy'],
            results['random_forest']['accuracy']
        ],
        'Precision': [
            results['logistic_regression']['precision'],
            results['random_forest']['precision']
        ],
        'Recall': [
            results['logistic_regression']['recall'],
            results['random_forest']['recall']
        ],
        'F1-Score': [
            results['logistic_regression']['f1_score'],
            results['random_forest']['f1_score']
        ]
    })
    
    print("\n" + comparison.to_string(index=False))
    
    # Save comparison
    comparison.to_csv('models/model_evaluation/model_comparison.csv', index=False)
    
    print("\n" + "="*70)
    print("ALL MODELS SAVED TO: models/trained_models/")
    print("="*70)
    print("\nSaved models:")
    print("  1. logistic_regression_model.pkl")
    print("  2. random_forest_model.pkl")
    print("  3. kmeans_clustering_model.pkl")
    print("\nThese models are now ready for use in the web application!")
    print()


if __name__ == "__main__":
    main()
