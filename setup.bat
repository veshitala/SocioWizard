@echo off
echo 🚀 Setting up SocioWizard - AI UPSC Sociology Mentor
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Python and Node.js are installed

REM Backend setup
echo.
echo 🔧 Setting up Backend...
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file
echo Creating environment file...
(
echo SECRET_KEY=your-secret-key-change-in-production
echo JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
echo DATABASE_URL=sqlite:///sociowizard.db
) > .env

echo ✅ Backend setup complete!

REM Frontend setup
echo.
echo 🔧 Setting up Frontend...
cd ..\frontend

REM Install dependencies
echo Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!

REM Create start script
echo.
echo 📝 Creating start script...
cd ..
(
echo @echo off
echo echo 🚀 Starting SocioWizard...
echo echo.
echo echo Starting backend server...
echo cd backend
echo call venv\Scripts\activate.bat
echo start python app.py
echo.
echo echo Starting frontend server...
echo cd ..\frontend
echo start npm start
echo.
echo echo ✅ SocioWizard is starting up!
echo echo Backend: http://localhost:5000
echo echo Frontend: http://localhost:3000
echo echo.
echo echo Press any key to exit...
echo pause
) > start.bat

echo.
echo 🎉 Setup complete!
echo.
echo To start the application:
echo   start.bat
echo.
echo Or start manually:
echo   Backend: cd backend ^&^& venv\Scripts\activate.bat ^&^& python app.py
echo   Frontend: cd frontend ^&^& npm start
echo.
echo Default demo credentials:
echo   Username: demo_user
echo   Password: ^(any password will work for demo^)
echo.
echo Happy studying! 📚
pause 