# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import roc_auc_score, classification_report

# # Load and explore data
# file_path = 'C:\\Users\\digan\\Desktop\\JP Morgan Chase & Co. Quantitative Research\\Task - 3\\Task 3 and 4_Loan_Data.csv'
# data = pd.read_csv(file_path)

# # Preview data
# print(data.head())

# # Preprocess data
# X = data.drop(columns=['customer_id', 'default'])
# y = data['default']

# # Encode categorical variables if any (here we have only numerical data)

# # Split data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# # Standardize features
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# # Initialize models
# models = {
#     'Logistic Regression': LogisticRegression(),
#     'Decision Tree': DecisionTreeClassifier(),
#     'Random Forest': RandomForestClassifier()
# }

# # Train and evaluate models
# for name, model in models.items():
#     model.fit(X_train_scaled, y_train)
#     y_pred = model.predict(X_test_scaled)
#     y_prob = model.predict_proba(X_test_scaled)[:, 1]  # Probability of default
    
#     print(f'\n{name} Model:')
#     print(f'ROC AUC Score: {roc_auc_score(y_test, y_prob)}')
#     print(classification_report(y_test, y_pred))

# # Calculate expected loss
# def calculate_expected_loss(probability_of_default, loan_amount_outstanding, recovery_rate=0.10):
#     loss_given_default = (1 - recovery_rate)  # Loss given default
#     expected_loss = probability_of_default * loan_amount_outstanding * loss_given_default
#     return expected_loss

# # Example usage
# example_loan_data = pd.DataFrame({
#     'credit_lines_outstanding': [0],
#     'loan_amt_outstanding': [5221.545193],
#     'total_debt_outstanding': [3915.471226],
#     'income': [78039.38546],
#     'years_employed': [5],
#     'fico_score': [605]
# })

# example_loan_scaled = scaler.transform(example_loan_data)
# predicted_prob = models['Random Forest'].predict_proba(example_loan_scaled)[:, 1]
# expected_loss = calculate_expected_loss(predicted_prob[0], example_loan_data['loan_amt_outstanding'][0])
# print(f'\nExpected Loss for Example Loan: ${expected_loss:.2f}')


from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import pandas as pd

# Read in loan data from a CSV file
df = pd.read_csv('C:\\Users\\digan\\Desktop\\JP Morgan Chase & Co. Quantitative Research\\Task - 3\\Task 3 and 4_Loan_Data.csv')

# Define the variable features
features = ['credit_lines_outstanding', 'debt_to_income', 'payment_to_income', 'years_employed', 'fico_score']

# Calculate the payment_to_income ratio
df['payment_to_income'] = df['loan_amt_outstanding'] / df['income']
    
# Calculate the debt_to_income ratio
df['debt_to_income'] = df['total_debt_outstanding'] / df['income']

# Define the Logistic Regression model
clf = LogisticRegression(random_state=0, solver='liblinear', tol=1e-5, max_iter=10000)

# Fit the model
clf.fit(df[features], df['default'])

# Print model coefficients and intercept
print("Model Coefficients:", clf.coef_)
print("Model Intercept:", clf.intercept_)

# Predict using the model
y_pred = clf.predict(df[features])

# Calculate and print evaluation metrics
fpr, tpr, thresholds = metrics.roc_curve(df['default'], y_pred)
print("Misclassification Rate:", (1.0 * (abs(df['default'] - y_pred)).sum()) / len(df))
print("ROC AUC Score:", metrics.auc(fpr, tpr))
