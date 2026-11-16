 Teacher Management API
 1. About the Project

Teacher Management API is a backend project developed using Python and FastAPI.
This project helps to manage teachers, students, and subjects. Users can add, view, update, and delete their details.
This project also includes user login, email notifications, Redis caching, automated testing, and Docker.

2. Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- JWT Authentication
- Pytest
- Docker
- Docker Compose

3. Features

Teacher Management
- Add new teachers.
- View all teachers.
- View teacher details.
- Update teacher details.
- Delete teachers.

Student Management
- Add new students.
- View all students.
- View student details.
- Update student details.
- Delete students.

Subject Management
- Create new subjects.
- View all subjects.
- Assign subjects to teachers.

User Authentication
- Register new users.
- Login using username and password.
- Generate JWT tokens.
- Protect API endpoints using authentication.

Email Notifications
- Send an email when a teacher is registered.
- Use background tasks to send emails without delaying the API response.

Redis Caching
- Store teacher list data in Redis.
- Set an expiry time for cached data.
- Update the cache when teacher details change.
- Get teacher data from PostgreSQL if Redis is unavailable.

Automated Testing
- Test API operations using Pytest.
- Use SQLite for testing.
- Mock Redis and email services during tests.

Docker
- Create a Docker image for the application.
- Run FastAPI, PostgreSQL, and Redis using Docker Compose.

4. Project Folder Structure

```text
teacher_management/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── security.py
├── email_service.py
├── cache.py
├── cache_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_teachers.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
```

5. Requirements
Before running the project, install:
- Python 3.12 or later
- PostgreSQL
- Redis
- Docker Desktop (for Docker setup)

 6. Download the Project
Open Command Prompt and run:

cmd
git clone https://github.com/kaviya-s08/teacher-management-api.git

Move into the project folder:

cmd
cd teacher-management-api

7. Run the Project Locally

 Step 1: Create a Virtual Environment

cmd
python -m venv .venv

Step 2: Activate the Virtual Environment
For Windows:

cmd
.venv\Scripts\activate

Step 3: Install Required Packages

cmd
pip install -r requirements.txt

To install testing packages, run:

cmd
pip install -r requirements-dev.txt

Step 4: Create the Environment File

Run:
cmd
copy .env.example .env

Open the `.env` file and enter your own configuration details.

You need to provide:
- PostgreSQL username and password.
- Database name.
- Email address and email app password.
- JWT secret key.

Do not upload your `.env` file to GitHub because it contains private information.

Step 5: Start PostgreSQL and Redis

Make sure PostgreSQL and Redis are running on your computer.
Default ports:

- PostgreSQL: 5432
- Redis: 6379

Step 6: Start the Application
Run:
cmd
uvicorn main:app --reload

The application will start at:

http://127.0.0.1:8000

 Step 7: Open API Documentation

Open the following link in your browser:

http://127.0.0.1:8000/docs

You can view and test the API endpoints using Swagger UI.

 8. Run the Project Using Docker

Docker Compose is used to run the FastAPI application, PostgreSQL, and Redis together.

Step 1: Start Docker Desktop

Open Docker Desktop and make sure it is running.

Step 2: Check the Environment File

Make sure the `.env` file is available in the project folder with the required configuration values.

Step 3: Build and Start the Containers

Run:

cmd
docker compose up --build


This command builds the application and starts these three services:

1. FastAPI
2. PostgreSQL
3. Redis

 Step 4: Open the Application

http://localhost:8000/docs

 Step 5: Stop the Containers

Run:
cmd
docker compose down


To remove containers and the PostgreSQL data volume, run:

cmd
docker compose down -v

 9. Run Automated Tests

This project uses Pytest to check whether the application is working correctly.

Step 1: Install Testing Packages

cmd
pip install -r requirements-dev.txt

Step 2: Run All Tests

cmd
pytest -v

The tests use SQLite and mock Redis and email services where needed.
You do not need a running PostgreSQL or Redis server to run the automated test suite.
Test Results

All 33 test cases passed successfully during the latest test run.

 10. Environment Variables

The project uses the following environment variables:

 Variable - Description 
 DB_USER - PostgreSQL username 
 DB_PASSWORD - PostgreSQL password 
 DB_HOST - PostgreSQL host 
 DB_PORT - PostgreSQL port 
 DB_NAME  Database name 
 REDIS_HOST - Redis host 
 REDIS_PORT - Redis port 
 EMAIL_ADDRESS - Email address used to send notifications 
 EMAIL_PASSWORD - Email app password 
 SECRET_KEY - JWT secret key 
 ALGORITHM - JWT algorithm 
 ACCESS_TOKEN_EXPIRE_MINUTES - Token expiry time 

 11. GitHub Repository

Project source code:

https://github.com/kaviya-s08/teacher-management-api

 12. Conclusion

Through this project, I learned how to develop APIs using FastAPI, connect to PostgreSQL, implement user authentication, use Redis caching, send background emails, write automated tests, and run an application using Docker.

This project helped me improve my Python and backend development skills.
