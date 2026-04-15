# notes-productivity-app

# Productivity Notes API (Flask Backend)

A secure Flask REST API for a productivity application that allows users to register, log in, and manage personal notes.  
Each user can only access and manage their own notes using session-based authentication.


## Features

- User registration (signup)
- User login and logout (session-based authentication)
- Retrieve current logged-in user (`/me`)
- Full CRUD operations for notes
- Pagination for notes listing
- Protected routes (user-specific access control)
- Password hashing using bcrypt

---

## Tech Stack

- Python 3
- Flask

- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite


## Project Structure

app.py          - Main application (routes and configuration)  
models.py       - Database models (User, Note)  
seed.py         - Database seed script  
migrations/     - Database migration files  
venv/           - Virtual environment (not tracked in git)


## Author
Jeremy Junior

## license
MIT