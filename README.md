

\# Teacher Management API



A RESTful API built using FastAPI and PostgreSQL to manage teachers, students, and subjects. The project includes JWT authentication, Redis caching, background email notifications, automated testing, and Docker containerization.



\## Technologies Used



\- Python

\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Redis

\- JWT Authentication

\- Pytest

\- Docker

\- Docker Compose



\## Features



\- Teacher and student CRUD operations

\- Subject creation and retrieval

\- Assign subjects to teachers

\- JWT-based user registration and login

\- Protected API endpoints

\- SQLAlchemy database relationships

\- Background email notifications

\- Redis caching for teacher list API

\- Cache expiration using TTL

\- Cache invalidation after create, update, and delete operations

\- Database fallback when Redis is unavailable

\- Automated API testing using Pytest

\- Docker containerization



\## Project Structure



```text

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

│   └── test\_teachers.py

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── requirements-dev.txt

├── .env.example

└── README.md

```



\## Prerequisites



\- Python 3.12 or later

\- PostgreSQL

\- Redis

\- Docker Desktop (for Docker setup)



\## Local Setup



\### 1. Clone the Repository



```bash

git clone https://github.com/kaviya-s08/teacher-management-api.git

cd teacher-management

```



\### 2. Create a Virtual Environment



```bash

python -m venv .venv

```



Activate it on Windows:



```bash

.venv\\Scripts\\activate

```



\### 3. Install Dependencies



For the application:



```bash

pip install -r requirements.txt

```



For development and testing:



```bash

pip install -r requirements-dev.txt

```



\### 4. Configure Environment Variables



Create your environment file using the example:



```bash

copy .env.example .env

```



Update `.env` with your PostgreSQL credentials, JWT secret, and email configuration.



Do not upload `.env` to GitHub.



\### 5. Start PostgreSQL and Redis



Make sure PostgreSQL and Redis are running locally.



Update `DB\_HOST` and `REDIS\_HOST` in `.env` if necessary.



\### 6. Run the Application



```bash

uvicorn main:app --reload

```



The API will be available at:



http://127.0.0.1:8000



\### 7. Open API Documentation



Swagger UI:



http://127.0.0.1:8000/docs



ReDoc:



http://127.0.0.1:8000/redoc



\## Docker Setup



Docker Compose starts three services:



\- FastAPI

\- PostgreSQL

\- Redis



\### 1. Configure Environment Variables



Ensure that `.env` exists in the project root and contains the required configuration.



\### 2. Build and Start Containers



```bash

docker compose up --build

```



\### 3. Access the Application



http://localhost:8000/docs



\### 4. Stop Containers



```bash

docker compose down

```



To remove containers and the PostgreSQL data volume:



```bash

docker compose down -v

```



Warning: The `-v` option deletes the stored PostgreSQL data.



\## Running Tests



Install development dependencies:



```bash

pip install -r requirements-dev.txt

```



Run all tests:



```bash

pytest -v

```



The automated tests use SQLite and mock external services where appropriate. They do not require a live PostgreSQL or Redis server.



\## Environment Variables



| Variable | Description |

|---|---|

| DB\_USER | PostgreSQL username |

| DB\_PASSWORD | PostgreSQL password |

| DB\_HOST | PostgreSQL host |

| DB\_PORT | PostgreSQL port |

| DB\_NAME | PostgreSQL database name |

| REDIS\_HOST | Redis host |

| REDIS\_PORT | Redis port |

| EMAIL\_ADDRESS | Sender email address |

| EMAIL\_PASSWORD | Email app password |

| SECRET\_KEY | JWT signing secret |

| ALGORITHM | JWT algorithm |

| ACCESS\_TOKEN\_EXPIRE\_MINUTES | JWT token expiration time |



\## GitHub Repository



https://github.com/kaviya-s08/teacher-management-api



