# Heart Attack Predictor

## Overview
The Heart Attack Predictor is a web-based application designed to predict the risk of heart attacks based on user inputs. It leverage machine learning models trained on medical data to provide predictions. The application includes a user-friendly interface built with Dash components and Flask to ensure seamless interaction and scalability.

![Webapp Demo](https://github.com/HanaHelaly/Heart-Attack-ML/blob/main/HA.gif)

## Features
1. **Homepage:**
   - Provides information about the required medical tests and their significance in assessing heart attack risk.

2. **Heart Attack Mortality Insights:**
   - Displays global statistics on heart attack mortality rates, highlighting its prevalence each year.

3. **Prediction Page:**
   - Accepts user inputs (e.g., age, cholesterol levels, blood pressure) and predicts whether the user is at high or low risk of a heart attack.

## Models and Performance
Two machine learning models were developed and evaluated for this project:

1. **Logistic Regression:**
   - Simple and interpretable model.
   - Achieved an accuracy of **87%**, which is a reliable metric due to the balanced nature of the dataset.

2. **XGBoost:**
   - Advanced gradient-boosted decision tree model.

## Technologies Used
1. **Frontend:**
   - Built using Dash components for an interactive user experience.
   - Designed to be intuitive and visually appealing.

2. **Backend:**
   - Flask framework to manage server-side logic and integrate with the machine learning models.

3. **Machine Learning:**
   - Models were trained using Python libraries such as scikit-learn and XGBoost.
   - Preprocessing steps included handling missing values, feature engineering, and balancing the dataset.

## App Pages in Detail
### 1. Homepage
   - Lists the medical tests required for input:
     - Age
     - Resting blood pressure (mm Hg)
     - Cholesterol level (mg/dL)
     - Maximum heart rate achieved during exercise (bpm)
     - Other relevant factors (e.g., gender, type of chest pain, fasting blood sugar levels).
       
### 2. Heart Attack Mortality Statistics
   - Provides global insights into the prevalence of heart attack mortality each year.
   - Uses visualizations to highlight trends and emphasize the importance of early risk detection.

### 3. Prediction Page
   - Allows users to input their medical data.
   - Predicts whether the user is at high or low risk of a heart attack.
   - Displays the prediction result in a clear and user-friendly format with alerts.
   - Utilizes SHAP values to provide interpretability, explaining the contribution of each feature to the prediction for the user.

## Deployment
1. **Running Locally:**
   - Clone the repository.
   - Install required Python packages using:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the Flask server:
     ```bash
     python index.py
     ```
   - Access the Dash app on your local browser at port `8050`.
   - Note: data folder contains the data for the 2nd page plot.

