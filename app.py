import streamlit as st
import joblib
import pandas as pd
import base64
from sklearn.preprocessing import LabelEncoder

# Load the trained model
knn_model = joblib.load("knn_model.pkl")

# Load the alert sound file
alert_sound = open('alert.mp3', 'rb').read()
alert_sound_encoded = base64.b64encode(alert_sound).decode('ascii')

# Payment Details Input Form
st.title("Online Payment Fraud Detection")

st.image("image1.png", use_column_width=True)

st.header("Payment Details")

payment_type = st.selectbox("Payment Type", ["CASH_OUT", "TRANSFER", "PAYMENT", "CASH_IN", "DEBIT"])
amount = st.number_input("Amount Available")
old_balance_origin = st.number_input("Old Balance of Origin Account")
new_balance_origin = st.number_input("New Balance of Origin Account")
old_balance_dest = st.number_input("Old Balance of Destination Account")
new_balance_dest = st.number_input("New Balance of Destination Account")

# Button to trigger prediction
if st.button("Predict"):
    # Convert input data to DataFrame
    input_data = {
        'type': [payment_type],
        'amount': [amount],
        'oldbalanceOrg': [old_balance_origin],
        'newbalanceOrig': [new_balance_origin],
        'oldbalanceDest': [old_balance_dest],
        'newbalanceDest': [new_balance_dest]
    }

    input_df = pd.DataFrame(input_data)

    # Convert 'type' column to numerical using Label Encoding
    le = LabelEncoder()
    input_df['type'] = le.fit_transform(input_df['type'])

    # Make predictions for the input data
    prediction = knn_model.predict(input_df)

    # Define the colors for the messages
    fraud_color = 'red'
    genuine_color = 'green'

    # Play alert sound if prediction is fraud
    if prediction[0] == 1:
        # Display the alert message
        message = "<h3><font color='{}'>!!! High Alert, Fraud Account Details...!!!</font></h3>".format(fraud_color)
        message += "<p><strong>Payment Type:</strong> {}</p>".format(payment_type)
        message += "<p><strong>Amount:</strong> {} thousand</p>".format(amount)
        message += "<p><strong>Old Balance of Origin Account:</strong> {}</p>".format(old_balance_origin)
        message += "<p><strong>New Balance of Origin Account:</strong> {}</p>".format(new_balance_origin)
        message += "<p><strong>Old Balance of Destination Account:</strong> {}</p>".format(old_balance_dest)
        message += "<p><strong>New Balance of Destination Account:</strong> {}</p>".format(new_balance_dest)
        message += "<p><font color='{}'>The payment is predicted to be fraudulent.</font></p>".format(fraud_color)
        # Embed the alert sound
        st.markdown(f'<audio src="data:audio/mp3;base64,{alert_sound_encoded}" autoplay controls>', unsafe_allow_html=True)
    else:
        # Display genuine message
        message = "<h3><font color='{}'>Payment Is Genuine</font></h3>".format(genuine_color)
        message += "<p><strong>Payment Type:</strong> {}</p>".format(payment_type)
        message += "<p><strong>Amount:</strong> {} thousand</p>".format(amount)
        message += "<p><strong>Old Balance of Origin Account:</strong> {}</p>".format(old_balance_origin)
        message += "<p><strong>New Balance of Origin Account:</strong> {}</p>".format(new_balance_origin)
        message += "<p><strong>Old Balance of Destination Account:</strong> {}</p>".format(old_balance_dest)
        message += "<p><strong>New Balance of Destination Account:</strong> {}</p>".format(new_balance_dest)
    # Display the message using HTML
    st.markdown(message, unsafe_allow_html=True)
