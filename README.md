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

## Common errors and fixes


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

