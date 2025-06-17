# Lend-Wise
Lend-Wise is a Flask-based peer-to-peer lending app that uses machine learning to predict borrower risk levels and loan grades. It enables data-driven loan approvals and integrates with Snowflake for secure storage.

# 💸 Lend-Wise: Loan Risk & Grade Prediction for Peer-to-Peer Lending

Lend-Wise is a full-stack machine learning web application designed to assist peer-to-peer lending platforms in evaluating borrower risk and loan grade. By combining predictive analytics with real-time simulation and secure backend integration, Lend-Wise helps lenders make informed decisions that improve credit trust and reduce default rates.

---

## 🚀 Features

- ✅ Predict borrower **default risk** (Low / Medium / High)
- ✅ Predict loan **grade** (A / B / C)
- ✅ Combined final decision using model fusion logic
- ✅ Real-time **loan risk simulation** using user-adjusted input
- ✅ **Snowflake integration** with RSA key-pair authentication
- ✅ Clean and interactive **Flask web interface**
- ✅ Secure and scalable architecture with pre-trained models

---

## 🧠 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML, CSS, Bootstrap              |
| Backend    | Flask (Python)                    |
| ML Models  | Random Forest & Gradient Boosting |
| Data       | Lending Club loan dataset         |
| Database   | Snowflake (secure insert)         |

---

## 🏗️ Project Structure

lend-wise/
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── loan_one_model.pkl # Risk model
├── loan_second_model.joblib # Grade model
├── loan_one_model_scaler.pkl # Scaler for risk model
├── loan_second_model_scaler.joblib # Scaler for grade model
├── templates/
│ ├── index.html # User input form
│ └── result.html # Prediction results page
├── static/ # (Optional) CSS, JS, assets
├── rsa_key.pem # 🔒 Private key (DO NOT COMMIT)
├── .gitignore # Files to exclude from GitHub
└── README.md # This file

## 📈 How It Works

1. **User Input:** Borrowers enter details like loan amount, credit score, income, etc.
2. **Risk Prediction:** A Random Forest Classifier predicts risk level.
3. **Grade Prediction:** A Gradient Boosting model assigns loan grade.
4. **Decision Engine:** Final result based on risk + grade logic.
5. **Snowflake Storage:** Results are securely stored for record-keeping.

---

## 🧪 Use Cases

- Check borrower eligibility instantly.
- Adjust inputs to simulate changes in risk.
- Guide risk-based loan approval workflow.
- Provide transparency for both lenders and borrowers.

---

## ⚙️ Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/lend-wise.git
cd lend-wise

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the Flask app
python app.py
