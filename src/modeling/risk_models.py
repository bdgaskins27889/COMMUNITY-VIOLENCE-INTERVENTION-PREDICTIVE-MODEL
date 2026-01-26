"""
Risk Prediction Models
Implements logistic regression, random forest, and clustering for violence risk assessment
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
import joblib
import os
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class RiskPredictor:
    """Base class for violence risk prediction models"""
    
    def __init__(self, model_config: Dict, random_state: int = 42):
        """
        Initialize risk predictor
        
        Args:
            model_config: Model configuration dictionary
            random_state: Random seed for reproducibility
        """
        self.model_config = model_config
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = None
        self.feature_names = None
        self.feature_importance = None
    
    def prepare_features(
        self,
        df: pd.DataFrame,
        target_col: str,
        feature_cols: list
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features and target for modeling
        
        Args:
            df: Input DataFrame
            target_col: Name of target variable
            feature_cols: List of feature column names
            
        Returns:
            Tuple of (features DataFrame, target Series)
        """
        # Remove rows with missing target
        df_clean = df.dropna(subset=[target_col]).copy()
        
        # Select features
        X = df_clean[feature_cols].copy()
        y = df_clean[target_col].copy()
        
        # Handle missing values in features
        X = X.fillna(X.median())
        
        # Store feature names
        self.feature_names = feature_cols
        
        return X, y
    
    def train_test_split_data(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2
    ) -> Tuple:
        """Split data into training and testing sets"""
        return train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=self.random_state,
            stratify=y if len(y.unique()) > 1 else None
        )
    
    def evaluate_model(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Evaluate model performance
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities (optional)
            
        Returns:
            Dictionary of evaluation metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }
        
        # Add AUC if probabilities provided
        if y_pred_proba is not None and len(np.unique(y_true)) == 2:
            metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
        
        # Confusion matrix
        metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred)
        
        return metrics
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance,
            'config': self.model_config
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.feature_importance = model_data.get('feature_importance')
        self.model_config = model_data['config']
        
        print(f"Model loaded from {filepath}")


class LogisticRiskModel(RiskPredictor):
    """Logistic Regression for interpretable risk prediction"""
    
    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series
    ) -> Dict:
        """
        Train logistic regression model
        
        Args:
            X_train: Training features
            y_train: Training target
            
        Returns:
            Dictionary of training metrics
        """
        print("Training Logistic Regression model...")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Initialize model
        self.model = LogisticRegression(
            max_iter=self.model_config.get('max_iter', 1000),
            solver=self.model_config.get('solver', 'lbfgs'),
            class_weight=self.model_config.get('class_weight', 'balanced'),
            random_state=self.random_state
        )
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Extract feature importance (coefficients)
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'coefficient': self.model.coef_[0],
            'abs_coefficient': np.abs(self.model.coef_[0])
        }).sort_values('abs_coefficient', ascending=False)
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, 
            cv=5, scoring='accuracy'
        )
        
        print(f"Training complete. CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        return {
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    def predict(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Make predictions
        
        Args:
            X: Features
            
        Returns:
            Tuple of (predictions, probabilities)
        """
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        return predictions, probabilities


class RandomForestRiskModel(RiskPredictor):
    """Random Forest for capturing complex patterns"""
    
    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series
    ) -> Dict:
        """Train random forest model"""
        
        print("Training Random Forest model...")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Initialize model
        self.model = RandomForestClassifier(
            n_estimators=self.model_config.get('n_estimators', 100),
            max_depth=self.model_config.get('max_depth', 10),
            min_samples_split=self.model_config.get('min_samples_split', 10),
            min_samples_leaf=self.model_config.get('min_samples_leaf', 5),
            class_weight=self.model_config.get('class_weight', 'balanced'),
            random_state=self.random_state,
            n_jobs=-1
        )
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Extract feature importance
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, 
            cv=5, scoring='accuracy'
        )
        
        print(f"Training complete. CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        return {
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    def predict(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions"""
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        return predictions, probabilities


class RiskClusteringModel:
    """K-Means clustering for risk tier grouping"""
    
    def __init__(self, n_clusters: int = 4, random_state: int = 42):
        """
        Initialize clustering model
        
        Args:
            n_clusters: Number of risk tiers (default: 4 for Low/Moderate/High/Critical)
            random_state: Random seed
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = None
        self.cluster_labels = ['Low', 'Moderate', 'High', 'Critical']
    
    def train(self, X: pd.DataFrame) -> Dict:
        """
        Train clustering model
        
        Args:
            X: Features
            
        Returns:
            Dictionary with cluster statistics
        """
        print("Training K-Means clustering model...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Initialize and train model
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10
        )
        
        clusters = self.model.fit_predict(X_scaled)
        
        # Calculate cluster centers
        cluster_centers = pd.DataFrame(
            self.scaler.inverse_transform(self.model.cluster_centers_),
            columns=X.columns
        )
        
        # Assign risk labels based on mean values
        cluster_means = []
        for i in range(self.n_clusters):
            cluster_means.append(X[clusters == i].mean().mean())
        
        # Sort clusters by severity
        cluster_order = np.argsort(cluster_means)
        self.cluster_mapping = {
            cluster_order[i]: self.cluster_labels[i] 
            for i in range(self.n_clusters)
        }
        
        print(f"Clustering complete. {self.n_clusters} risk tiers identified.")
        
        return {
            'cluster_centers': cluster_centers,
            'cluster_mapping': self.cluster_mapping,
            'inertia': self.model.inertia_
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict cluster assignments
        
        Args:
            X: Features
            
        Returns:
            Array of cluster labels
        """
        X_scaled = self.scaler.transform(X)
        clusters = self.model.predict(X_scaled)
        
        # Map to risk labels
        risk_labels = np.array([self.cluster_mapping[c] for c in clusters])
        
        return risk_labels
    
    def save_model(self, filepath: str):
        """Save clustering model"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'cluster_mapping': self.cluster_mapping,
            'n_clusters': self.n_clusters
        }
        
        joblib.dump(model_data, filepath)
        print(f"Clustering model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load clustering model"""
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.cluster_mapping = model_data['cluster_mapping']
        self.n_clusters = model_data['n_clusters']
        
        print(f"Clustering model loaded from {filepath}")


def create_binary_target(
    df: pd.DataFrame,
    value_col: str,
    threshold: Optional[float] = None,
    percentile: int = 75
) -> pd.Series:
    """
    Create binary target variable for classification
    
    Args:
        df: Input DataFrame
        value_col: Column to threshold
        threshold: Explicit threshold value (if None, use percentile)
        percentile: Percentile for automatic threshold
        
    Returns:
        Binary target Series (1 = high risk, 0 = low risk)
    """
    if threshold is None:
        threshold = df[value_col].quantile(percentile / 100)
    
    target = (df[value_col] > threshold).astype(int)
    
    print(f"Binary target created: {target.sum()} high-risk, {len(target) - target.sum()} low-risk")
    print(f"Threshold: {threshold:.2f}")
    
    return target
