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

### init_db

```bash
cd backend
uv run python init_db_and_fetch.py
```

### Run the backend and frontend

```bash
task run:dev
```

## Note
