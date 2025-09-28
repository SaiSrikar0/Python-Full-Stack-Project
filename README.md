# ProjectDock : A Project Management System

ProjectDock is a lightweight full-stack application for managing projects, tasks, and team members. It uses FastAPI for the backend API, Streamlit for the frontend interface, and Supabase as the database. Users can create projects, assign tasks, track progress, and collaborate in one simple dashboard.
## 🚀 Features

- **Project Management**: Create, update, and track projects
- **Task Management**: Organize tasks with status tracking
- **User-friendly Interface**: Built with Streamlit for an intuitive web experience
- **RESTful API**: FastAPI backend for scalable operations
- **Real-time Data**: Supabase integration for live data synchronization

## 📁 Project Structure

```
Project Manager/
|--- README.md             # Project documentation
|
|--- requirements.txt      # Python dependencies
|
|--- .env                  #Setup for environment variables
|
|--- API/                  # Backend API
|   |-- main.py            # FastAPI backend application
|
|--- Frontend/             # Frontend application
|   |-- app.py             # Streamlit frontend application
|
|--- src/                  # Core application logic
|   |-- db.py              # Database connection and operations
|   |-- logic.py           # Business logic and utilities
```

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: Supabase
- **Server**: Uvicorn
- **Configuration**: python-dotenv

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Supabase account and project
- Git (Push, Cloning)

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd "Project Manager"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   ```
## Setup Supebase

1. create a Supebase project

2. create the necessary tables. Select and run the following command in SQL Editor in Supebase:
    
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT CHECK (role IN ('admin', 'member')) DEFAULT 'member',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    CREATE TABLE projects (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name TEXT NOT NULL,
        owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
        start_date DATE,
        end_date DATE,
        team_members JSONB DEFAULT '[]'::jsonb, -- array of user UUIDs
        status TEXT CHECK (status IN ('pending', 'ongoing', 'completed')) DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        description TEXT NULL
    );

    CREATE TABLE tasks (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        description TEXT,
        assigned_to UUID REFERENCES users(id) ON DELETE SET NULL,
        status TEXT CHECK (status IN ('pending', 'in-progress', 'completed')) DEFAULT 'pending',
        due_date DATE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );


## 🏃‍♂️ Running the Application

### Start the FastAPI Backend
```bash
cd API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start the Streamlit Frontend
```bash
cd Frontend
streamlit run app.py
```

The application will be available at:
- Frontend: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## 📊 API Endpoints

The FastAPI backend provides RESTful endpoints for:
- Project CRUD operations
- Task management
- User authentication (if implemented)
- Data analytics and reporting

Visit `/docs` when the API is running for interactive API documentation.

## 🗄️ Database Schema

The application uses Supabase as the backend database. Key tables include:
- Projects
- Tasks
- Users (if authentication is implemented)

## 🔧 Configuration

Environment variables can be configured in the `.env` file:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anonymous key
- Additional configuration options as needed

## 📝 Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 🚨 Common Errors and Fixes

This section covers common issues encountered during development and their solutions:

### 1. **JSON Decode Errors**
**Error:** `requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`

**Cause:** API server not running or returning non-JSON responses

**Fix:**
```bash
# Ensure the FastAPI server is running
cd API
uvicorn main:app --host 0.0.0.0 --port 8080
```

**Code Fix in Frontend:**
```python
# Enhanced error handling in app.py
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
```

### 2. **CORS Policy Errors**
**Error:** `Access to fetch at 'http://localhost:8080' from origin 'http://localhost:8501' has been blocked by CORS policy`

**Cause:** Frontend and backend running on different ports without proper CORS configuration

**Fix:** Add CORS middleware in `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. **Supabase Connection Issues**
**Error:** `supabase.exceptions.APIError: Invalid API key`

**Cause:** Missing or incorrect environment variables

**Fix:**
1. Create `.env` file in root directory:
```bash
SUPABASE_URL=your_actual_supabase_url
SUPABASE_KEY=your_actual_supabase_anon_key
```

2. Verify environment loading in `db.py`:
```python
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
```

### 4. **UUID Validation Errors**
**Error:** `pydantic.ValidationError: invalid input syntax for type uuid`

**Cause:** Manually entered UUIDs in forms causing validation issues

**Fix:** Replace manual UUID inputs with dropdown selections:
```python
# Instead of text input for UUIDs
# owner_id = st.text_input("Owner ID (UUID)")

# Use dropdown with user-friendly display
if available_users:
    owner_option = st.selectbox(
        "Project Owner", 
        options=[user[0] for user in available_users],
        format_func=lambda x: next(user[1] for user in available_users if user[0] == x)
    )
```

### 5. **Port Conflicts**
**Error:** `OSError: [WinError 10048] Only one usage of each socket address is normally permitted`

**Cause:** Port already in use by another process

**Fix:**
```bash
# Check what's using the port
netstat -ano | findstr :8080

