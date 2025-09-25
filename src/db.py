# db_manager.py

import os
from supabase import create_client
from dotenv import load_dotenv

# loading environment variables from a .env file

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

db = create_client(url, key)

# ============ USER MANAGEMENT ============

def create_user(name, email, password_hash, role):
    return db.table("users").insert({
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "role": role
    }).execute()

def get_all_users():
    return db.table("users").select("id, name, email, role, created_at").execute()

def update_user(user_id, data: dict):
    return db.table("users").update(data).eq("id", user_id).execute()

def delete_user(user_id):
    return db.table("users").delete().eq("id", user_id).execute()

# ============ PROJECT MANAGEMENT ============

def create_project(name, description, owner_id, start_date, end_date, status):
    return db.table("projects").insert({
        "name": name,
        "description": description,
        "owner_id": owner_id,
        "start_date": start_date,
        "end_date": end_date,
        "status": status
    }).execute()

def get_all_projects():
    return db.table("projects").select("*").execute()

def update_project(project_id, data: dict):
    return db.table("projects").update(data).eq("id", project_id).execute()

def delete_project(project_id):
    return db.table("projects").delete().eq("id", project_id).execute()

# ============ TASK MANAGEMENT ============

def create_task(project_id, title, description, assigned_to, due_date, status):
    return db.table("tasks").insert({
        "project_id": project_id,
        "title": title,
        "description": description,
        "assigned_to": assigned_to,
        "due_date": due_date,
        "status": status
    }).execute()

def get_tasks_by_project(project_id):
    return db.table("tasks").select("*").eq("project_id", project_id).execute()

def update_task(task_id, data: dict):
    return db.table("tasks").update(data).eq("id", task_id).execute()

def delete_task(task_id):
    return db.table("tasks").delete().eq("id", task_id).execute()
