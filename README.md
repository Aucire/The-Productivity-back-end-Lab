# Personal Productivity API

A RESTful API built with **Python, Flask, and SQLAlchemy** that allows users to manage their personal productivity notes. Users can create accounts, authenticate securely, and manage their own notes through protected API endpoints.

## Features

- User registration and authentication.
- Secure password hashing using Flask-Bcrypt.
- JWT-based authentication.
- Authenticated user profile.
- Create, read, update, and delete notes (CRUD).
- Note categories and priority levels.
- Track completed and pending tasks.
- Pagination for retrieving notes.
- User-specific data ownership and access protection.
- Database migrations using Flask-Migrate.
- Seed data for demonstration purposes.
- Automated testing using Pytest.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Flask | Backend framework |
| Flask-SQLAlchemy | Database ORM |
| SQLite | Database |
| Flask-Migrate | Database migrations |
| Flask-JWT-Extended | Authentication |
| Flask-Bcrypt | Password hashing |
| Pytest | Automated testing |

## Project Structure

```text
flask-productivity-api/
│
├── README.md
├── .gitignore
│
└── server/
    ├── app.py
    ├── config.py
    ├── extensions.py
    ├── seed.py
    ├── Pipfile
    │
    ├── controllers/
    │   ├── __init__.py
    │   ├── auth.py
    │   └── notes.py
    │
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   └── note.py
    │
    ├── migrations/
    └── testing/
        ├── conftest.py
        ├── test_auth.py
        └── test_notes.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone git@github.com:mils2001/flask-productivity-api.git
cd flask-productivity-api/server
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Using Pipenv:

```bash
pip install pipenv
pipenv install --dev
```

Alternatively, install the dependencies directly:

```bash
pip install Flask==2.2.2 \
Flask-SQLAlchemy==3.0.3 \
Werkzeug==2.2.2 \
marshmallow==3.20.1 \
Faker==15.3.2 \
Flask-Migrate==4.0.0 \
Flask-RESTful==0.3.9 \
importlib-metadata==6.0.0 \
importlib-resources==5.10.0 \
Flask-Bcrypt==1.0.1 \
Flask-JWT-Extended==4.7.4 \
pytest==7.2.0
```

### 4. Configure environment variables

Set development secrets before running the application:

```bash
export SECRET_KEY="your-secret-key"
export JWT_SECRET_KEY="your-jwt-secret"
```

Use strong, private secrets for deployment. Never commit real secrets to GitHub.

### 5. Apply database migrations

```bash
flask --app app db upgrade
```

### 6. Seed the database

```bash
python seed.py
```

The seed script creates demonstration users and notes. It checks for existing records to prevent duplicates.

### 7. Start the application

```bash
python -m flask --app app run
```

The API will be available at:

`http://127.0.0.1:5000`

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Log in and receive an access token |
| GET | `/api/auth/me` | Retrieve the authenticated user's profile |

### Notes Endpoints

All notes endpoints require JWT authentication.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/notes` | Create a new note |
| GET | `/api/notes` | Retrieve all user's notes |
| GET | `/api/notes/<id>` | Retrieve a specific note |
| PUT | `/api/notes/<id>` | Update an existing note |
| DELETE | `/api/notes/<id>` | Delete a note |

### Health Check

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check API health |
| GET | `/` | API welcome message |

## Authentication

The application uses JSON Web Tokens (JWT) to protect private endpoints.

After successfully logging in, the API returns an access token.

Include the token in authenticated requests using:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Example API Requests

### Register a user

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"christian","email":"christian@example.com","password":"Password123"}'
```

### Log in

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{"username":"christian","password":"Password123"}'
```

### Create a note

```bash
curl -X POST http://127.0.0.1:5000/api/notes \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{"title":"Learn Flask","content":"Practice Flask and SQLAlchemy","category":"Learning","priority":"High"}'
```

### Retrieve notes with pagination

```bash
curl "http://127.0.0.1:5000/api/notes?page=1&per_page=10" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Demo Account

The seed script provides a development demonstration account:

| Field | Value |
|---|---|
| Username | demo |
| Email | demo@example.com |
| Password | DemoPass123! |

The demo password can be changed by setting the `SEED_PASSWORD` environment variable before running the seed script.

**Note:** These are demonstration credentials only. Change them before using the application in a public deployment.

## Automated Testing

The project uses Pytest to verify API functionality.

Run all tests from the `server` directory:

```bash
python -m pytest testing/ -v
```

Tests cover:

- User registration and login.
- Authentication and authorization.
- Password validation.
- Creating and retrieving notes.
- Updating and deleting notes.
- Pagination.
- Invalid requests.
- User ownership protection.

The test suite uses a separate in-memory SQLite database to avoid modifying the development database.

## Security

The application implements:

- Password hashing.
- JWT-protected endpoints.
- User-specific note access.
- Input validation.
- Authentication error handling.
- Environment-based secret configuration.

## Author

**Software Development Project**

Built with Python, Flask, SQLAlchemy, and SQLite.

## License

Created for educational and portfolio purposes.
