@echo off
echo Setting up Technical Document Search Platform with Milvus...

echo.
echo Step 1: Starting Milvus vector database...
docker-compose up -d
echo Waiting for Milvus to start...
timeout /t 15 /nobreak > nul

echo.
echo Step 2: Setting up Python backend...
cd backend
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Step 3: Fetching real data and loading to Milvus...
python real_data_integration.py
python data_loader.py

echo.
echo Step 4: Setting up frontend...
cd ..\frontend
npm install

echo.
echo Setup complete! 
echo.
echo To start: Run start_all.bat
echo Or manually: start_backend.bat + start_frontend.bat
echo.
echo Note: Milvus is running in Docker (ports 19530, 2379, 9000)
echo.
pause
