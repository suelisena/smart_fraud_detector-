# smart_fraud_detector-

💳 Fraud Detection System
📑 Table of Contents
1. [Project Overview](#project-overview)  
2. [Dataset and Preprocessing](#dataset-and-preprocessing)  
3. [Model Training](#model-training)  
4. [Evaluation](#evaluation)  
5. [Prediction on New Data](#prediction-on-new-data)  
6. [Frontend with Streamlit](#frontend-with-streamlit)  
7. [How to Run](#how-to-run)  
8. [Future Improvements](#future-improvements)
9. [Screenshots](#screenshots) 

## Project Overview
This project implements a Machine Learning model for fraud detection in financial transactions. It uses a Neural Network (MLPClassifier) to classify whether a transaction is fraudulent or legitimate.
The project includes:
• 	Data preprocessing and balancing with SMOTE.
• 	Training and evaluation of a fraud detection model.
• 	Saving the trained model and scaler for reuse.
• 	A Streamlit frontend that allows users to input transaction details and receive real-time fraud predictions.
• 	Visualization of dataset statistics for better insights.

## Dataset and Preprocessing
Steps:
• 	Remove irrelevant columns: Transaction and customer IDs are dropped since they don’t carry semantic meaning.
• 	Add simulated fraud cases: High-value online transactions are artificially added to strengthen fraud detection.
• 	Encode categorical variables: The  column is transformed using one-hot encoding.
• 	Feature scaling: Numerical features (, ) are standardized using .
• 	Balance dataset: Fraud cases are often rare, so SMOTE (Synthetic Minority Oversampling Technique) is applied to balance the dataset.

Example: Preprocessing
df = df.drop(columns=['transaction_id', 'customer_id'], errors='ignore')
df_encoded = pd.get_dummies(df, columns=['location'], drop_first=True)
scaler = StandardScaler()
X[['amount', 'time']] = scaler.fit_transform(X[['amount', 'time']])

## Model Training
• 	Algorithm:  (Multi-Layer Perceptron Neural Network).
• 	Architecture: Three hidden layers with sizes .
• 	Activation function: ReLU.
• 	Learning rate: 0.01.
• 	Iterations: Up to 1000.
The model is trained on the balanced dataset and saved as . The scaler is also saved as .
Example:
model = MLPClassifier(hidden_layer_sizes=(50, 30, 20),
                      max_iter=1000,
                      random_state=42,
                      learning_rate_init=0.01,
                      activation='relu')
model.fit(X_train, y_train)

## Evaluation
The model is evaluated using a classification report
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)
print(report)

## Prediction on New Data
The model can predict fraud probability for new transactions.
new_transactions = [
    {"amount": 3871.09, "time": 10, "location": "Physical Store"},
    {"amount": 12.56, "time": 12, "location": "Online"},
]

df_new = pd.DataFrame(new_transactions)
df_new_encoded = pd.get_dummies(df_new, columns=['location'], drop_first=True)
df_new_encoded[['amount', 'time']] = scaler.transform(df_new_encoded[['amount', 'time']])
predictions = model.predict(df_new_encoded)
probabilities = model.predict_proba(df_new_encoded)[:, 1]

## Frontend with Streamlit
The frontend allows users to input transaction details and get fraud predictions in real time.

import streamlit as st
import joblib

model = joblib.load("fraude_model.pkl")
scaler = joblib.load("scaler.pkl")

st.markdown("<h1 style='font-size:40px; color:#2E86C1;'>💳 Fraud Detection System</h1>", unsafe_allow_html=True)

with st.form("fraude_form"):
    amount = st.number_input("Transaction amount (R$)", min_value=0.0)
    time_input = st.number_input("Transaction time (0-23)", min_value=0, max_value=23)
    location = st.selectbox("Transaction location", ["Physical Store", "Online"])
    submitted = st.form_submit_button("Detect Fraud")

    
## How to Run
1. 	Clone the repository:
git clone https://github.com/yourusername/smart_fraud_detector.git
cd smart_fraud_detector

2. 	Install dependencies:
pip install -r requirements.txt

3. 	Run the Streamlit app:
streamlit run app.py


## Future Improvements
• 	Add more features (e.g., device type, transaction frequency).
• 	Deploy the model with Docker or cloud services.
• 	Improve frontend with interactive dashboards.

## Screenshots
### Fraud Detection Form

