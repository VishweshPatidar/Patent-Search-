@echo off
echo Starting Technical Document Search Platform - Both Services
echo.
echo Starting backend on port 8000...
start "Backend Server" cmd /k "cd backend && call .venv\Scripts\activate && python -m uvicorn app:app --host 0.0.0.0 --port 8000"

echo.
echo Starting frontend on port 3000...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul
