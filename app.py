import streamlit as st
import requests

# Define the base URL for your Flask application
BASE_URL = 'https://session.loca.lt'

# Streamlit UI code
st.title('Order Metrics Dashboard')

# General Median Visits
st.subheader('General Median Visits')
general_visits_url = f'{BASE_URL}/metrics/orders/General_Median_Visits'
general_visits_response = requests.get(general_visits_url)
if general_visits_response.status_code == 200:
    general_visits_result = general_visits_response.json()
    st.write(f"Median Visits Before Order: {general_visits_result}")
else:
    st.write('Error retrieving general median visits.')

# General Duration Median
st.subheader('General Duration Median')
general_duration_url = f'{BASE_URL}/metrics/orders/General_Duration_Median'
general_duration_response = requests.get(general_duration_url)
if general_duration_response.status_code == 200:
    general_duration_result = general_duration_response.json()
    st.write(f"Median Session Duration: {general_duration_result} minutes")
else:
    st.write('Error retrieving general duration median.')

# Customer Duration Median
st.subheader('Customer Duration Median')
customer_id = st.text_input('Enter Customer ID:')
if customer_id:
    customer_duration_url = f'{BASE_URL}/metrics/orders/Customer_Duration_Median/{customer_id}'
    customer_duration_response = requests.get(customer_duration_url)
    if customer_duration_response.status_code == 200:
        customer_duration_result = customer_duration_response.json()
        st.success(f"Median Session Duration for Customer {customer_id}: {customer_duration_result} minutes")
    else:
        st.write('Error retrieving customer duration median.')


# Customer Session Nb
st.subheader('Customer Session Nb')
customer_id2 = st.text_input('Enter Customer ID:', key='customer_id2')
if customer_id2:
    customer_session_nb_url = f'{BASE_URL}/metrics/orders/Customer_session_nb/{customer_id2}'
    customer_session_nb_response = requests.get(customer_session_nb_url)
    if customer_session_nb_response.status_code == 200:
        customer_session_nb_result = customer_session_nb_response.json()
        st.success(f"Number of Sessions for Customer {customer_id2}: {customer_session_nb_result}")
    else:
        st.write('Error retrieving customer session count.')
