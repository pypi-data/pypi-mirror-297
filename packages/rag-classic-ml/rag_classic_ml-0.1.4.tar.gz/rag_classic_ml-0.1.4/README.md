# RAG-Classic-ML

**RAG-Classic-ML** is a versatile Python package designed to provide out-of-the-box machine learning pipelines for both basic and advanced tasks. It simplifies the process of building, training, and evaluating models for tasks like classification, regression, autoencoder-based feature extraction, and survival clustering. The package is designed for ease of use, offering pre-built pipelines and customizable parameters for a variety of machine learning algorithms.

## Table of Contents  

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Machine Learning Pipelines](#classic_ml)
    - [Classification]
    - [Regression]
  - [Advanced Pipelines](#classic_ml)
    - [Autoencoder with Feature Extraction](#train_autoencoder)
    - [Clustering and Survival Analysis](#Cluster)
  - [Train Autoencoder Model](#train-autoencoder-model)
  - [Survival Clustering Analysis](#survival-clustering-analysis)
- [Command-Line Arguments](#command-line-arguments)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

## Features

- **Basic Machine Learning Pipelines**: Ready-to-use pipelines for common supervised learning tasks, including classification and regression, with a variety of machine learning models (e.g., Logistic Regression, SVC, Random Forest).
- **Advanced Pipelines**
  - **Autoencoder** : Dimensionality reduction and feature extraction using deep learning autoencoders.
  - **Survival Clustering Analysis**: Performs clustering on patient features and integrates clinical data to generate Kaplan-Meier survival plots and log-rank tests.
- **Customizable Models and Parameters**: Easily define and customize machine learning models and hyperparameters.
- **Prediction and Metrics Generation**: Generates and saves predictions, feature importance scores, and various performance metrics for each model and run.
- **Aggregation of Results**: Aggregates results across runs and models for comprehensive analysis, facilitating comparison and evaluation.
- **Visualization Tools**: Generates plots including AUC curves, AUC box plots, feature importance charts, radar charts for model performance comparison, and survival analysis plots.

## Installation

You can install the package directly from PyPI:

```bash
pip install classic-ml
```
Alternatively, install from source:

```bash
git clone https://github.com/yourusername/classic-ml.git
cd benchmark-adv-ml
pip install .
```

## Useage
The classic-ml package provides a command-line interface (CLI) for ease of use. Below are examples of how to use the various components.

## Basic Machine Learning Pipelines

### Classification
Train and evaluate a classification model using the classic-ml CLI. You can specify different models and hyperparameters.

### Example 1: Support Vector Classifier (SVC)

```bash
classic-ml classification \
    --data ./Raisin_Dataset.data \
    --target 'label' \
    --output ./results/svc_rbf/ \
    --model SVC \
    --model_params '{"C": 1.0, "kernel": "rbf", "gamma": "scale", "probability": true}' \
    --test_size 0.2 \
    --seed 42
```

### Example 2: Logistic Regression

```bash
classic-ml classification \
    --data ./Raisin_Dataset.data \
    --target 'label' \
    --output ./results/logistic_regression/ \
    --model LogisticRegression \
    --model_params '{"C": 0.5, "penalty": "l1", "solver": "saga", "max_iter": 1000, "class_weight": "balanced"}' \
    --test_size 0.2 \
    --seed 42

```

### Example 3: Random Forest Classifier

```bash
classic-ml classification \
    --data ./Raisin_Dataset.data \
    --target 'label' \
    --output ./results/random_forest/ \
    --model RandomForestClassifier \
    --model_params '{"n_estimators": 100, "max_depth": 10}' \
    --test_size 0.2 \
    --seed 42

```

### Benchmark Machine Learning Models
Run the benchmark ML pipeline to evaluate model stability across multiple runs.

```bash
benchmark-adv-ml benchmark --data ./your_dataset.csv --output ./final_results --prelim_output ./prelim_results --n_runs 10 --seed 42
```
### Train Autoencoder Model
Train and evaluate an autoencoder model for feature extraction.

```bash
classic-ml autoencoder \
    --data ./your_dataset.csv \
    --sampleID 'PatientID' \
    --output_dir ./final_results \
    --prelim_output ./prelim_results \
    --latent_dim 10 \
    --epochs 50 \
    --batch_size 32 \
    --validation_split 0.1 \
    --test_size 0.2 \
    --seed 42

```

### Survival Clustering Analysis
```bash
classic-ml survival_clustering \
    --data_path ./latent_features.csv \
    --clinical_df_path ./clinical_data.csv \
    --save_dir ./final_results

```

## Command-Line Arguments

### Common Arguments
- `--data`: Path to the existing CSV file containing the dataset.
- `--output`: Directory to save the final results and plots.
- `--prelim_output`: Directory to save the preliminary results (predictions).
- `--seed`: Seed for random state (default is 42).
- `--test_size`: Fraction of data to use for testing (default: 0.2).

### Classification/Regression Command Arguments

- `--target`:  Target column name in the dataset (e.g., 'label' for classification or 'price' for regression).
- `--model`:  Specify the machine learning model to use (e.g., SVC, LogisticRegression, RandomForestClassifier, LinearRegression).
- `--model_params`:  Hyperparameters for the specified model in JSON format (e.g., {"C": 1.0, "kernel": "rbf"}).

### Autoencoder Command Arguments

- `--sampleID`: Column name representing the sample or patient ID (default: 'sampleID').
- `--latent_dim`: Dimensionality of the latent space (default: input_dim // 8).
- `--epochs`: Number of training epochs (default: 50).
- `--batch_size`: Training batch size (default: 32).
- `--validation_split`: Proportion of training data to use as validation set (default: 0.1).
- `--test_size`: Proportion of data to use as test set (default: 0.2).
- `--early_stopping`: Enable early stopping (use flag to activate).
- `--patience`: Patience for early stopping (default: 5).
- `--checkpoint`: Enable model checkpointing (use flag to activate).


### Benchmark Command Arguments

- `--target`: Target column name in the dataset (default: 'label').
- `--n_runs`: Number of runs for model stability evaluation (default: 20).

### Survival Clustering Command Arguments

- `--data_path`: Path to the CSV file containing patient features.
- `--clinical_df_path`: Path to the CSV file containing clinical data.
- `--save_dir`: Directory to save the results.

## Dependencies

- Python 3.11+
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- tensorflow
- lifelines
- yellowbrick

## License 
This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. See the LICENSE file for details.

## Author
Vatsal Patel - VatsalPatel18