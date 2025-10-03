@echo off
echo Starting Technical Document Search Platform - Backend
cd backend
call .venv\Scripts\activate
python -m uvicorn app:app --host 0.0.0.0 --port 8000
pause
