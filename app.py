import streamlit as st
import joblib
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Load the trained model
knn_model = joblib.load("knn_model.pkl")

# Load the alert sound file
alert_sound = open('alert.mp3', 'rb').read()
alert_sound_encoded = base64.b64encode(alert_sound).decode('ascii')

# Define correct username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "password"  # Change this to your desired password

# Function to authenticate user
def authenticate(username, password):
    return username == CORRECT_USERNAME and password == CORRECT_PASSWORD

# Payment Details Input Form
st.title("Online Payment Fraud Detection")
st.image("image1.png")

# Sidebar for login/logout
st.sidebar.header("Authentication")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

# Check if the user is authenticated
session_state = st.session_state
if "authenticated" not in session_state:
    session_state.authenticated = False

if st.sidebar.button("Login"):
    if authenticate(username, password):
        session_state.authenticated = True
    else:
        st.sidebar.error("Incorrect username or password")

if session_state.authenticated:
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        session_state.authenticated = False
        st.sidebar.info("Logged out")
else:
    st.sidebar.warning("Please login to continue.")

if session_state.authenticated:
    payment_type = st.selectbox("Payment Type", ["CASH_OUT", "TRANSFER", "PAYMENT", "CASH_IN", "DEBIT"])
    amount = st.number_input("Amount Available")
    old_balance_origin = st.number_input("Old Balance of Origin Account")
    new_balance_origin = st.number_input("New Balance of Origin Account")
    old_balance_dest = st.number_input("Old Balance of Destination Account")
    new_balance_dest = st.number_input("New Balance of Destination Account")

    # Visualizations
    st.markdown("### Data Visualization")
    st.markdown("#### 1. Distribution of Payment Types")
    payment_types = ['CASH_OUT', 'TRANSFER', 'PAYMENT', 'CASH_IN', 'DEBIT']
    payment_counts = [1000, 2000, 1500, 1800, 1200]  # Example data, replace with your actual data
    plt.bar(payment_types, payment_counts)
    plt.xlabel('Payment Type')
    plt.ylabel('Frequency')
    st.pyplot()

    st.markdown("#### 2. Scatter Plot: Old Balance Origin vs. New Balance Origin")
    df = pd.DataFrame({
        'Old Balance Origin': [old_balance_origin],
        'New Balance Origin': [new_balance_origin]
    })
    sns.scatterplot(data=df, x='Old Balance Origin', y='New Balance Origin')
    st.pyplot()

    st.markdown("#### 3. Distribution of Amount")
    amounts = [100, 200, 300, 400, 500]  # Example data, replace with your actual data
    plt.hist(amounts, bins=5)
    plt.xlabel('Amount')
    plt.ylabel('Frequency')
    st.pyplot()

    st.markdown("#### 4. Balance Change Comparison")
    balance_changes = [old_balance_origin - new_balance_origin, old_balance_dest - new_balance_dest]
    labels = ['Origin Account', 'Destination Account']
    plt.bar(labels, balance_changes)
    plt.xlabel('Account')
    plt.ylabel('Balance Change')
    st.pyplot()

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
            message += "<p><strong>Old Balance of Origin Account:</strong> {} lakhs</p>".format(old_balance_origin)
            message += "<p><strong>New Balance of Origin Account:</strong> {} lakhs</p>".format(new_balance_origin)
            message += "<p><strong>Old Balance of Destination Account:</strong> {} thousand</p>".format(old_balance_dest)
            message += "<p><strong>New Balance of Destination Account:</strong> {} thousand</p>".format(new_balance_dest)
            message += "<p><font color='{}'>The payment is predicted to be fraudulent.</font></p>".format(fraud_color)
            # Embed the alert sound
            st.markdown(f'<audio src="data:audio/mp3;base64,{alert_sound_encoded}" autoplay controls>', unsafe_allow_html=True)
        else:
            # Display genuine message
            message = "<h3><font color='{}'>Payment Is Genuine</font></h3>".format(genuine_color)
            message += "<p><strong>Payment Type:</strong> {}</p>".format(payment_type)
            message += "<p><strong>Amount:</strong> {} thousand</p>".format(amount)
            message += "<p><strong>Old Balance of Origin Account:</strong> {} lakhs</p>".format(old_balance_origin)
            message += "<p><strong>New Balance of Origin Account:</strong> {} lakhs</p>".format(new_balance_origin)
            message += "<p><strong>Old Balance of Destination Account:</strong> {} thousand</p>".format(old_balance_dest)
            message += "<p><strong>New Balance of Destination Account:</strong> {} thousand</p>".format(new_balance_dest)
        # Display the message using HTML
        st.markdown(message, unsafe_allow_html=True)
