@echo off
echo Setting up Python virtual environment...

REM Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
cd backend
pip install -r requirements.txt

echo Backend setup complete!
echo To start the backend server, run: run.bat backend
echo To start the frontend server, run: run.bat frontend
echo To start both servers, run: run.bat

pause
