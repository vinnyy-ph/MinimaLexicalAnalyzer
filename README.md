# Minima

### Installation

1.  **Create a virtual environment:** This isolates project dependencies.

    *   **CMD/PowerShell:**
        ```bash
        python -m venv venv
        ```

2.  **Activate the virtual environment:**

    *   **CMD/PowerShell:**
        ```bash
        venv\Scripts\activate
        ```

3.  **Install required Python packages:**

    *   **CMD/PowerShell:**
        ```bash
        python -m pip install -r requirements.txt
        ```

4.  **Install required Node.js packages (frontend):**

    *   **CMD/PowerShell:**
        ```bash
        cd frontend
        npm install --force  # or npm ci for a clean install
        ```

## Running the Program

This section explains how to start the application. Note: Always start a new powershell/command prompt window for each step.

### Frontend

1.  Navigate to the frontend directory:

    *   **CMD/PowerShell:**
        ```bash
        cd frontend
        ```

2.  Start the development server:

    *   **CMD/PowerShell:**
        ```bash
        npm start
        ```

### Backend (Lexer)

1.  Navigate to the backend directory:

    *   **CMD/PowerShell:**
        ```bash
        cd backend
        ```

2.  Run the Python application:

    *   **CMD/PowerShell:**
        ```bash
        python app.py
        ```
