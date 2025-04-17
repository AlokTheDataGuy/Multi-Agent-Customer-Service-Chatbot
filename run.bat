@echo off
setlocal

REM Check if we need to build the frontend
if "%1"=="build" (
    echo Building frontend...
    cd frontend
    call npm install
    call npm run build
    cd ..
    goto :eof
)

REM Start the backend and frontend servers
if "%1"=="backend" (
    echo Starting backend server...
    cd backend
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    goto :eof
)

if "%1"=="frontend" (
    echo Starting frontend server...
    cd frontend
    call npm run dev
    goto :eof
)

REM If no specific service is specified, start both
if "%1"=="" (
    echo Starting both backend and frontend servers...
    
    REM Start backend in a new window
    start cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    
    REM Start frontend
    cd frontend
    call npm run dev
)

endlocal
