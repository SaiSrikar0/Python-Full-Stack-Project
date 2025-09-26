import streamlit as st
import requests
import pandas as pd

# API base URL
API_URL = "http://localhost:8080"

# Set page configuration and dark theme
st.set_page_config(
    page_title="ProjectDock",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🚀",
)

# Apply permanent dark theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .st-bx {
        background-color: #252526;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FF4B4B !important;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    .stTextInput>div>div>input {
        background-color: #252526;
        color: white !important;
        border: 1px solid #FF4B4B;
    }
    .stTextArea>div>div>textarea {
        background-color: #252526;
        color: white !important;
        border: 1px solid #FF4B4B;
    }
    .stSelectbox>div>div>select {
        background-color: #252526;
        color: white !important;
        border: 1px solid #FF4B4B;
    }
    .stMarkdown, .stText {
        color: #FFFFFF !important;
    }
    .stDataFrame {
        background-color: #252526;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
st.sidebar.title("ProjectDock")
st.sidebar.markdown("A Project Management System")

# Navigation
page = st.sidebar.selectbox("Navigate", ["Projects", "Tasks", "Users"])

# --- Helper Functions for API calls ---
def handle_response(response, success_message):
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("success"):
                st.success(success_message)
                return result.get("data", [])
            else:
                st.error(f"Error: {result.get('message', 'Unknown error')}")
                return []
        except ValueError:
            st.error("Error: Invalid response from server")
            return []
    else:
        try:
            error_detail = response.json().get('detail', f'HTTP {response.status_code} Error')
        except ValueError:
            error_detail = f"HTTP {response.status_code} Error - {response.text[:100]}"
        st.error(f"Error: {error_detail}")
        return []

# --- Projects Page ---
if page == "Projects":
    st.header("Projects")

    # Fetch and display projects
    st.subheader("All Projects")
    projects_response = requests.get(f"{API_URL}/projects")
    if projects_response.status_code == 200:
        projects = projects_response.json().get("data", [])
        if projects:
            df = pd.DataFrame(projects)
            st.dataframe(df)
        else:
            st.info("No projects found.")
    else:
        st.error("Could not fetch projects.")

    # Create a new project
    st.subheader("Create New Project")
    
    # Fetch available users for the dropdown
    users_response = requests.get(f"{API_URL}/users")
    available_users = []
    if users_response.status_code == 200:
        users_data = users_response.json().get("data", [])
        available_users = [(user["id"], f"{user['name']} ({user['email']})") for user in users_data]
    
    with st.form("new_project_form"):
        name = st.text_input("Project Name")
        description = st.text_area("Description")
        
        if available_users:
            owner_option = st.selectbox(
                "Project Owner", 
                options=[user[0] for user in available_users],
                format_func=lambda x: next(user[1] for user in available_users if user[0] == x)
            )
            owner_id = owner_option
        else:
            st.warning("No users found. Please create a user first.")
            owner_id = st.text_input("Owner ID (UUID)")
            
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        status = st.selectbox("Status", ["pending", "ongoing", "completed"])
        submitted = st.form_submit_button("Create Project")

        if submitted and name and owner_id:
            project_data = {
                "name": name,
                "description": description,
                "owner_id": owner_id,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "status": status,
            }
            response = requests.post(f"{API_URL}/projects", json=project_data)
            handle_response(response, "Project created successfully!")
        elif submitted:
            st.error("Please fill in all required fields.")

# --- Tasks Page ---
elif page == "Tasks":
    st.header("Tasks")

    # Fetch and display tasks
    st.subheader("All Tasks")
    tasks_response = requests.get(f"{API_URL}/tasks")
    if tasks_response.status_code == 200:
        tasks = tasks_response.json().get("data", [])
        if tasks:
            df = pd.DataFrame(tasks)
            st.dataframe(df)
        else:
            st.info("No tasks found.")
    else:
        st.error("Could not fetch tasks.")

    # Create a new task
    st.subheader("Create New Task")
    
    # Fetch available projects and users for dropdowns
    projects_resp = requests.get(f"{API_URL}/projects")
    users_resp = requests.get(f"{API_URL}/users")
    
    available_projects = []
    available_users = []
    
    if projects_resp.status_code == 200:
        projects_data = projects_resp.json().get("data", [])
        available_projects = [(proj["id"], proj["name"]) for proj in projects_data]
    
    if users_resp.status_code == 200:
        users_data = users_resp.json().get("data", [])
        available_users = [(user["id"], f"{user['name']} ({user['email']})") for user in users_data]
    
    with st.form("new_task_form"):
        if available_projects:
            project_option = st.selectbox(
                "Project", 
                options=[proj[0] for proj in available_projects],
                format_func=lambda x: next(proj[1] for proj in available_projects if proj[0] == x)
            )
            project_id = project_option
        else:
            st.warning("No projects found. Please create a project first.")
            project_id = st.text_input("Project ID (UUID)")
        
        title = st.text_input("Task Title")
        description = st.text_area("Description")
        
        if available_users:
            user_option = st.selectbox(
                "Assigned to", 
                options=[user[0] for user in available_users],
                format_func=lambda x: next(user[1] for user in available_users if user[0] == x)
            )
            assigned_to = user_option
        else:
            st.warning("No users found. Please create a user first.")
            assigned_to = st.text_input("Assigned to (User ID)")
        
        due_date = st.date_input("Due Date")
        status = st.selectbox("Status", ["pending", "in-progress", "completed"])
        submitted = st.form_submit_button("Create Task")

        if submitted and title and project_id and assigned_to:
            task_data = {
                "project_id": project_id,
                "title": title,
                "description": description,
                "assigned_to": assigned_to,
                "due_date": str(due_date),
                "status": status,
            }
            response = requests.post(f"{API_URL}/tasks", json=task_data)
            handle_response(response, "Task created successfully!")
        elif submitted:
            st.error("Please fill in all required fields.")

# --- Users Page ---
elif page == "Users":
    st.header("Users")

    # Fetch and display users
    st.subheader("All Users")
    users_response = requests.get(f"{API_URL}/users")
    if users_response.status_code == 200:
        users = users_response.json().get("data", [])
        if users:
            df = pd.DataFrame(users)
            st.dataframe(df)
        else:
            st.info("No users found.")
    else:
        st.error("Could not fetch users.")

    # Create a new user
    st.subheader("Create New User")
    with st.form("new_user_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "member"])
        submitted = st.form_submit_button("Create User")

        if submitted:
            user_data = {
                "name": name,
                "email": email,
                "password_hash": password,  # In a real app, hash this properly
                "role": role,
            }
            response = requests.post(f"{API_URL}/users", json=user_data)
            handle_response(response, "User created successfully!")