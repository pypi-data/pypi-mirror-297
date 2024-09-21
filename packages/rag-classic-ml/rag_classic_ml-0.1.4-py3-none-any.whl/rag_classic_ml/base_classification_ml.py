# base_classification_ml.py

import pandas as pd
import numpy as np
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
import joblib  # For saving the model

class FeatureClassifier:
    def __init__(self, model_name, model_params=None):
        self.model_name = model_name
        self.model_params = model_params if model_params is not None else {}
        self.model = self.initialize_model()

    def initialize_model(self):
        if self.model_name == 'LogisticRegression':
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(**self.model_params)
        elif self.model_name == 'SVC':
            from sklearn.svm import SVC
            # Enable probability estimates if not already set
            if 'probability' not in self.model_params:
                self.model_params['probability'] = True
            model = SVC(**self.model_params)
        elif self.model_name == 'RandomForestClassifier':
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(**self.model_params)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
        return model

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        
        # Handle cases where predict_proba might not be available
        if hasattr(self.model, "predict_proba"):
            y_scores = self.model.predict_proba(X_test)
        elif hasattr(self.model, "decision_function"):
            y_scores = self.model.decision_function(X_test)
            # For binary classification, convert to probabilities
            if len(y_scores.shape) == 1:
                y_scores = np.vstack([-y_scores, y_scores]).T
        else:
            y_scores = None  # AUC cannot be calculated without scores

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
        }

        if y_scores is not None:
            try:
                if y_scores.shape[1] == 2:
                    # Binary classification: use the probability of the positive class
                    y_scores_binary = y_scores[:, 1]
                    metrics['auc'] = roc_auc_score(y_test, y_scores_binary)
                else:
                    # Multiclass classification: use 'ovr' strategy
                    metrics['auc'] = roc_auc_score(y_test, y_scores, multi_class='ovr')
            except ValueError as e:
                print(f"ROC AUC Score could not be computed: {e}")
                metrics['auc'] = None
        else:
            metrics['auc'] = None

        return metrics

    def save_model(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        model_path = os.path.join(output_dir, f'{self.model_name}_model.joblib')
        joblib.dump(self.model, model_path)
        print(f"Model saved to {model_path}")
