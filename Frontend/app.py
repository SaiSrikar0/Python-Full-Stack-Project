# frontend interface
# using streamlit for the frontend

import streamlit as st
import requests
from datetime import datetime

# backend api url
API_URL = "http://localhost:8000"
st.set_page_config(page_title="Project Manager", layout="wide")
st.title("Project Manager")
st.write("A simple project management tool")
#sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Home", "Projects", "Tasks", "Users"])
st.sidebar.markdown("---")
#home page
if page == "Home":
    st.header("Welcome to Project Manager")
    st.write("Use the sidebar to navigate between pages.")
#projects page
elif page == "Projects":
    st.header("Projects")
    #fetch projects from api
    response = requests.get(f"{API_URL}/projects")
    if response.status_code == 200:
        projects = response.json().get("data", [])
    else:
        st.error("Error fetching projects")
        projects = []
    #display projects
    if projects:
        for project in projects:
            with st.expander(project['name']):
                st.write(f"**Description:** {project.get('description', 'N/A')}")
                st.write(f"**Owner ID:** {project.get('owner_id', 'N/A')}")
                st.write(f"**Start Date:** {project.get('start_date', 'N/A')}")
                st.write(f"**End Date:** {project.get('end_date', 'N/A')}")
                st.write(f"**Status:** {project.get('status', 'N/A')}")
    else:
        st.info("No projects found.")
    #form to add a new project
    st.subheader("Add New Project")
    with st.form("add_project_form"):
        name = st.text_input("Project Name", max_chars=50)
        description = st.text_area("Description", max_chars=200)
        owner_id = st.text_input("Owner ID")
        start_date = st.date_input("Start Date", value=datetime.today())
        end_date = st.date_input("End Date", value=datetime.today())
        status = st.selectbox("Status", ["pending", "ongoing", "completed"])
        submitted = st.form_submit_button("Add Project")
        if submitted:
            if not name or not owner_id:
                st.error("Project Name and Owner ID are required.")
            else:
                project_data = {
                    "name": name,
                    "description": description,
                    "owner_id": owner_id,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "status": status
                }
                response = requests.post(f"{API_URL}/projects", json=project_data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success(result.get("message"))
                    else:
                        st.error(result.get("message"))
                else:
                    st.error("Error adding project")
                st.rerun()
#tasks page
elif page == "Tasks":
    st.header("Tasks")
    #fetch tasks from api
    response = requests.get(f"{API_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json().get("data", [])
    else:
        st.error("Error fetching tasks")
        tasks = []
    #display tasks
    if tasks:
        for task in tasks:
            with st.expander(task['title']):
                st.write(f"**Description:** {task.get('description', 'N/A')}")
                st.write(f"**Project ID:** {task.get('project_id', 'N/A')}")
                st.write(f"**Assigned To:** {task.get('assigned_to', 'N/A')}")
                st.write(f"**Due Date:** {task.get('due_date', 'N/A')}")
                st.write(f"**Status:** {task.get('status', 'N/A')}")
    else:
        st.info("No tasks found.")
    #form to add a new task
    st.subheader("Add New Task")
    with st.form("add_task_form"):
        project_id = st.text_input("Project ID")
        title = st.text_input("Task Title", max_chars=50)
        description = st.text_area("Description", max_chars=200)
        assigned_to = st.text_input("Assigned To (User ID)")
        due_date = st.date_input("Due Date", value=datetime.today())
        status = st.selectbox("Status", ["pending", "in-progress", "completed"])
        submitted = st.form_submit_button("Add Task")
        if submitted:
            if not project_id or not title or not assigned_to:
                st.error("Project ID, Task Title, and Assigned To are required.")
            else:
                task_data = {
                    "project_id": project_id,
                    "title": title,
                    "description": description,
                    "assigned_to": assigned_to,
                    "due_date": due_date.isoformat(),
                    "status": status
                }
                response = requests.post(f"{API_URL}/tasks", json=task_data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success(result.get("message"))
                    else:
                        st.error(result.get("message"))
                else:
                    st.error("Error adding task")
                st.rerun()
#users page
elif page == "Users":
    st.header("Users")
    #fetch users from api
    response = requests.get(f"{API_URL}/users")
    if response.status_code == 200:
        users = response.json().get("data", [])
    else:
        st.error("Error fetching users")
        users = []
    #display users
    if users:
        for user in users:
            with st.expander(user['name']):
                st.write(f"**Email:** {user.get('email', 'N/A')}")
                st.write(f"**Role:** {user.get('role', 'N/A')}")
                st.write(f"**Created At:** {user.get('created_at', 'N/A')}")
    else:
        st.info("No users found.")
    #form to add a new user
    st.subheader("Add New User")
    with st.form("add_user_form"):
        name = st.text_input("Name", max_chars=50)
        email = st.text_input("Email", max_chars=100)
        password_hash = st.text_input("Password Hash", type="password")
        role = st.selectbox("Role", ["admin", "member"])
        submitted = st.form_submit_button("Add User")
        if submitted:
            if not name or not email or not password_hash:
                st.error("Name, Email, and Password are required.")
            else:
                user_data = {
                    "name": name,
                    "email": email,
                    "password_hash": password_hash,
                    "role": role
                }
                response = requests.post(f"{API_URL}/users", json=user_data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success(result.get("message"))
                    else:
                        st.error(result.get("message"))
                else:
                    st.error("Error adding user")
                st.rerun()
#footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 Project Manager")