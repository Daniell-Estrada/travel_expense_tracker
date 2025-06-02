# Travel Expense Tracker

A simple application to track travel expenses with a FastAPI backend and a React + Vite frontend. This README explains how to install dependencies, set up environment variables, and run both the backend (API and console) and the frontend.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)

  - [Backend `.env` file](#backend-env-file)
  - [Frontend `.env` file](#frontend-env-file)

- [Running the Backend](#running-the-backend)

  - [1. API Mode](#1-api-mode)
  - [2. Console Mode](#2-console-mode)

- [Running the Frontend](#running-the-frontend)
- [Running Tests](#running-tests)
- [Notes](#notes)

---

## Prerequisites

- **Python 3.10 or higher**
- **Node.js 18+** and **npm** (or **Yarn**)
- **MySQL** (or another database compatible with the connector in `requirements.txt`)
- Basic understanding of Python and JavaScript/TypeScript

---

## Project Structure

```
travel_expense_tracker/
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── main.py                    ← Console application entry point
│   ├── presentation/
│   │   ├── api/
│   │   │   └── main_api.py        ← FastAPI backend entry point
│   │   └── console/
│   │       └── console_interface.py
│   ├── application/
│   ├── core/
│   ├── config/
│   └── infrastructure/
├── frontend/                      ← React + Vite frontend
│   ├── package.json
│   ├── index.html
│   └── src/
│       └── ...
└── tests/
    ├── unit/
    └── infrastructure/
```

- `pyproject.toml` and `requirements.txt`: Define backend dependencies.
- `src/presentation/api/main_api.py`: Run the backend as a web API.
- `src/main.py`: Run the backend as a console application.
- `frontend/`: A standard Vite + React + TypeScript app.
- `tests/`: Unit and integration tests for backend logic.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your_username/travel_expense_tracker.git
   cd travel_expense_tracker
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install backend dependencies**
   Make sure you are in the project root (where `pyproject.toml` and `requirements.txt` live).

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   > **Tip:** The `pyproject.toml` file defines packaging settings. If you prefer, you can install the project in editable mode:
   >
   > ```bash
   > pip install -e .
   > ```
   >
   > This ensures that if you change any source file, you don’t need to reinstall.

4. **Install frontend dependencies**

   ```bash
   cd frontend
   npm install
   # or
   # yarn install
   cd ..
   ```

---

## Environment Variables

Both backend and frontend rely on environment variables defined in `.env` files. Place these at the project root (for the backend) and inside `frontend/` (for the frontend).

### Backend `.env` file

Create a file named `.env` in the project root (same level as `pyproject.toml`), and add:

```
# Database Configuration
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

# Currency API configuration
API_URL=
```

- **DB_HOST**: Hostname or IP of your database server (e.g., `localhost`).
- **DB_PORT**: Database port (e.g., `3306` for MySQL).
- **DB_NAME**: Name of the database (e.g., `travel_expenses`).
- **DB_USER**: Database username.
- **DB_PASSWORD**: Database password.
- **API_URL**: URL of an external currency conversion API (if needed by the app).

_Example:_

```ini
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=travel_expenses
DB_USER=root
DB_PASSWORD=my-secret-password

API_URL=https://api.exchangerate.host/latest
```

### Frontend `.env` file

Create a file named `.env` inside the `frontend/` directory:

```
VITE_API_BASE_URL=
```

- **VITE_API_BASE_URL**: The base URL where the FastAPI backend is running.

  - If you run the API on `http://localhost:8000`, set:

    ```
    VITE_API_BASE_URL=http://localhost:8000/api/v1
    ```

---

## Running the Backend

There are two ways to start the backend:

1. **API Mode (FastAPI)**
2. **Console Mode**

### 1. API Mode

This mode will launch a FastAPI server. It serves REST endpoints for managing expenses, trips, reports, and dashboards.

1. Make sure your `.env` file is configured.

2. Install dependencies (see [Installation](#installation)).

3. Run the API with Uvicorn (from the project root):

   ```bash
   uvicorn src.presentation.api.main_api:app --reload
   ```

   Or directly via Python:

   ```bash
   python src/presentation/api/main_api.py
   ```

4. Open your browser and go to `http://127.0.0.1:8000/docs` to see the interactive Swagger UI.

> **Note:**
>
> - `--reload` enables live code reload on changes.
> - If you have a different host or port, specify flags:
>
>   ```bash
>   uvicorn src.presentation.api.main_api:app --reload --host 0.0.0.0 --port 8080
>   ```

### 2. Console Mode

This mode runs the application purely in the console, without any HTTP server. You can manually interact with it through text prompts.

1. Make sure your `.env` file is configured.

2. Install dependencies (see [Installation](#installation)).

3. Run:

   ```bash
   python src/main.py
   ```

4. Follow the on-screen prompts to add trips, expenses, and generate reports directly in your terminal.

---

## Running the Frontend

The frontend is a React + Vite application. Make sure the backend API is running (e.g., at `http://localhost:8000`) before starting the frontend.

1. Go to the `frontend/` folder:

   ```bash
   cd frontend
   ```

2. Create or update the `.env` file inside `frontend/` (see [Environment Variables](#frontend-env-file)).

3. Install dependencies if you haven’t yet:

   ```bash
   npm install
   # or
   # yarn install
   ```

4. Start the development server:

   ```bash
   npm run dev
   # or
   # yarn dev
   ```

5. Open your browser and go to the URL shown in the console (usually `http://localhost:5173`). The React app will connect to the FastAPI backend.

---

## Running Tests

There are both unit tests and integration tests using `pytest`.

1. Make sure dependencies are installed.
2. From the project root, run:

   ```bash
   pytest
   ```

Tests are organized under the `tests/` folder:

- **`tests/unit/`**: Unit tests for core services.
- **`tests/infrastructure/`**: Tests for external dependencies like API clients.

---

## Notes

- **`pyproject.toml`**: Defines packaging configuration. You can install the project in editable mode with `pip install -e .`. This makes it easier to develop, as changes to source files will take effect immediately without reinstalling.
- **Database Setup**: Ensure your database is running and you have created the schema/tables before starting the backend.
- **Port Conflicts**: If port `8000` or `5173` is already in use, adjust the `uvicorn` command (for backend) or Vite config (for frontend) accordingly.
- **Linting & Formatting**: The frontend includes ESLint and TypeScript configuration by default. You can extend or modify those settings as needed.
- **Contributing**: Feel free to open issues or submit pull requests. Make sure you run tests and add new tests for any new features.

---
