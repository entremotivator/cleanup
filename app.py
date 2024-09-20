import streamlit as st
import pandas as pd
import json
from datetime import datetime

# File paths for saving data
CLIENTS_FILE = "clients.json"
PROPERTIES_FILE = "properties.json"
TASKS_FILE = "tasks.json"
STAFF_FILE = "staff.json"
INVOICES_FILE = "invoices.json"

# Load data from JSON files
def load_data():
    try:
        with open(CLIENTS_FILE, 'r') as f:
            clients = json.load(f)
        with open(PROPERTIES_FILE, 'r') as f:
            properties = json.load(f)
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
        with open(STAFF_FILE, 'r') as f:
            staff = json.load(f)
        with open(INVOICES_FILE, 'r') as f:
            invoices = json.load(f)
    except FileNotFoundError:
        clients, properties, tasks, staff, invoices = [], [], [], [], []
    return clients, properties, tasks, staff, invoices

# Save data to JSON files
def save_data(clients, properties, tasks, staff, invoices):
    with open(CLIENTS_FILE, 'w') as f:
        json.dump(clients, f, indent=4)
    with open(PROPERTIES_FILE, 'w') as f:
        json.dump(properties, f, indent=4)
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
    with open(STAFF_FILE, 'w') as f:
        json.dump(staff, f, indent=4)
    with open(INVOICES_FILE, 'w') as f:
        json.dump(invoices, f, indent=4)

# Add new client
def add_client(clients):
    st.subheader("Add New Client")
    with st.form("add_client_form"):
        name = st.text_input("Client Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        address = st.text_area("Address")
        service_tier = st.selectbox("Service Tier", ["Basic", "Standard", "Premium"])
        notes = st.text_area("Notes (optional)")
        submit = st.form_submit_button("Add Client")
    
    if submit:
        client = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "service_tier": service_tier,
            "notes": notes
        }
        clients.append(client)
        st.success(f"Client {name} added successfully!")

# Add new property
def add_property(properties):
    st.subheader("Add New Property")
    with st.form("add_property_form"):
        client_name = st.text_input("Client Name")
        address = st.text_area("Property Address")
        cleaning_frequency = st.selectbox("Cleaning Frequency", ["Daily", "Weekly", "Monthly"])
        notes = st.text_area("Notes (optional)")
        submit = st.form_submit_button("Add Property")

    if submit:
        property_ = {
            "client_name": client_name,
            "address": address,
            "cleaning_frequency": cleaning_frequency,
            "notes": notes
        }
        properties.append(property_)
        st.success(f"Property for client {client_name} added successfully!")

# Manage tasks
def manage_tasks(tasks):
    st.subheader("Task Management")
    with st.form("add_task_form"):
        task_name = st.text_input("Task Name")
        client_name = st.text_input("Client Name")
        property_address = st.text_area("Property Address")
        staff_assigned = st.text_input("Assigned Staff")
        deadline = st.date_input("Deadline")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
        submit = st.form_submit_button("Add Task")

    if submit:
        task = {
            "task_name": task_name,
            "client_name": client_name,
            "property_address": property_address,
            "staff_assigned": staff_assigned,
            "deadline": deadline.strftime("%Y-%m-%d"),
            "priority": priority,
            "status": status
        }
        tasks.append(task)
        st.success(f"Task '{task_name}' added successfully!")

    # Display tasks
    st.subheader("Current Tasks")
    df_tasks = pd.DataFrame(tasks)
    st.dataframe(df_tasks)

# Manage staff
def manage_staff(staff):
    st.subheader("Staff Management")
    with st.form("add_staff_form"):
        name = st.text_input("Staff Name")
        role = st.selectbox("Role", ["Cleaner", "Supervisor", "Manager"])
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        schedule = st.text_area("Work Schedule")
        submit = st.form_submit_button("Add Staff")

    if submit:
        staff_member = {
            "name": name,
            "role": role,
            "phone": phone,
            "email": email,
            "schedule": schedule
        }
        staff.append(staff_member)
        st.success(f"Staff member {name} added successfully!")

    # Display staff
    st.subheader("Current Staff")
    df_staff = pd.DataFrame(staff)
    st.dataframe(df_staff)

# Manage invoices and payments
def manage_invoices(invoices):
    st.subheader("Invoices and Payments")
    with st.form("add_invoice_form"):
        client_name = st.text_input("Client Name")
        amount_due = st.number_input("Amount Due", min_value=0.0, format="%.2f")
        due_date = st.date_input("Due Date")
        status = st.selectbox("Status", ["Unpaid", "Paid"])
        submit = st.form_submit_button("Generate Invoice")

    if submit:
        invoice = {
            "client_name": client_name,
            "amount_due": amount_due,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "status": status
        }
        invoices.append(invoice)
        st.success(f"Invoice for client {client_name} generated successfully!")

    # Display invoices
    st.subheader("Invoice List")
    df_invoices = pd.DataFrame(invoices)
    st.dataframe(df_invoices)

# Feedback and Ratings (New Feature)
def client_feedback():
    st.subheader("Client Feedback and Ratings")
    with st.form("feedback_form"):
        client_name = st.text_input("Client Name")
        rating = st.slider("Rating", 1, 5)
        feedback = st.text_area("Feedback")
        submit = st.form_submit_button("Submit Feedback")
        
    if submit:
        st.success(f"Thank you, {client_name}, for your feedback!")

# UI Rendering and Menu Options
def render_ui(clients, properties, tasks, staff, invoices):
    st.title("Cleaning Company CRM")
    st.sidebar.header("Navigation")
    options = st.sidebar.selectbox("Select a page", [
        "View Clients", "Add Client", "View Properties", "Add Property", 
        "Manage Tasks", "Manage Staff", "Invoices and Payments", "Client Feedback"
    ])
    
    if options == "View Clients":
        st.subheader("Client List")
        df_clients = pd.DataFrame(clients)
        st.dataframe(df_clients)

    elif options == "Add Client":
        add_client(clients)

    elif options == "View Properties":
        st.subheader("Property List")
        df_properties = pd.DataFrame(properties)
        st.dataframe(df_properties)

    elif options == "Add Property":
        add_property(properties)

    elif options == "Manage Tasks":
        manage_tasks(tasks)

    elif options == "Manage Staff":
        manage_staff(staff)

    elif options == "Invoices and Payments":
        manage_invoices(invoices)

    elif options == "Client Feedback":
        client_feedback()

if __name__ == "__main__":
    clients, properties, tasks, staff, invoices = load_data()
    render_ui(clients, properties, tasks, staff, invoices)
    save_data(clients, properties, tasks, staff, invoices)
