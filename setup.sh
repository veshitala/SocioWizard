#!/bin/bash

echo "🚀 Setting up SocioWizard - AI UPSC Sociology Mentor"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Backend setup
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file
echo "Creating environment file..."
cat > .env << EOF
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
DATABASE_URL=sqlite:///sociowizard.db
EOF

echo "✅ Backend setup complete!"

# Frontend setup
echo ""
echo "🔧 Setting up Frontend..."
cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

# Create start script
echo ""
echo "📝 Creating start script..."
cd ..
cat > start.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting SocioWizard..."

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ SocioWizard is starting up!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait $BACKEND_PID $FRONTEND_PID
EOF

chmod +x start.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "  ./start.sh"
echo ""
echo "Or start manually:"
echo "  Backend: cd backend && source venv/bin/activate && python app.py"
echo "  Frontend: cd frontend && npm start"
echo ""
echo "Default demo credentials:"
echo "  Username: demo_user"
echo "  Password: (any password will work for demo)"
echo ""
echo "Happy studying! 📚" 