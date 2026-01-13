# quant-crew

Weekly stock reports created via crew of Agentic AI

## Setup

### Prerequisite

- task (taskfile) <https://taskfile.dev/>
- uv <https://docs.astral.sh/uv/getting-started/installation/>
- nvm (npm)

### CREATE Postgresql user and db

```bash
CREATE USER quantcrew WITH PASSWORD 'your-secret-passsword';
CREATE DATABASE quantcrew OWNER quantcrew;
```

### Copy and modify backend/.env

```bash
cd backend
cp .env.example .env
```

### Initialize Database

```bash
# Using Taskfile (recommended)
task db:init

# Or directly
cd backend
uv run python scripts/init_db_and_fetch.py
```

### Run the Application

```bash
# Run both backend and frontend
task run:dev

# Or run separately
task run:backend  # Backend only
task run:frontend # Frontend only
```

## Available Commands

### Development
- `task run:dev` - Run both backend and frontend in parallel
- `task run:backend` - Start FastAPI backend server
- `task run:frontend` - Start frontend dev server

### Database & Data
- `task db:init` - Initialize database and fetch ticker data
- `task db:migrate` - Run database migrations
- `task db:migrate:rollback` - Rollback last migration
- `task db:migrate:create -- "message"` - Create new migration
- `task data:fetch` - Fetch latest ticker data from Yahoo Finance

### Testing & Quality
- `task test:backend` - Run backend tests
- `task test:backend:cov` - Run tests with coverage report
- `task lint:backend` - Lint code with ruff
- `task format:backend` - Format code with black

### Configuration
- `task config:demo` - Demo the configuration system

### Setup
- `task setup:backend` - Install backend dependencies
- `task setup:frontend` - Install frontend dependencies

For more commands, run: `task --list`

## Note
