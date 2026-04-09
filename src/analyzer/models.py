import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from typing import List, Dict, Any, Optional

class AstroPredictor:
    """
    High-density predictive model for celestial-financial direction.
    Uses ensemble learners to mapping astro-features to market direction.
    """

    def __init__(self, model_params: Optional[Dict[str, Any]] = None):
        """
        model_params: Configuration for the Random Forest Classifier.
        """
        self.params = model_params or {
            "n_estimators": 100,
            "max_depth": 7,
            "random_state": 42
        }
        self.model = RandomForestClassifier(**self.params)

    def train(self, df: pd.DataFrame, feature_cols: List[str]) -> float:
        """
        Trains the model on high-density celestial features.
        Returns the accuracy score on the test set.
        """
        X = df[feature_cols]
        y = df["target_direction"]
        
        # Split into training and test sets (Time-Aware Split should be used in production)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        self.model.fit(X_train, y_train)
        
        # Verification
        y_pred = self.model.predict(X_test)
        return accuracy_score(y_test, y_pred)

    def predict_next(self, current_features: pd.DataFrame) -> Dict[str, Any]:
        """
        Predicts the direction of the next period (Up=1, Down=0).
        """
        prediction = self.model.predict(current_features)
        probability = self.model.predict_proba(current_features)
        
        return {
            "direction": int(prediction[0]),
            "probability_up": float(probability[0][1]),
            "probability_down": float(probability[0][0])
        }

    def get_feature_importance(self, feature_cols: List[str]) -> Dict[str, float]:
        """
        Returns which planets/aspects are driving the prediction.
        """
        importances = self.model.feature_importances_
        return dict(zip(feature_cols, importances))
