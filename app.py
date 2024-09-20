import streamlit as st
import pandas as pd
import json
import random
from datetime import datetime, timedelta
import calendar
import io
import base64

# --- Setup Placeholder Data Structures ---
clients = []
properties = []
cleaning_checklists = {}
sales_call_scripts = {}
invoices = {}
staff = {}
tasks = {}

# Generate 25 example clients with multiple properties
def generate_example_clients(num_clients=25):
    first_names = ["John", "Jane", "Alex", "Emily", "Chris", "Taylor", "Oliver", "Sophia", "Liam", "Mia"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Lee", "Martinez", "Rodriguez", "Clark"]
    street_names = ["Main", "Maple", "Oak", "Pine", "Elm", "Cedar", "Walnut", "Sunset", "Riverside", "Hillside"]
    
    for i in range(num_clients):
        client_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        contact = f"{client_name.replace(' ', '').lower()}{i}@example.com"
        phone = f"+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}"
        preferred_contact = random.choice(['Email', 'Phone', 'SMS'])
        service_tier = random.choice(['Basic', 'Standard', 'Premium'])
        account_status = random.choice(['Active', 'Pending', 'Inactive'])
        registration_date = (datetime.today() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        annual_spend = random.randint(500, 5000)
        
        # Add example client
        clients.append({
            'name': client_name,
            'contact': contact,
            'phone': phone,
            'preferred_contact': preferred_contact,
            'service_tier': service_tier,
            'account_status': account_status,
            'registration_date': registration_date,
            'annual_spend': annual_spend
        })

        # Add multiple properties for each client
        num_properties = random.randint(1, 3)
        for j in range(num_properties):
            prop_address = f"{random.randint(1, 999)} {random.choice(street_names)} St, Unit {j+1}"
            size = random.randint(1000, 5000)  # Square feet
            prop_type = random.choice(['Residential', 'Commercial'])
            cleaning_freq = random.choice(['Weekly', 'Bi-weekly', 'Monthly'])
            cleaning_notes = f"Specific instructions for Unit {j+1}"
            last_cleaned = (datetime.today() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')

            properties.append({
                'client': client_name,
                'address': prop_address,
                'size': size,
                'type': prop_type,
                'cleaning_freq': cleaning_freq,
                'last_cleaned': last_cleaned,
                'cleaning_notes': cleaning_notes,
                'photos': None  # Placeholder for property photos
            })

# Load and save data (for persistence)
def load_data():
    try:
        with open('crm_data.json', 'r') as f:
            data = json.load(f)
            global clients, properties, cleaning_checklists, sales_call_scripts, invoices, staff, tasks
            clients = data['clients']
            properties = data['properties']
            cleaning_checklists = data['cleaning_checklists']
            sales_call_scripts = data['sales_call_scripts']
            invoices = data['invoices']
            staff = data['staff']
            tasks = data['tasks']
    except FileNotFoundError:
        pass

def save_data():
    data = {
        'clients': clients,
        'properties': properties,
        'cleaning_checklists': cleaning_checklists,
        'sales_call_scripts': sales_call_scripts,
        'invoices': invoices,
        'staff': staff,
        'tasks': tasks
    }
    with open('crm_data.json', 'w') as f:
        json.dump(data, f)

# Function to display data in a more visible format
def display_data():
    st.subheader("Client Data")
    if clients:
        df_clients = pd.DataFrame(clients)
        st.dataframe(df_clients)
    else:
        st.write("No clients available.")
    
    st.subheader("Property Data")
    if properties:
        df_properties = pd.DataFrame(properties)
        st.dataframe(df_properties)
    else:
        st.write("No properties available.")

    st.subheader("Invoice Data")
    if invoices:
        df_invoices = pd.DataFrame(invoices).T
        st.dataframe(df_invoices)
    else:
        st.write("No invoices available.")

    st.subheader("Staff Data")
    if staff:
        df_staff = pd.DataFrame(staff).T
        st.dataframe(df_staff)
    else:
        st.write("No staff data available.")

# --- Main App Execution ---
load_data()

st.title("Cleaning Company CRM System")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ['Dashboard', 'Clients', 'Properties', 'Tasks', 'Invoices', 'Staff', 'Add Client', 'Add Property'])

# Page content based on selection
if option == 'Dashboard':
    st.header("Dashboard")
    st.write("Summary of the company's performance:")
    total_clients = len(clients)
    total_properties = len(properties)
    total_invoices = len(invoices)
    st.write(f"Total Clients: {total_clients}")
    st.write(f"Total Properties: {total_properties}")
    st.write(f"Total Invoices: {total_invoices}")
    display_data()
elif option == 'Clients':
    st.header("Client List")
    display_data()
elif option == 'Properties':
    st.header("Properties List")
    display_data()
elif option == 'Tasks':
    manage_tasks()
elif option == 'Invoices':
    manage_invoices()
elif option == 'Staff':
    manage_staff()
elif option == 'Add Client':
    add_client()
elif option == 'Add Property':
    add_property()
