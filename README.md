# Event Management System API

This project is a simple Django REST Framework API for managing users. It provides endpoints for registering new accounts, obtaining JWT authentication tokens, and performing standard CRUD operations on user profiles.

## Features

- User registration with email/password
- JWT authentication using `djangorestframework-simplejwt`
- Endpoints for updating profile information and changing passwords
- Admin site accessible at `/admin/`

## Requirements

- Python 3.10+
- Django 5.2+
- djangorestframework
- djangorestframework-simplejwt

You can install dependencies with:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

## Running the project

1. Apply migrations:

```bash
python manage.py migrate
```

2. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

## Usage

- Register a user via `POST /api/users/register/` with `first_name`, `last_name`, `email`, and `password` fields.
- Obtain JWT tokens via `POST /api/users/login/` using your credentials.
- Access authenticated endpoints (such as profile management) using the returned access token.

The browsable API provided by Django REST Framework is available at `/api/` when the server is running in debug mode.

