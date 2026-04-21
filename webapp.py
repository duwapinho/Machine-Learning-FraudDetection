import streamlit as st
import joblib
import pandas as pd

model = joblib.load('fraud_pipeline.pkl')
st.title('Fraud Detector')
st.write('Enter transaction details below to check if its fraudulent.')
col1, col2 = st.columns(2)  #spliting page on two columns.
with col1:
    transaction_type = st.selectbox('Transaction Type', ['CASH_OUT', 'TRANSFER', 'CASH_IN', 'PAYMENT', 'DEBIT']) #creating box where i can choose type of transactions
    amount = st.number_input('Amount', min_value=0.0, value=10000.0,step=1.0) #value of transaction.
with col2:
    oldbalanceOrg = st.number_input('Balance before transaction (Sender)', min_value=0.0, value=0.0, step=1.0)
    newbalanceOrig = st.number_input('Balance after transaction (Sender)', min_value=0.0, value=0.0,step=1.0)
    oldbalanceDest = st.number_input('Balance before transcation (Receiver)', min_value=0.0, value=0.0,step=1.0)
    newbalanceDest = st.number_input('Balance after transaction (Receiver)', min_value=0.0, value=0.0,step=1.0)
if st.button(' Check Transaction'):
    input_data = pd.DataFrame([{
        'type': transaction_type,
        'amount': amount,
        'oldbalanceOrg': oldbalanceOrg,
        'newbalanceOrig': newbalanceOrig,
        'oldbalanceDest': oldbalanceDest,
        'newbalanceDest': newbalanceDest}]) #taking typed data into data frame to be compailant with model
    prediction = model.predict(input_data)[0] #feeding model
    fraud_probability = model.predict_proba(input_data)[0][1]  #returns
    st.divider()  #separating sections.
    if prediction == 1:
        st.error(f' FRAUD DETECTED! Fraud probability: {fraud_probability:.2%}') #showing red error message
    else:
        st.success(f'Looks Legit. Fraud probability: {fraud_probability:.2%}') #showing green success message
    st.progress(float(fraud_probability)) #visual bar dependent on fraud probability, more  % = bar is more loaded.