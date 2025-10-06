import streamlit as st
import requests
import pandas as pd
import os

# API base URL - Use environment variable for deployment flexibility
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Alternative: Use Streamlit secrets for deployment
try:
    API_URL = st.secrets["general"]["API_URL"]
except (KeyError, FileNotFoundError):
    # Fallback to environment variable or localhost
    API_URL = os.getenv("API_URL", "http://localhost:8000")

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

st.sidebar.markdown("---")
st.sidebar.markdown("### Features")
st.sidebar.markdown("✅ **Create** new records")
st.sidebar.markdown("👁️ **View** all data")
st.sidebar.markdown("✏️ **Edit** existing records")
st.sidebar.markdown("🗑️ **Delete** records")
st.sidebar.markdown("🎨 **Dark Theme** UI")

# Add connection status check
def check_api_connection():
    """Check if the API is accessible"""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def safe_api_request(url, method="GET", json_data=None, timeout=5):
    """Make API request with error handling"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=json_data, timeout=timeout)
        elif method == "PUT":
            response = requests.put(url, json=json_data, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, timeout=timeout)
        else:
            return None
        
        return response
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Could not connect to API: {API_URL}")
        st.info("💡 The backend API is not available. Please check if it's deployed and running.")
        return None

# Display API connection status
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 API Status")
if check_api_connection():
    st.sidebar.success("🟢 Connected")
    st.sidebar.caption(f"URL: {API_URL}")
else:
    st.sidebar.error("🔴 Not Connected")
    st.sidebar.caption(f"URL: {API_URL}")
    st.sidebar.warning("Deploy your backend API to enable full functionality")

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
    
    # Quick stats
    projects_response = safe_api_request(f"{API_URL}/projects")
    if projects_response and projects_response.status_code == 200:
        projects_data = projects_response.json().get("data", [])
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Projects", len(projects_data))
        with col2:
            pending_count = len([p for p in projects_data if p.get("status") == "pending"])
            st.metric("Pending", pending_count)
        with col3:
            ongoing_count = len([p for p in projects_data if p.get("status") == "ongoing"])
            st.metric("Ongoing", ongoing_count)
        with col4:
            completed_count = len([p for p in projects_data if p.get("status") == "completed"])
            st.metric("Completed", completed_count)
        st.markdown("---")
    else:
        # Show placeholder metrics when API is not available
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Projects", "—")
        with col2:
            st.metric("Pending", "—")
        with col3:
            st.metric("Ongoing", "—")
        with col4:
            st.metric("Completed", "—")
        st.markdown("---")
        st.warning("📊 **API Connection Required** - Deploy your backend to view real project data")

    # Fetch and display projects
    st.subheader("All Projects")
    projects_response = safe_api_request(f"{API_URL}/projects")
    if projects_response and projects_response.status_code == 200:
        projects = projects_response.json().get("data", [])
        if projects:
            df = pd.DataFrame(projects)
            st.dataframe(df, use_container_width=True)
            
            # Project Management Actions
            st.subheader("Manages Projects")
            if projects:
                project_to_manage = st.selectbox(
                    "Select Project to Edit/Delete:",
                    options=[proj["id"] for proj in projects],
                    format_func=lambda x: next(proj["name"] for proj in projects if proj["id"] == x)
                )
                
                selected_project = next(proj for proj in projects if proj["id"] == project_to_manage)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🗑️ Delete Project"):
                        delete_response = requests.delete(f"{API_URL}/projects/{project_to_manage}")
                        if delete_response.status_code == 200:
                            result = delete_response.json()
                            if result.get("success"):
                                st.success("Project deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"Error: {result.get('message')}")
                        else:
                            st.error("Failed to delete project")
                
                with col2:
                    if st.button("✏️ Edit Project"):
                        st.session_state.editing_project = project_to_manage
                
                # Edit Project Form
                if st.session_state.get("editing_project") == project_to_manage:
                    st.write("### Edit Project")
                    with st.form(f"edit_project_form_{project_to_manage}"):
                        # Fetch users for dropdown
                        users_resp = requests.get(f"{API_URL}/users")
                        available_users = []
                        if users_resp.status_code == 200:
                            users_data = users_resp.json().get("data", [])
                            available_users = [(user["id"], f"{user['name']} ({user['email']})") for user in users_data]
                        
                        edit_name = st.text_input("Project Name", value=selected_project["name"])
                        edit_description = st.text_area("Description", value=selected_project.get("description", ""))
                        
                        if available_users:
                            current_owner_index = next((i for i, user in enumerate(available_users) if user[0] == selected_project["owner_id"]), 0)
                            edit_owner = st.selectbox(
                                "Project Owner",
                                options=[user[0] for user in available_users],
                                format_func=lambda x: next(user[1] for user in available_users if user[0] == x),
                                index=current_owner_index
                            )
                        else:
                            edit_owner = st.text_input("Owner ID", value=selected_project["owner_id"])
                        
                        edit_start_date = st.date_input("Start Date", value=pd.to_datetime(selected_project["start_date"]).date())
                        edit_end_date = st.date_input("End Date", value=pd.to_datetime(selected_project["end_date"]).date())
                        
                        current_status = selected_project.get("status", "pending")
                        status_options = ["pending", "ongoing", "completed"]
                        current_status_index = status_options.index(current_status) if current_status in status_options else 0
                        edit_status = st.selectbox("Status", status_options, index=current_status_index)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            update_submitted = st.form_submit_button("💾 Update Project")
                        with col2:
                            cancel_edit = st.form_submit_button("❌ Cancel")
                        
                        if update_submitted:
                            update_data = {
                                "name": edit_name,
                                "description": edit_description,
                                "owner_id": edit_owner,
                                "start_date": str(edit_start_date),
                                "end_date": str(edit_end_date),
                                "status": edit_status
                            }
                            
                            update_response = requests.put(f"{API_URL}/projects/{project_to_manage}", json=update_data)
                            if update_response.status_code == 200:
                                result = update_response.json()
                                if result.get("success"):
                                    st.success("Project updated successfully!")
                                    st.session_state.editing_project = None
                                    st.rerun()
                                else:
                                    st.error(f"Error: {result.get('message')}")
                            else:
                                st.error("Failed to update project")
                        
                        if cancel_edit:
                            st.session_state.editing_project = None
                            st.rerun()
        else:
            st.info("No projects found.")
    else:
        # API not available - show helpful message
        st.info("🚀 **Welcome to ProjectDock!**")
        st.markdown("""
        **To view and manage projects:**
        1. Deploy your FastAPI backend
        2. Update the API_URL in your Streamlit Cloud app secrets
        3. Or run locally with both frontend and backend
        
        **Current API URL:** `{}`
        """.format(API_URL))
        
        st.markdown("---")
        st.subheader("📋 Sample Project Structure")
        sample_df = pd.DataFrame([
            {"Name": "ProjectDock Development", "Status": "ongoing", "Owner": "Developer", "Start Date": "2025-09-01"},
            {"Name": "Mobile App Design", "Status": "pending", "Owner": "Designer", "Start Date": "2025-10-01"}
        ])
        st.dataframe(sample_df, use_container_width=True)

    # Create a new project
    st.subheader("Create New Project")
    
    # Fetch available users for the dropdown
    users_response = safe_api_request(f"{API_URL}/users")
    available_users = []
    if users_response and users_response.status_code == 200:
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
        elif users_response:  # API responded but no users found
            st.warning("No users found. Please create a user first.")
            owner_id = st.text_input("Owner ID (UUID)")
        else:  # API not available
            st.info("💡 **Backend API Required** - Create forms will be enabled when your API is deployed.")
            owner_id = st.text_input("Owner ID (UUID)", disabled=True, help="Deploy backend API to enable this feature")
            
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
            if check_api_connection():
                response = safe_api_request(f"{API_URL}/projects", method="POST", json_data=project_data)
                if response:
                    handle_response(response, "Project created successfully!")
                else:
                    st.error("Failed to create project - API not available")
            else:
                st.error("❌ Cannot create project - Backend API is not available")
                st.info("💡 Deploy your FastAPI backend to enable project creation")
        elif submitted:
            st.error("Please fill in all required fields.")

# --- Tasks Page ---
elif page == "Tasks":
    st.header("Tasks")
    
    # Quick stats
    tasks_response = requests.get(f"{API_URL}/tasks")
    if tasks_response.status_code == 200:
        tasks_data = tasks_response.json().get("data", [])
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", len(tasks_data))
        with col2:
            pending_count = len([t for t in tasks_data if t.get("status") == "pending"])
            st.metric("Pending", pending_count)
        with col3:
            in_progress_count = len([t for t in tasks_data if t.get("status") == "in-progress"])
            st.metric("In Progress", in_progress_count)
        with col4:
            completed_count = len([t for t in tasks_data if t.get("status") == "completed"])
            st.metric("Completed", completed_count)
        st.markdown("---")

    # Fetch and display tasks
    st.subheader("All Tasks")
    tasks_response = requests.get(f"{API_URL}/tasks")
    if tasks_response.status_code == 200:
        tasks = tasks_response.json().get("data", [])
        if tasks:
            df = pd.DataFrame(tasks)
            st.dataframe(df, use_container_width=True)
            
            # Task Management Actions
            st.subheader("Manage Tasks")
            if tasks:
                task_to_manage = st.selectbox(
                    "Select Task to Edit/Delete:",
                    options=[task["id"] for task in tasks],
                    format_func=lambda x: next(task["title"] for task in tasks if task["id"] == x)
                )
                
                selected_task = next(task for task in tasks if task["id"] == task_to_manage)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🗑️ Delete Task"):
                        delete_response = requests.delete(f"{API_URL}/tasks/{task_to_manage}")
                        if delete_response.status_code == 200:
                            result = delete_response.json()
                            if result.get("success"):
                                st.success("Task deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"Error: {result.get('message')}")
                        else:
                            st.error("Failed to delete task")
                
                with col2:
                    if st.button("✏️ Edit Task"):
                        st.session_state.editing_task = task_to_manage
                
                # Edit Task Form
                if st.session_state.get("editing_task") == task_to_manage:
                    st.write("### Edit Task")
                    with st.form(f"edit_task_form_{task_to_manage}"):
                        # Fetch projects and users for dropdowns
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
                        
                        if available_projects:
                            current_project_index = next((i for i, proj in enumerate(available_projects) if proj[0] == selected_task["project_id"]), 0)
                            edit_project = st.selectbox(
                                "Project",
                                options=[proj[0] for proj in available_projects],
                                format_func=lambda x: next(proj[1] for proj in available_projects if proj[0] == x),
                                index=current_project_index
                            )
                        else:
                            edit_project = st.text_input("Project ID", value=selected_task["project_id"])
                        
                        edit_title = st.text_input("Task Title", value=selected_task["title"])
                        edit_description = st.text_area("Description", value=selected_task.get("description", ""))
                        
                        if available_users:
                            current_user_index = next((i for i, user in enumerate(available_users) if user[0] == selected_task["assigned_to"]), 0)
                            edit_assigned_to = st.selectbox(
                                "Assigned to",
                                options=[user[0] for user in available_users],
                                format_func=lambda x: next(user[1] for user in available_users if user[0] == x),
                                index=current_user_index
                            )
                        else:
                            edit_assigned_to = st.text_input("Assigned to", value=selected_task["assigned_to"])
                        
                        edit_due_date = st.date_input("Due Date", value=pd.to_datetime(selected_task["due_date"]).date())
                        
                        current_status = selected_task.get("status", "pending")
                        status_options = ["pending", "in-progress", "completed"]
                        current_status_index = status_options.index(current_status) if current_status in status_options else 0
                        edit_status = st.selectbox("Status", status_options, index=current_status_index)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            update_submitted = st.form_submit_button("💾 Update Task")
                        with col2:
                            cancel_edit = st.form_submit_button("❌ Cancel")
                        
                        if update_submitted:
                            update_data = {
                                "project_id": edit_project,
                                "title": edit_title,
                                "description": edit_description,
                                "assigned_to": edit_assigned_to,
                                "due_date": str(edit_due_date),
                                "status": edit_status
                            }
                            
                            update_response = requests.put(f"{API_URL}/tasks/{task_to_manage}", json=update_data)
                            if update_response.status_code == 200:
                                result = update_response.json()
                                if result.get("success"):
                                    st.success("Task updated successfully!")
                                    st.session_state.editing_task = None
                                    st.rerun()
                                else:
                                    st.error(f"Error: {result.get('message')}")
                            else:
                                st.error("Failed to update task")
                        
                        if cancel_edit:
                            st.session_state.editing_task = None
                            st.rerun()
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
    
    # Quick stats
    users_response = requests.get(f"{API_URL}/users")
    if users_response.status_code == 200:
        users_data = users_response.json().get("data", [])
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.metric("Total Users", len(users_data))
        with col2:
            admin_count = len([u for u in users_data if u.get("role") == "admin"])
            st.metric("Admins", admin_count)
        with col3:
            member_count = len([u for u in users_data if u.get("role") == "member"])
            st.metric("Members", member_count)
        st.markdown("---")

    # Fetch and display users
    st.subheader("All Users")
    users_response = requests.get(f"{API_URL}/users")
    if users_response.status_code == 200:
        users = users_response.json().get("data", [])
        if users:
            # Create a display DataFrame without password_hash
            display_users = [{k: v for k, v in user.items() if k != 'password_hash'} for user in users]
            df = pd.DataFrame(display_users)
            st.dataframe(df, use_container_width=True)
            
            # User Management Actions
            st.subheader("Manage Users")
            if users:
                user_to_manage = st.selectbox(
                    "Select User to Edit/Delete:",
                    options=[user["id"] for user in users],
                    format_func=lambda x: next(f"{user['name']} ({user['email']})" for user in users if user["id"] == x)
                )
                
                selected_user = next(user for user in users if user["id"] == user_to_manage)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🗑️ Delete User"):
                        delete_response = requests.delete(f"{API_URL}/users/{user_to_manage}")
                        if delete_response.status_code == 200:
                            result = delete_response.json()
                            if result.get("success"):
                                st.success("User deleted successfully!")
                                st.rerun()
                            else:
                                st.error(f"Error: {result.get('message')}")
                        else:
                            st.error("Failed to delete user")
                
                with col2:
                    if st.button("✏️ Edit User"):
                        st.session_state.editing_user = user_to_manage
                
                # Edit User Form
                if st.session_state.get("editing_user") == user_to_manage:
                    st.write("### Edit User")
                    with st.form(f"edit_user_form_{user_to_manage}"):
                        edit_name = st.text_input("Name", value=selected_user["name"])
                        edit_email = st.text_input("Email", value=selected_user["email"])
                        edit_password = st.text_input("New Password (leave blank to keep current)", type="password")
                        
                        current_role = selected_user.get("role", "member")
                        role_options = ["admin", "member"]
                        current_role_index = role_options.index(current_role) if current_role in role_options else 1
                        edit_role = st.selectbox("Role", role_options, index=current_role_index)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            update_submitted = st.form_submit_button("💾 Update User")
                        with col2:
                            cancel_edit = st.form_submit_button("❌ Cancel")
                        
                        if update_submitted:
                            update_data = {
                                "name": edit_name,
                                "email": edit_email,
                                "role": edit_role
                            }
                            
                            # Only include password if a new one was provided
                            if edit_password.strip():
                                update_data["password_hash"] = edit_password
                            
                            update_response = requests.put(f"{API_URL}/users/{user_to_manage}", json=update_data)
                            if update_response.status_code == 200:
                                result = update_response.json()
                                if result.get("success"):
                                    st.success("User updated successfully!")
                                    st.session_state.editing_user = None
                                    st.rerun()
                                else:
                                    st.error(f"Error: {result.get('message')}")
                            else:
                                st.error("Failed to update user")
                        
                        if cancel_edit:
                            st.session_state.editing_user = None
                            st.rerun()
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