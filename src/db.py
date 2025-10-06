# db_manager.py

import os
from supabase import create_client
from dotenv import load_dotenv

# loading environment variables from .env file
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Validate environment variables
if not url or not key:
    raise ValueError(f"Missing Supabase credentials. URL: {'✓' if url else '✗'}, KEY: {'✓' if key else '✗'}")

# Remove any quotes that might be in the environment variables
url = url.strip('"\'')
key = key.strip('"\'')

print(f"Connecting to Supabase: {url[:50]}...")  # Debug info

try:
    db = create_client(url, key)
    print("✅ Supabase connection established")
except Exception as e:
    print(f"❌ Failed to connect to Supabase: {e}")
    raise

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

def get_all_tasks():
    return db.table("tasks").select("*").execute()

def update_task(task_id, data: dict):
    return db.table("tasks").update(data).eq("id", task_id).execute()

def delete_task(task_id):
    return db.table("tasks").delete().eq("id", task_id).execute()

# ============ DATABASE MANAGER CLASS ============

class DataBaseManager:
    def create_user(self, name, email, password_hash, role):
        return create_user(name, email, password_hash, role)
    
    def get_all_users(self):
        return get_all_users()
    
    def update_user(self, user_id, data):
        return update_user(user_id, data)
    
    def delete_user(self, user_id):
        return delete_user(user_id)
    
    def create_project(self, name, description, owner_id, start_date, end_date, status):
        return create_project(name, description, owner_id, start_date, end_date, status)
    
    def get_all_projects(self):
        return get_all_projects()
    
    def update_project(self, project_id, data):
        return update_project(project_id, data)
    
    def delete_project(self, project_id):
        return delete_project(project_id)
    
    def create_task(self, project_id, title, description, assigned_to, due_date, status):
        return create_task(project_id, title, description, assigned_to, due_date, status)
    
    def get_all_tasks(self):
        return get_all_tasks()
    
    def get_tasks_by_project(self, project_id):
        return get_tasks_by_project(project_id)
    
    def update_task(self, task_id, data):
        return update_task(task_id, data)
    
    def delete_task(self, task_id):
        return delete_task(task_id)
