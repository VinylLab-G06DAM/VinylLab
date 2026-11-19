# VinylLab

Repositorio de VinylLab — a FastAPI-based API for managing vinyl records.

## Setup Guide: Python Virtual Environment & Dependencies

Using a virtual environment (`venv`) isolates project dependencies from your global Python installation and avoids version conflicts.

### 1. Prerequisites

Make sure Python 3 is installed:

```bash
python3 --version
```

*(On Windows, you can also use `python --version` or `py --version`.)*

### 2. Create a Virtual Environment

Run this command from the project root directory (`VinylLab`):

- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  ```
- **Windows:**
  ```bash
  python -m venv .venv
  ```

> `.venv` is listed in `.gitignore`, so it will not be committed to Git.

### 3. Activate the Virtual Environment

- **Linux / macOS (bash/zsh):**
  ```bash
  source .venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(If PowerShell blocks script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once.)*
- **Windows (Command Prompt / CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

Once activated, your terminal prompt will show `(.venv)` at the beginning. You can verify you are using the virtual environment's Python with:

```bash
which python   # Linux / macOS
where python   # Windows
```

### 4. Upgrade `pip` and Install Requirements

With the virtual environment activated, upgrade `pip` and install the packages from `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the Application

Start the FastAPI development server with Uvicorn:

```bash
uvicorn main:app --reload
```

Then open in your browser:
- API root: http://127.0.0.1:8000/
- Interactive API docs (Swagger UI): http://127.0.0.1:8000/docs

### 6. Deactivate the Virtual Environment

When you finish working on the project, exit the virtual environment by running:

```bash
deactivate
```
