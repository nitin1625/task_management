

# Task Management API

## Project Overview
This is a Django-based RESTful API for managing tasks and users, built with Django Rest Framework (DRF). The system allows users to create tasks, assign them to users, retrieve tasks per user, and manage user accounts. It uses token-based authentication for secure access and follows best practices for scalability and maintainability.

### Features
- **User Management**: Create users and retrieve user details/list.
- **Task Management**: Create tasks, assign users, and fetch tasks by user.
- **Authentication**: JWT-based authentication for protected endpoints.
- **Admin Interface**: Customized Django admin panel for managing users and tasks.
- **Scalability**: Pagination and proper database indexing.

### Models
- **User**:
  - Fields: `id`, `username`, `email`, `mobile`, `department`, `job_title`, `created_at`, `last_login`, `is_staff`, `is_active`
  - Custom user model with no unnecessary fields (e.g., groups removed).
- **Task**:
  - Fields: `id`, `name`, `description`, `created_at`, `task_type`, `priority`, `status`, `due_date`, `completed_at`, `assigned_users` (ManyToMany with User)
  - `completed_at` auto-updates based on `status`.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (recommended) or SQLite
- Git
- Postman (for testing APIs)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd task_management
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   - Access at: `http://localhost:8000`

---

## Dependencies
Add these to `requirements.txt`:
```
Django>=4.2
djangorestframework>=3.14
```

---

## API Endpoints

### Authentication
- **Obtain Token**:
  - **URL**: `POST api/token/`
  - **Headers**: `Content-Type: application/json`
  - **Payload**:
    ```json
    {
        "email": "admin@gmail.com",
        "password": "admin123"
    }
    ```
  - **Response**: `{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni..."  // New refresh token due to ROTATE_REFRESH_TOKENS
}`

### User Endpoints
1. **Create User**:
   - **URL**: `POST /api/users/create/`
   - **Headers**: `Content-Type: application/json`
   - **Payload**:
     ```json
     {
         "username": "testuser",
         "email": "testuser@example.com",
         "password": "test123",
         "mobile": "1234567890",
         "department": "ENGINEERING",
         "job_title": "Developer"
     }
     ```
   - **Response**: `201 Created` with user details

2. **Get All Users**:
   - **URL**: `GET /api/users/`
   - **Headers**: `Authorization: Token <token>`
   - **Response**:
     ```json
     {
         "users": [{"id": 1, "username": "admin", ...}, ...],
         "total_users": 2
     }
     ```

3. **Get User Details**:
   - **URL**: `GET /api/users/<user_id>/` (e.g., `/api/users/1/`)
   - **Headers**: `Authorization: Token <token>`
   - **Response**:
     ```json
     {
         "id": 1,
         "username": "admin",
         "email": "admin@example.com",
         ...
     }
     ```

### Task Endpoints
1. **Create Task**:
   - **URL**: `POST /api/tasks/create/`
   - **Headers**: 
     - `Authorization: Token <token>`
     - `Content-Type: application/json`
   - **Payload**:
     ```json
     {
         "name": "Develop API Docs",
         "description": "Create API documentation",
         "task_type": "DEVELOPMENT",
         "priority": "HIGH",
         "due_date": "2025-04-10T12:00:00Z",
         "assigned_user_ids": [1, 2]
     }
     ```
   - **Response**: `201 Created` with task details

2. **Assign Task**:
   - **URL**: `PUT /api/tasks/<task_id>/assign/` (e.g., `/api/tasks/1/assign/`)
   - **Headers**: 
     - `Authorization: Token <token>`
     - `Content-Type: application/json`
   - **Payload**:
     ```json
     {
         "assigned_user_ids": [1]
     }
     ```
   - **Response**: `200 OK` with updated task

3. **Get User Tasks**:
   - **URL**: `GET /api/users/<user_id>/tasks/` (e.g., `/api/users/1/tasks/`)
   - **Headers**: `Authorization: Token <token>`
   - **Response**:
     ```json
     {
         "user_id": "1",
         "tasks": [{"id": 1, "name": "Develop API Docs", ...}],
         "total_tasks": 1
     }
     ```

---

## Admin Panel
- **URL**: `http://localhost:8000/admin/`
- **Login**: Use superuser credentials.
- **Features**:
  - **Users**: View/edit with fields like `username`, `email`, `department`, `task_count`.
  - **Tasks**: View/edit with colored `task_type`, `priority`, `status`, and fields like `due_date`, `completed_at`.

---

## Testing with Postman
1. **Setup Environment**:
   - Variables:
     - `base_url`: `http://localhost:8000`
     - `token`: `<your-token-from-api-token-auth>`
   - Use `{{base_url}}` in URLs and `Authorization: Token {{token}}` in headers.

2. **Collection**:
   - **Obtain Token**: `POST {{base_url}}/api/token/`
   - **Create User**: `POST {{base_url}}/api/users/create/`
   - **Get All Users**: `GET {{base_url}}/api/users/`
   - **Get User Details**: `GET {{base_url}}/api/users/1/`
   - **Create Task**: `POST {{base_url}}/api/tasks/create/`
   - **Assign Task**: `PUT {{base_url}}/api/tasks/1/assign/`
   - **Get User Tasks**: `GET {{base_url}}/api/users/1/tasks/`

3. **Workflow**:
   - Get token → Create user → List users → Create task → Assign task → Check user tasks.

---

## Project Structure
```
TASK_MANAGEMENT/
│── task_management/            # Main Django project directory
│   │── __pycache__/            # Compiled Python files
│   │── __init__.py             # Marks the directory as a Python package
│   │── asgi.py                 # ASGI configuration
│   │── settings.py             # Project settings
│   │── urls.py                 # URL configurations
│   │── wsgi.py                 # WSGI configuration
│
│── tasks/                      # Django app for managing tasks
│   │── __pycache__/            # Compiled Python files
│   │── migrations/             # Database migrations
│   │── __init__.py             # Marks the directory as a Python package
│   │── admin.py                # Django admin configurations
│   │── apps.py                 # App configuration
│   │── models.py               # Database models
│   │── serializers.py          # API serializers (for DRF)
│   │── tests.py                # Test cases
│   │── urls.py                 # App-specific URLs
│   │── views.py                # Business logic and API views
│
│── db.sqlite3                   # SQLite database file
│── manage.py                     # Django's CLI management script
│── readme.md                     # Project documentation
│── requirements.txt               # Dependencies list

```

---

## Additional Notes
- **Authentication**: Token-based via `rest_framework.authtoken`. Tokens don’t expire by default.
- **Database**: SQLite by default; 
- **Scalability**: Pagination set to 20 items per page; adjust in `settings.py`.
- **Error Handling**: Validation errors return 400; unauthorized requests return 401.
- **Customizations**: 
  - `completed_at` auto-sets/clears based on `status`.
  - Only active users (`is_active=True`) shown in user list.

---

## Troubleshooting
- **Token Issues**: Ensure `rest_framework.authtoken` is in `INSTALLED_APPS` and migrations are applied.
- **404 Errors**: Verify URLs match `urls.py` and server is running.


