Home Assignment

A simple JWT-based authentication server built with FastAPI and PostgreSQL.

## Features

- User registration and login
- JWT-based authentication using RSA signing
- Token refresh mechanism
- User profile management
- PostgreSQL database integration

## Prerequisites

- Python 3.8+
- PostgreSQL
- OpenSSL (for generating RSA keys)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd auth-server
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Generate RSA keys:
```bash
# Generate private key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Generate public key
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

5. Create a `.env` file with your configuration:
```
DATABASE_URL=postgresql://user:password@localhost/auth_db
JWT_PRIVATE_KEY_PATH=private_key.pem
JWT_PUBLIC_KEY_PATH=public_key.pem
JWT_ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

6. Create the PostgreSQL database:
```bash
createdb auth_db
```

7. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- POST `/api/v1/register-user` - Register a new user
- POST `/api/v1/auth/login` - Login and get access token
- POST `/api/v1/auth/refresh-token` - Refresh access token
- GET `/api/v1/me` - Get current user profile

## Error Handling

The API implements proper error handling with appropriate HTTP status codes:

- 400 Bad Request - Invalid input data
- 401 Unauthorized - Invalid credentials
- 404 Not Found - Resource not found
- 500 Internal Server Error - Server-side errors

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens are signed using RSA (asymmetric encryption)
- Database connection is protected with environment variables
- Input validation using Pydantic models
