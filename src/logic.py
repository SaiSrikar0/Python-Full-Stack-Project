# src logic.py

from src.db import DataBaseManager

class TaskManager:
    '''
    acts as a bridge between frontend(Streamlit/FastAPI) and database
    '''
    def __init__(self):
        #create an instance of the database manager (this will handle all db operations)
        self.db = DataBaseManager()

    #create a new task

    def add_task(self, project_id, title, description, assigned_to, due_date, status):
        '''
        add a new task to the database
        return the success if task is added successfully
        '''
        result = self.db.create_task(project_id, title, description, assigned_to, due_date, status)
        if result.data:
            return {"success": True, "message": "task added successfully"}
        return {"success": False, "message": "error adding task"}
    
    def get_tasks(self):
        '''
        get all tasks from the database
        return all tasks
        '''
        result = self.db.get_all_tasks()
        if result.data:
            return {"success": True, "message": "retrived all tasks", "data": result.data}
        return {"success": False, "message": "error retrieving tasks"}
    
    def mark_complete(self, task_id):
        '''
        mark a task as complete
        return the success if task is marked as complete successfully
        '''
        result = self.db.update_task(task_id, {"status": "completed"})
        if result.data:
            return {"success": True, "message": "task marked as completed"}
        return {"success": False, "message": "error marking task as completed"}
    
    def mark_pending(self, task_id):
        '''
        mark a task as pending
        return the success if task is marked as pending successfully
        '''
        result = self.db.update_task(task_id, {"status": "pending"})
        if result.data:
            return {"success": True, "message": "task marked as pending"}
        return {"success": False, "message": "error marking task as pending"}
    
    def remove_task(self, task_id):
        '''
        remove a task from the database
        return the success if task is removed successfully
        '''
        result = self.db.delete_task(task_id)
        if result.data:
            return {"success": True, "message": "task removed successfully"}
        return {"success": False, "message": "error removing task"}

class ProjectManager:
    '''
    Handles project-related operations
    '''

    def __init__(self):
        self.db = DataBaseManager()
    #create
    def add_project(self, name, description, owner_id, start_date, end_date, status):
        '''
        add a new project to the database
        return the success if project is added successfully
        '''
        if not name or not owner_id:
            return {"success": False, "message": "Project name and owner_id are required"}
        result = self.db.create_project(name, description, owner_id, start_date, end_date, status)
        if result.data:
            return {"success": True, "message": "project added successfully"}
        return {"success": False, "message": "error adding project"}
    
    #read
    def get_projects(self):
        '''
        get all projects from the database
        return all projects
        '''
        result = self.db.get_all_projects()
        if result.data:
            return {"success": True, "message": "retrived all projects", "data": result.data}
        return {"success": False, "message": "error retrieving projects"}
    
    #update
    def update_project(self, project_id, data: dict):
        '''
        update a project in the database
        return the success if project is updated successfully
        '''
        if not data:
            return {"success": False, "message": "No data provided for update"}
        result = self.db.update_project(project_id, data)
        if result.data:
            return {"success": True, "message": "project updated successfully"}
        return {"success": False, "message": "error updating project"}
    
    #delete
    def remove_project(self, project_id):
        '''
        remove a project from the database
        return the success if project is removed successfully
        '''
        result = self.db.delete_project(project_id)
        if result.data:
            return {"success": True, "message": "project removed successfully"}
        return {"success": False, "message": "error removing project"}
    
class UserManager:
    '''
    Handles user-related operations
    '''

    def __init__(self):
        self.db = DataBaseManager()
    
    #create
    def add_user(self, name, email, password_hash, role):
        '''
        add a new user to the database
        return the success if user is added successfully
        '''
        if not name or not email or not password_hash:
            return {"success": False, "message": "Name, email, and password are required"}
        result = self.db.create_user(name, email, password_hash, role)
        if result.data:
            return {"success": True, "message": "user added successfully"}
        return {"success": False, "message": "error adding user"}
    
    #read
    def get_users(self):
        '''
        get all users from the database
        return all users
        '''
        result = self.db.get_all_users()
        if result.data:
            return {"success": True, "message": "retrived all users", "data": result.data}
        return {"success": False, "message": "error retrieving users"}
    
    #update
    def update_user(self, user_id, data: dict):
        '''
        update a user in the database
        return the success if user is updated successfully
        '''
        if not data:
            return {"success": False, "message": "No data provided for update"}
        result = self.db.update_user(user_id, data)
        if result.data:
            return {"success": True, "message": "user updated successfully"}
        return {"success": False, "message": "error updating user"}
    
    #delete
    def remove_user(self, user_id):
        '''
        remove a user from the database
        return the success if user is removed successfully
        '''
        result = self.db.delete_user(user_id)
        if result.data:
            return {"success": True, "message": "user removed successfully"}
        return {"success": False, "message": "error removing user"}