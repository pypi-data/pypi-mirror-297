# classification_ml.py

import argparse
import os
import pandas as pd
import json
from .base_classification_ml import FeatureClassifier
from .pre_processing import load_and_preprocess_data, split_data

def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description="Run the classification ML pipeline.")
        parser.add_argument('--data', type=str, required=True, help='Path to the CSV file containing the dataset.')
        parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')
        parser.add_argument('--output', type=str, required=True, help='Directory to save the results and trained model.')
        parser.add_argument('--model', type=str, default='LogisticRegression', choices=['LogisticRegression', 'SVC', 'RandomForestClassifier'], help='Model to train.')
        parser.add_argument('--model_params', type=str, default=None, help='Model hyperparameters in JSON format.')
        parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of the dataset to include in the test split.')
        parser.add_argument('--seed', type=int, default=42, help='Seed for random state.')
        args = parser.parse_args()

    # Load and preprocess data
    df = load_and_preprocess_data(args.data, args.target)

    # Split data
    split_data_dict = split_data(df, args.target, test_size=args.test_size, random_state=args.seed)
    X_train, y_train = split_data_dict['train']['X'], split_data_dict['train']['y']
    X_test, y_test = split_data_dict['test']['X'], split_data_dict['test']['y']

    # Parse model parameters
    if args.model_params:
        try:
            model_params = json.loads(args.model_params)
        except json.JSONDecodeError as e:
            print(f"Error parsing model_params JSON: {e}")
            model_params = {}
    else:
        model_params = {}

    # Initialize and train the classifier
    classifier = FeatureClassifier(model_name=args.model, model_params=model_params)
    classifier.train(X_train, y_train)

    # Evaluate the model
    metrics = classifier.evaluate(X_test, y_test)
    print("Evaluation Metrics:")
    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value}")

    # Save the model
    classifier.save_model(args.output)

    # Save the metrics
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(os.path.join(args.output, f'{args.model}_metrics.csv'), index=False)
    print(f"Metrics saved to {os.path.join(args.output, f'{args.model}_metrics.csv')}")
