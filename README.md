# FastAPI Template

A production-ready FastAPI backend template with modular architecture, authentication, database management, and AWS integration.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🔐 **Authentication** - JWT-based authentication with role-based access control
- 🗄️ **Database** - SQLAlchemy ORM with Alembic migrations
- 📦 **Modular Structure** - Clean, organized codebase with separation of concerns
- 🧪 **Testing** - Pytest setup for unit and integration tests
- ☁️ **AWS Integration** - S3 client for file operations
- 📄 **Pagination** - Built-in pagination utilities
- 🎨 **Templates** - HTML templates support
- 📝 **Logging** - Configurable logging system

## Project Structure

```
fastapi-template/
├── alembic/              # Database migrations
├── src/                  # Source code
│   ├── auth/            # Authentication module
│   ├── aws/             # AWS services module
│   ├── posts/           # Posts module (example)
│   ├── config.py        # Global configuration
│   ├── database.py      # Database setup
│   ├── exceptions.py    # Global exception handlers
│   ├── models.py        # Global database models
│   ├── pagination.py    # Pagination utilities
│   └── main.py          # FastAPI application
├── tests/               # Test files
├── templates/           # HTML templates
├── requirements/        # Python dependencies
│   ├── base.txt        # Base dependencies
│   ├── dev.txt         # Development dependencies
│   └── prod.txt        # Production dependencies
├── .env                 # Environment variables
├── .gitignore          # Git ignore rules
├── logging.ini          # Logging configuration
└── alembic.ini         # Alembic configuration
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL (or your preferred database)
- pip

### Installation

1. **Clone or use this template**

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements/dev.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env  # If you have an example file
   # Or create .env file with your configuration
   ```

5. **Configure database**
   - Update `DATABASE_URL` in `.env` file
   - Example: `postgresql://user:password@localhost:5432/fastapi_db`

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Run the application**
   ```bash
   uvicorn src.main:app --reload
   ```

8. **Access the API**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Environment Variables

Key environment variables in `.env`:

```env
# Application
APP_NAME=FastAPI Template
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# AWS (optional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

## Module Structure

Each module (auth, aws, posts) follows this structure:

- `router.py` - API endpoints
- `schemas.py` - Pydantic models for request/response validation
- `models.py` - SQLAlchemy database models
- `service.py` - Business logic layer
- `dependencies.py` - FastAPI dependencies
- `config.py` - Module-specific configuration
- `constants.py` - Module constants
- `exceptions.py` - Module-specific exceptions
- `utils.py` - Utility functions

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info

### Posts
- `GET /api/v1/posts/` - List posts (paginated)
- `GET /api/v1/posts/me` - Get current user's posts
- `POST /api/v1/posts/` - Create a new post
- `GET /api/v1/posts/{post_id}` - Get a post by ID
- `PUT /api/v1/posts/{post_id}` - Update a post
- `DELETE /api/v1/posts/{post_id}` - Delete a post

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## Development

### Code Formatting
```bash
black src/ tests/
isort src/ tests/
```

### Type Checking
```bash
mypy src/
```

### Linting
```bash
flake8 src/ tests/
```

## Production Deployment

1. **Install production dependencies**
   ```bash
   pip install -r requirements/prod.txt
   ```

2. **Set environment variables**
   - Ensure `DEBUG=False` in production
   - Use strong `SECRET_KEY`
   - Configure proper `CORS_ORIGINS`

3. **Run with Gunicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## Adding New Modules

To add a new module:

1. Create a new directory under `src/`
2. Add the standard files: `router.py`, `schemas.py`, `models.py`, etc.
3. Register the router in `src/main.py`
4. Add the model to `alembic/env.py` for migrations
5. Create corresponding test files in `tests/`

## License

This is a template project. Feel free to use it as a starting point for your projects.

## Contributing

This is a template repository. Feel free to fork and customize for your needs!

