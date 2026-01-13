# Taskfile Commands Reference

Complete reference for all available `task` commands in the Quant-Crew project.

## Quick Reference

```bash
# Show all available commands
task --list

# Get help for a specific task
task --summary <task-name>
```

---

## Development Commands

### Run Application

```bash
# Start both backend and frontend in parallel
task run:dev

# Start backend only (FastAPI)
task run:backend

# Start frontend only (Next.js)
task run:frontend
```

**What happens**:
- `run:dev`: Starts both services simultaneously
- `run:backend`: FastAPI at http://localhost:8000
- `run:frontend`: Next.js at http://localhost:3000

---

## Setup Commands

### Initial Setup

```bash
# Setup backend (install Python dependencies)
task setup:backend

# Setup frontend (install Node dependencies)
task setup:frontend
```

**What happens**:
- Creates virtual environment (backend)
- Installs all dependencies from pyproject.toml or package.json
- Only runs if dependencies have changed

---

## Database Commands

### Initialize Database

```bash
# Initialize database and fetch initial data
task db:init
```

**What it does**:
1. Runs Alembic migrations
2. Fetches ticker data from Yahoo Finance
3. Populates database

**When to use**: First time setup or after database reset

### Migrations

```bash
# Apply pending migrations
task db:migrate

# Rollback last migration
task db:migrate:rollback

# Create new migration
task db:migrate:create -- "add user authentication"
```

**Migration workflow**:
1. Modify SQLAlchemy models
2. Run `task db:migrate:create -- "description"`
3. Review generated migration in `backend/alembic/versions/`
4. Run `task db:migrate` to apply

---

## Data Management

### Fetch Ticker Data

```bash
# Fetch latest stock data from Yahoo Finance
task data:fetch
```

**What it does**:
- Downloads latest price data for configured tickers
- Updates database with new records
- Can be run daily/regularly

**Configured tickers**: See `backend/app/config/stock_watchlist.yaml`

---

## Testing Commands

### Run Tests

```bash
# Run all backend tests
task test:backend

# Run tests with coverage report
task test:backend:cov
```

**Coverage report**:
- Terminal output shows coverage percentages
- HTML report generated in `backend/htmlcov/`
- Open `htmlcov/index.html` in browser to view

---

## Code Quality

### Linting

```bash
# Check code for issues
task lint:backend
```

Uses `ruff` to check for:
- Code style violations
- Potential bugs
- Unused imports
- And more

### Formatting

```bash
# Auto-format code with black
task format:backend
```

Automatically formats all Python code to consistent style.

**Tip**: Run `task format:backend` before committing code.

---

## Configuration

### Demo Configuration System

```bash
# Display all loaded configuration
task config:demo
```

Shows:
- Environment variables from `.env`
- YAML configuration (agents, watchlist)
- All settings values

**Useful for**: Verifying configuration is loaded correctly

---

## Frontend Sync

### Sync from External Repo

```bash
# Sync frontend from ~/workspace/quant-crew-ui
task sync:frontend
```

**Use case**: If developing frontend in separate repo

---

## Task Dependencies

Tasks automatically handle dependencies:

```bash
# This will automatically run setup:backend first
task run:backend

# This will run both setup tasks before starting
task run:dev
```

You don't need to manually run setup tasks unless you want to.

---

## Common Workflows

### First Time Setup

```bash
# 1. Setup dependencies
task setup:backend
task setup:frontend

# 2. Configure environment
cd backend
cp .env.example .env
# Edit .env with your API keys

# 3. Initialize database
task db:init

# 4. Run the application
task run:dev
```

### Daily Development

```bash
# Start development servers
task run:dev

# In another terminal, fetch latest data
task data:fetch
```

### Before Committing

```bash
# Format code
task format:backend

# Check for issues
task lint:backend

# Run tests
task test:backend
```

### Database Changes

```bash
# 1. Modify models in backend/app/models/
# 2. Create migration
task db:migrate:create -- "describe your changes"

# 3. Review migration file
# 4. Apply migration
task db:migrate

# If something goes wrong
task db:migrate:rollback
```

---

## Environment Variables

Tasks respect `.env` configuration:

```bash
# backend/.env
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ENVIRONMENT=development
DEBUG=true
```

Make sure `.env` is configured before running tasks.

---

## Troubleshooting

### "Task not found"

**Solution**: Make sure you're in the project root directory.

```bash
cd /path/to/quant-crew
task --list
```

### "Command not found: uv"

**Solution**: Install uv package manager.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### "Database connection failed"

**Solution**:
1. Check PostgreSQL is running
2. Verify `DATABASE_URL` in `.env`
3. Test connection: `psql $DATABASE_URL`

### "Dependencies out of sync"

**Solution**: Force dependency reinstall.

```bash
cd backend
rm -rf .venv
task setup:backend
```

---

## Creating Custom Tasks

Add tasks to `Taskfile.yml`:

```yaml
# Example: Custom data export task
data:export:
  desc: "Export data to CSV"
  deps: [setup:backend]
  dir: backend
  cmds:
    - uv run python scripts/export_data.py
```

Then run:
```bash
task data:export
```

---

## Task Features Used

### Dependencies
```yaml
deps: [setup:backend]  # Runs setup:backend first
```

### File Watching
```yaml
sources:
  - pyproject.toml
  - uv.lock
generates:
  - .venv/pyvenv.cfg
```
Task only runs if sources changed.

### Working Directory
```yaml
dir: backend  # Changes to backend/ before running
```

### Command Line Arguments
```bash
task db:migrate:create -- "my migration message"
```
Access via `{{.CLI_ARGS}}` in task.

---

## Advanced Usage

### Run Specific Task Without Dependencies

```bash
task --force run:backend  # Skip setup:backend dependency
```

### Parallel Execution

```bash
# Already built into run:dev
task --parallel run:backend run:frontend
```

### List Task Commands

```bash
# See what commands a task will run
task --dry run:backend
```

### Task Summary

```bash
# Show detailed info about a task
task --summary db:init
```

---

## See Also

- [Main README](./README.md) - Project overview
- [Backend Documentation](./backend/docs/INDEX.md) - Backend architecture
- [Scripts Documentation](./backend/scripts/README.md) - Script details
- [Taskfile Documentation](https://taskfile.dev/) - Official Taskfile docs

---

**Pro Tip**: Add shell completion for task commands!

```bash
# Bash
task --completion bash >> ~/.bashrc

# Zsh
task --completion zsh >> ~/.zshrc

# Fish
task --completion fish > ~/.config/fish/completions/task.fish
```

Then restart your shell and type `task <TAB>` for autocomplete! 🎉
