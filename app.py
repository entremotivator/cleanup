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

# Function to add a new client manually
def add_client():
    with st.form("Add a new client"):
        name = st.text_input("Client Name")
        contact = st.text_input("Client Contact Info (Email)")
        phone = st.text_input("Client Phone")
        preferred_contact = st.selectbox("Preferred Contact Method", ['Email', 'Phone', 'SMS'])
        service_tier = st.selectbox("Service Tier", ['Basic', 'Standard', 'Premium'])
        account_status = st.selectbox("Account Status", ['Active', 'Pending', 'Inactive'])
        registration_date = st.date_input("Registration Date", value=datetime.today())
        annual_spend = st.number_input("Annual Spend", min_value=0, step=100)
        if st.form_submit_button("Add Client"):
            clients.append({
                'name': name,
                'contact': contact,
                'phone': phone,
                'preferred_contact': preferred_contact,
                'service_tier': service_tier,
                'account_status': account_status,
                'registration_date': registration_date.strftime('%Y-%m-%d'),
                'annual_spend': annual_spend
            })
            save_data()

# Function to add a new property manually
def add_property():
    with st.form("Add a new property"):
        client_name = st.selectbox("Client", [client['name'] for client in clients])
        property_address = st.text_input("Property Address")
        size = st.number_input("Property Size (sq. ft.)", min_value=500, step=50)
        prop_type = st.selectbox("Property Type", ['Residential', 'Commercial'])
        cleaning_freq = st.selectbox("Cleaning Frequency", ['Weekly', 'Bi-weekly', 'Monthly'])
        cleaning_notes = st.text_area("Cleaning Notes (specific instructions)")
        property_photos = st.file_uploader("Upload Property Photos", accept_multiple_files=True)
        if st.form_submit_button("Add Property"):
            properties.append({
                'client': client_name,
                'address': property_address,
                'size': size,
                'type': prop_type,
                'cleaning_freq': cleaning_freq,
                'last_cleaned': (datetime.today() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'cleaning_notes': cleaning_notes,
                'photos': property_photos  # Store photo file references
            })
            save_data()

# Function to add and manage cleaning tasks
def manage_tasks():
    st.subheader("Task Scheduler")
    with st.form("Assign a Cleaning Task"):
        property_address = st.selectbox("Property", [prop['address'] for prop in properties])
        assigned_staff = st.selectbox("Assign to Staff", [member['name'] for member in staff])
        task_date = st.date_input("Task Date")
        task_notes = st.text_area("Task Notes")
        if st.form_submit_button("Assign Task"):
            tasks[property_address] = {
                'staff': assigned_staff,
                'date': task_date,
                'status': 'Assigned',
                'notes': task_notes
            }
            save_data()
    # Display tasks
    st.write("Assigned Tasks:")
    for property_address, task in tasks.items():
        st.write(f"Property: {property_address}, Assigned to: {task['staff']}, Date: {task['date']}, Status: {task['status']}, Notes: {task['notes']}")

# Manage staff
def manage_staff():
    st.subheader("Manage Cleaning Staff")
    with st.form("Add Staff Member"):
        name = st.text_input("Staff Name")
        contact = st.text_input("Staff Contact Info (Email/Phone)")
        role = st.selectbox("Staff Role", ["Cleaner", "Supervisor", "Manager"])
        availability = st.selectbox("Availability", ["Full-time", "Part-time", "On-call"])
        if st.form_submit_button("Add Staff"):
            staff[name] = {
                'contact': contact,
                'role': role,
                'availability': availability
            }
            save_data()

    st.write("Staff Members:")
    for name, info in staff.items():
        st.write(f"{name} - Role: {info['role']}, Availability: {info['availability']}, Contact: {info['contact']}")

# Manage invoices and payments
def manage_invoices():
    st.subheader("Manage Invoices")
    with st.form("Generate Invoice"):
        client_name = st.selectbox("Select Client", [client['name'] for client in clients])
        service_date = st.date_input("Service Date")
        amount_due = st.number_input("Amount Due", min_value=0.0, step=0.01)
        due_date = st.date_input("Due Date")
        invoice_notes = st.text_area("Invoice Notes")
        if st.form_submit_button("Generate Invoice"):
            invoices[client_name] = {
                'service_date': service_date.strftime('%Y-%m-%d'),
                'amount_due': amount_due,
                'due_date': due_date.strftime('%Y-%m-%d'),
                'status': 'Pending',
                'notes': invoice_notes
            }
            save_data()
    
    # Display invoices
    st.write("Invoices:")
    for client, invoice in invoices.items():
        st.write(f"Client: {client}, Amount Due: ${invoice['amount_due']}, Due Date: {invoice['due_date']}, Status: {invoice['status']}")

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
elif option == 'Clients':
    st.header("Client List")
    for client in clients:
        st.write(client)
elif option == 'Properties':
    st.header("Properties List")
    for property in properties:
        st.write(property)
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

    clients, properties, tasks, staff, invoices = load_data()
    render_ui(clients, properties, tasks, staff, invoices)
    save_data(clients, properties, tasks, staff, invoices)