# Kill the process (replace PID with actual process ID)
taskkill /PID 12345 /F

# Or use different ports
uvicorn main:app --host 0.0.0.0 --port 8000  # Backend
streamlit run app.py --server.port 8501      # Frontend
```

### 6. **Module Import Errors**
**Error:** `ModuleNotFoundError: No module named 'src'`

**Cause:** Python path not properly configured for relative imports

**Fix:** Add path configuration in API files:
```python
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import ProjectManager, TaskManager, UserManager
```

### 7. **Database Table Not Found**
**Error:** `supabase.exceptions.APIError: relation "projects" does not exist`

**Cause:** Database tables not created in Supabase

**Fix:** Run the table creation SQL in Supabase SQL Editor:
```sql
-- Copy and execute the complete SQL from the README setup section
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- ... rest of the schema
);
```

### 8. **Streamlit Dark Theme Issues**
**Error:** Text not visible in dark theme or inconsistent styling

**Fix:** Apply comprehensive CSS styling:
```python
st.markdown("""
<style>
.stApp {
    background-color: #1E1E1E;
    color: #FFFFFF;
}
h1, h2, h3, h4, h5, h6 {
    color: #FF4B4B !important;
}
.stTextInput>div>div>input {
    background-color: #252526;
    color: white !important;
    border: 1px solid #FF4B4B;
}
</style>
""", unsafe_allow_html=True)
```

### 9. **Terminal Navigation Issues**
**Error:** Commands failing due to incorrect working directory

**Fix:** Always use absolute paths or proper directory changes:
```bash
# Use full path navigation
cd "C:\Users\username\OneDrive\Desktop\Project Manager\API"

# Or use relative navigation step by step
cd "Project Manager"
cd API
```

### 10. **Package Installation Issues**
**Error:** `pip: command not found` or package conflicts

**Fix:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt

# If conflicts occur, create virtual environment
python -m venv project_env
project_env\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 🔧 **Debugging Tips**

1. **Check Server Status:**
   ```bash
   # Test API directly
   curl http://localhost:8080/
   # Or in PowerShell
   Invoke-RestMethod -Uri "http://localhost:8080/" -Method GET
   ```

2. **Monitor Logs:**
   - Backend: Check uvicorn console output
   - Frontend: Check streamlit console output
   - Database: Check Supabase dashboard logs

3. **Environment Verification:**
   ```python
   # Test database connection
   python -c "from src.db import DataBaseManager; db = DataBaseManager(); print('Connection:', db.get_all_users())"
   ```

4. **Browser Developer Tools:**
   - Check Network tab for API call failures
   - Check Console for JavaScript errors
   - Verify CORS headers in Response headers


## � Future Enhancements

The following features and improvements are planned for future releases:

### Frontend Modernization
- **React/Next.js Migration**: Convert the frontend from Streamlit to React or Next.js for better performance, customization, and modern web development practices
- **Enhanced UI/UX**: Implement a more sophisticated user interface with advanced styling and animations
- **Mobile Responsiveness**: Ensure full mobile compatibility and responsive design
- **Progressive Web App (PWA)**: Add offline capabilities and mobile app-like experience

### Feature Enhancements
- **Real-time Collaboration**: Implement WebSocket connections for real-time updates and collaboration
- **Advanced Authentication**: Add OAuth integration (Google, GitHub, Microsoft)
- **Role-based Permissions**: Implement granular permission system for different user roles
- **File Management**: Add file upload/download capabilities for project documents
- **Notifications System**: Email and in-app notifications for task assignments and deadlines
- **Time Tracking**: Built-in time tracking for tasks and projects
- **Reporting Dashboard**: Advanced analytics and reporting with charts and graphs
- **Gantt Charts**: Visual project timeline management
- **Comments System**: Task and project commenting functionality

### Technical Improvements
- **API Versioning**: Implement proper API versioning strategy
- **Caching Layer**: Add Redis for improved performance
- **Testing Suite**: Comprehensive unit and integration tests
- **CI/CD Pipeline**: Automated testing and deployment
- **Docker Containerization**: Container-based deployment
- **Microservices Architecture**: Split into smaller, manageable services
- **GraphQL API**: Alternative to REST API for more efficient data fetching

### Integration & Extensions
- **Third-party Integrations**: Slack, Microsoft Teams, Jira, Trello
- **Calendar Integration**: Google Calendar, Outlook integration
- **Email Integration**: Direct email notifications and updates
- **Export Functionality**: PDF, Excel export for reports and data
- **API Rate Limiting**: Implement proper rate limiting and throttling
- **Audit Logging**: Track all user actions and system changes

## �📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you have any questions or issues, please open an issue on GitHub or contact the development team.
Mail : bsaisrikar05@gmail.com