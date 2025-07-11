# Concrete Strength Predictor

## 1. Project Overview

This project is a sophisticated desktop application designed to predict the compressive strength of concrete. It provides a user-friendly graphical interface (GUI) for inputting various components of a concrete mixture and leverages machine learning to deliver accurate strength predictions. The application is not just a simple predictor; it also includes an expert system to validate inputs, ensuring they fall within realistic and effective ranges for concrete production.

## 2. Goal and Objectives

The primary goal of this project is to provide a practical and reliable tool for civil engineers, students, and researchers to estimate concrete strength without the need for immediate physical testing. The key objectives are:

- To predict the mean compressive strength of concrete with high accuracy.
- To provide a probabilistic range (10th and 90th percentiles) to account for variability in materials and conditions.
- To create an intuitive and easy-to-use interface for seamless user interaction.
- To implement a knowledge-based expert system that guides users toward creating valid and effective concrete mix designs.
- To maintain a history of predictions for future reference and analysis.

## 3. Features and Functionalities

- **Graphical User Interface:** A clean and modern interface built with Tkinter, featuring a light green theme for a pleasant user experience.
- **Mean and Quantile Predictions:** The application predicts not only the mean strength but also the 10th and 90th percentile strengths, offering a comprehensive view of the likely strength range.
- **Expert System:** A rule-based knowledge base (`knowledge_base.py`) validates user inputs in real-time, providing warnings for values that are outside of typical engineering standards.
- **Database Integration:** All predictions are automatically saved to a local database (`database.py`), allowing for a persistent record of past analyses.
- **Responsive Design:** The application window can be resized, and the components will adjust accordingly.

## 4. Working Procedure

1.  **Input:** The user enters the quantities of the eight key components of the concrete mix:
    - Cement (kg/m³)
    - Blast Furnace Slag (kg/m³)
    - Fly Ash (kg/m³)
    - Water (kg/m³)
    - Superplasticizer (kg/m³)
    - Coarse Aggregate (kg/m³)
    - Fine Aggregate (kg/m³)
    - Age (days)
2.  **Validation:** Upon clicking the "Submit" button, the application first validates the inputs using the rules defined in the `knowledge_base.py` module.
3.  **Prediction:** If the inputs are valid, the application uses the pre-trained machine learning models to predict the concrete's compressive strength.
4.  **Output:** The predicted mean strength and the 80% probability range are displayed to the user.
5.  **Data Storage:** The input values and the corresponding predictions are stored in a local database for future reference.

## 5. Machine Learning Models

The application uses three pre-trained XGBoost models:

- `xgboost_model_strength.joblib`: This model predicts the mean compressive strength.
- `xgb_quantile_model_10.joblib`: This model predicts the 10th percentile of the compressive strength.
- `xgb_quantile_model_90.joblib`: This model predicts the 90th percentile of the compressive strength.

These models have been trained on a comprehensive dataset of concrete mix designs and their corresponding strengths.

## 6. Knowledge Base

The expert system in `knowledge_base.py` enforces the following rules to ensure the validity of the concrete mix design:

- **Critical Components:** Cement, Water, and Age are essential for strength development and cannot be zero.
- **Water-Cement Ratio:** The water-to-cement ratio is checked to be within the typical range of 0.4 to 0.6.
- **Aggregate Proportions:** The ratio of coarse to total aggregates is validated to be within the standard range of 0.5 to 0.7.
- **Superplasticizer Dosage:** The superplasticizer amount is checked to be within a reasonable limit (not exceeding 20 kg/m³).

## 7. How to Run the Application

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd AiUserFriendlyProject-DbConnected
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```

## 8. Future Work

- **Expanded Knowledge Base:** Incorporate more sophisticated rules, such as slump and air content estimations, to provide more comprehensive feedback on the mix design.
- **Data Visualization:** Add a feature to visualize the prediction history, allowing users to track and compare different mix designs over time.
- **Model Retraining:** Implement a mechanism to allow users to retrain the models with new data, keeping the prediction engine up-to-date with the latest information.
- **User Accounts:** Introduce user accounts to allow for personalized prediction histories and model management.