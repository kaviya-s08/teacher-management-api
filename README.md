\# Teacher Management API



1\. About the Project



Teacher Management API is a backend project developed using Python and FastAPI.



This project helps to manage teachers, students, and subjects. Users can add, view, update, and delete their details.



This project also includes user login, email notifications, Redis caching, automated testing, and Docker.



2\. Technologies Used



\- Python

\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Redis

\- JWT Authentication

\- Pytest

\- Docker

\- Docker Compose



3\. Features



&#x20;Teacher Management

\- Add new teachers.

\- View all teachers.

\- View teacher details.

\- Update teacher details.

\- Delete teachers.



&#x20;Student Management

\- Add new students.

\- View all students.

\- View student details.

\- Update student details.

\- Delete students.



&#x20;Subject Management

\- Create new subjects.

\- View all subjects.

\- Assign subjects to teachers.



&#x20;User Authentication

\- Register new users.

\- Login using username and password.

\- Generate JWT tokens.

\- Protect API endpoints using authentication.



&#x20;Email Notifications

\- Send an email when a teacher is registered.

\- Use background tasks to send emails without delaying the API response.



&#x20;Redis Caching

\- Store teacher list data in Redis.

\- Set an expiry time for cached data.

\- Update the cache when teacher details change.

\- Get teacher data from PostgreSQL if Redis is unavailable.



&#x20;Automated Testing

\- Test API operations using Pytest.

\- Use SQLite for testing.

\- Mock Redis and email services during tests.



&#x20;Docker

\- Create a Docker image for the application.

\- Run FastAPI, PostgreSQL, and Redis using Docker Compose.



&#x20;4. Project Folder Structure



text

teacher\_management/

│

├── main.py

├── database.py

├── models.py

├── schemas.py

├── auth.py

├── security.py

├── email\_service.py

├── cache.py

├── cache\_service.py

│

├── tests/

│   ├── conftest.py

│   ├── test\_auth.py

│   └── test\_teachers.py

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── requirements-dev.txt

├── .env.example

├── .gitignore

└── README.md

```



&#x20;5. Requirements



Before running the project, install:



\- Python 3.12 or later

\- PostgreSQL

\- Redis

\- Docker Desktop (for Docker setup)



&#x20;6. Download the Project

Open Command Prompt and run:



cmd

git clone https://github.com/kaviya-s08/teacher-management-api.git



Move into the project folder:



cmd

cd teacher-management-api



&#x20;7. Run the Project Locally



&#x20;Step 1: Create a Virtual Environment



cmd

python -m venv .venv



Step 2: Activate the Virtual Environment



For Windows:



cmd

.venv\\Scripts\\activate





&#x20;Step 3: Install Required Packages



cmd

pip install -r requirements.txt



To install testing packages, run:



cmd

pip install -r requirements-dev.txt



&#x20;Step 4: Create the Environment File



Run:



cmd

copy .env.example .env



Open the `.env` file and enter your own configuration details.



You need to provide:

\- PostgreSQL username and password.

\- Database name.

\- Email address and email app password.

\- JWT secret key.



Do not upload your `.env` file to GitHub because it contains private information.



&#x20;Step 5: Start PostgreSQL and Redis



Make sure PostgreSQL and Redis are running on your computer.



Default ports:



\- PostgreSQL: 5432

\- Redis: 6379



Step 6: Start the Application



Run:



cmd

uvicorn main:app --reload





The application will start at:



http://127.0.0.1:8000

&#x20;Step 7: Open API Documentation



Open the following link in your browser:



http://127.0.0.1:8000/docs



You can view and test the API endpoints using Swagger UI.



&#x20;8. Run the Project Using Docker



Docker Compose is used to run the FastAPI application, PostgreSQL, and Redis together.



&#x20;Step 1: Start Docker Desktop



Open Docker Desktop and make sure it is running.



&#x20;Step 2: Check the Environment File



Make sure the `.env` file is available in the project folder with the required configuration values.



&#x20;Step 3: Build and Start the Containers



Run:



cmd

docker compose up --build



This command builds the application and starts these three services:

1\. FastAPI

2\. PostgreSQL

3\. Redis



&#x20;Step 4: Open the Application



http://localhost:8000/docs



&#x20;Step 5: Stop the Containers



Run:



cmd

docker compose down



To remove containers and the PostgreSQL data volume, run:



cmd

docker compose down -v



Note: The `-v` option deletes the PostgreSQL data stored in the Docker volume.



&#x20;9. Run Automated Tests



This project uses Pytest to check whether the application is working correctly.



&#x20;Step 1: Install Testing Packages



cmd

pip install -r requirements-dev.txt



&#x20;Step 2: Run All Tests



cmd

pytest -v



The tests use SQLite and mock Redis and email services where needed.



You do not need a running PostgreSQL or Redis server to run the automated test suite.



&#x20;Test Results



All 33 test cases passed successfully during the latest test run.



&#x20;10. Environment Variables



The project uses the following environment variables:



&#x20;Variable | Description |



&#x20;DB\_USER - PostgreSQL username 

&#x20;DB\_PASSWORD - PostgreSQL password 

&#x20;DB\_HOST  PostgreSQL host 

&#x20;DB\_PORT - PostgreSQL port 

&#x20;DB\_NAME - Database name 

&#x20;REDIS\_HOST - Redis host 

&#x20;REDIS\_PORT - Redis port 

&#x20;EMAIL\_ADDRESS - Email address used to send notifications 

&#x20;EMAIL\_PASSWORD - Email app password 

&#x20;SECRET\_KEY - JWT secret key 

&#x20;ALGORITHM - JWT algorithm 

&#x20;ACCESS\_TOKEN\_EXPIRE\_MINUTES  Token expiry time 



11\. GitHub Repository



Project source code:



https://github.com/kaviya-s08/teacher-management-api



12\. Conclusion



Through this project, I learned how to develop APIs using FastAPI, connect to PostgreSQL, implement user authentication, use Redis caching, send background emails, write automated tests, and run an application using Docker.



This project helped me improve my Python and backend development skills.

