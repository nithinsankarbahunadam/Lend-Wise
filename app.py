from flask import Flask, render_template, request
import joblib
import numpy as np
from datetime import datetime
import snowflake.connector
from pathlib import Path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# Load models and scalers
model_risk = joblib.load('loan_one_model.pkl')
model_grade = joblib.load('loan_second_model.joblib')
scaler_risk = joblib.load('loan_one_model_scaler.pkl')
scaler_grade = joblib.load('loan_second_model_scaler.joblib')

# Snowflake private key loader
def load_private_key():
    with open("rsa_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
        return private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

# Snowflake insert function
def insert_into_snowflake(data):
    p_key = load_private_key()
    conn = snowflake.connector.connect(
        user='NITHIN_APP_USER',
        account='bj72627.us-east-2.aws',
        private_key=p_key,
        warehouse='CIBIL_WH',
        database='CIBIL_DB',
        schema='PUBLIC',
        authenticator='snowflake',
        role='SYSADMIN'
    )
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO loan_user_data (
        loan_amount, employment_status, credit_score, income, debt_to_income_ratio, age,
        interest_rate, existing_loan_balance, previous_default,
        borrower_rate, interest_paid, installment, term, principal_paid,
        amount_borrowed, origination_date, last_payment_date, loan_age,
        predicted_risk, predicted_grade, final_prediction
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()

# Risk and grade mappers
def map_risk_level(risk_code):
    return {0: "Low", 1: "Medium", 2: "High"}.get(risk_code, "Unknown")

def map_grade_level(grade_code):
    return {'A': "Low", 'B': "Medium", 'C': "High"}.get(grade_code, "Unknown")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect form data
    loan_amount = float(request.form['loan_amount'])
    employment_status = int(request.form['employment_status'])
    credit_score = int(request.form['credit_score'])
    income = float(request.form['income'])
    debt_to_income_ratio = float(request.form['debt_to_income_ratio'])
    age = int(request.form['age'])
    interest_rate = float(request.form['interest_rate'])
    existing_loan_balance = float(request.form['existing_loan_balance'])
    previous_default = int(request.form['previous_default'])

    borrower_rate = interest_rate
    interest_paid = float(request.form['interest_paid'])
    installment = float(request.form['installment'])
    term = int(request.form['term'])
    principal_paid = float(request.form['principal_paid'])
    amount_borrowed = loan_amount

    origination_date = datetime.strptime(request.form['origination_date'], "%Y-%m-%d")
    last_payment_date = datetime.strptime(request.form['last_payment_date'], "%Y-%m-%d")
    loan_age = (last_payment_date - origination_date).days / 365

    # Prepare inputs
    risk_input_data = np.array([[loan_amount, employment_status, credit_score, income,
                                 debt_to_income_ratio, age, interest_rate,
                                 existing_loan_balance, previous_default]])
    grade_input_data = np.array([[borrower_rate, interest_paid, installment, term,
                                  principal_paid, amount_borrowed, loan_age]])

    risk_input_scaled = scaler_risk.transform(risk_input_data)
    grade_input_scaled = scaler_grade.transform(grade_input_data)

    # Predict risk and grade
    predicted_risk_code = model_risk.predict(risk_input_scaled)[0]
    predicted_grade_code = model_grade.predict(grade_input_scaled)[0]

    predicted_risk = map_risk_level(predicted_risk_code)
    predicted_grade = map_grade_level(predicted_grade_code)

    if predicted_risk == predicted_grade:
        final_prediction = predicted_risk
    elif "High" in [predicted_risk, predicted_grade]:
        final_prediction = "High"
    elif "Medium" in [predicted_risk, predicted_grade]:
        final_prediction = "Medium"
    else:
        final_prediction = "Low"

    # Save prediction in Snowflake
    data_to_insert = (
        loan_amount, employment_status, credit_score, income, debt_to_income_ratio, age,
        interest_rate, existing_loan_balance, previous_default,
        borrower_rate, interest_paid, installment, term, principal_paid,
        amount_borrowed, origination_date, last_payment_date, loan_age,
        predicted_risk, predicted_grade, final_prediction
    )
    insert_into_snowflake(data_to_insert)

    return render_template('result.html',
                           predicted_risk=predicted_risk,
                           predicted_grade=predicted_grade,
                           final_prediction=final_prediction,)

if __name__ == '__main__':
    app.run(debug=True)