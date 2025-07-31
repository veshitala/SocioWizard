# UPSC Sociology Mentor

An AI-powered web application designed to help UPSC aspirants master sociology through intelligent answer practice and evaluation.

## Features

### Frontend (React + Tailwind CSS)
- **Dashboard**: Clean, minimalist interface with sidebar navigation
- **Answer Practice**: Random PYQ generation with text editor and file upload
- **Evaluation**: AI-powered answer assessment with detailed feedback
- **Progress Tracking**: Visual timeline and progress graphs
- **PYQ Database**: Categorized previous year questions by theme and year

### Backend (Python Flask)
- **User Authentication**: Secure login/signup system
- **Answer Management**: Store and retrieve user answers with metadata
- **PYQ Service**: Serve categorized questions from database
- **AI Evaluation**: ChatGPT integration for intelligent answer assessment
- **File Upload**: Support for PDF, DOCX, and DOC answer uploads
- **AI Suggestions**: Real-time recommendations for answer improvement

### AI-Powered Features
- **ChatGPT Integration**: Advanced answer evaluation using OpenAI's GPT-4
- **File Processing**: Automatic text extraction from uploaded documents
- **Smart Feedback**: Detailed analysis with strengths and improvement areas
- **Keyword Extraction**: Automatic identification of sociological concepts
- **Thinker Recognition**: Detection of sociological thinkers mentioned
- **Theory Analysis**: Identification of sociological theories referenced

### Bonus Features
- **Flashcards**: Interactive learning from PYQ themes
- **Daily Tips**: Motivational quotes and sociology facts
- **Topic Tagging**: Automatic categorization using NLP
- **Topper Analysis**: Compare answers with model responses

## Project Structure

```
SocioWizard/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
├── backend/                 # Flask API server
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic (including ChatGPT)
│   │   └── utils/          # Helper functions
│   ├── uploads/            # File upload storage
│   ├── requirements.txt    # Python dependencies
│   └── README_SETUP.md     # ChatGPT setup guide
└── README.md              # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ and npm installed
- Git (for cloning the repository)
- OpenAI API key (for ChatGPT features)

### Quick Start (macOS/Linux)
1. Clone the repository: `git clone <repository-url>`
2. Navigate to project: `cd SocioWizard`
3. Run setup script: `chmod +x setup.sh && ./setup.sh`
4. Configure ChatGPT API (see ChatGPT Setup below)
5. Start both services: `./start.sh`

### ChatGPT Setup (Optional but Recommended)
1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Create `.env` file in backend directory:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```
3. See `backend/README_SETUP.md` for detailed setup instructions

### Manual Setup

#### Backend Setup
1. Navigate to backend directory: `cd backend`
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize database: `python init_db.py`
6. (Optional) Configure ChatGPT API key in `.env` file
7. Run the server: `python app.py`
   - **Note**: Backend runs on port 5001 (not 5000 due to macOS AirPlay conflict)

#### Frontend Setup
1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start development server: `npm start`
   - Frontend will run on http://localhost:3000

### Windows Setup
1. Clone the repository: `git clone <repository-url>`
2. Navigate to project: `cd SocioWizard`
3. Run setup script: `setup.bat`
4. Configure ChatGPT API (optional)
5. Start both services: `start.bat`

### Accessing the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001
- **Demo Login**: 
  - Username: `demo_user`
  - Password: `demo123`

## New Features

### File Upload Support
- Upload PDF, DOCX, or DOC files containing your answers
- Automatic text extraction and AI evaluation
- Download uploaded files for reference
- Support for handwritten and typed answers

### AI-Powered Evaluation
- **ChatGPT Integration**: Advanced evaluation using GPT-4
- **Detailed Feedback**: Structure, content, and theoretical analysis
- **Strengths & Improvements**: Specific areas to focus on
- **Keyword Analysis**: Automatic concept identification
- **Thinker Recognition**: Detection of sociological thinkers
- **Theory Analysis**: Identification of sociological theories

### AI Suggestions
- Real-time recommendations while writing answers
- Structure, content, and theoretical suggestions
- Examples and concepts to include
- Thinkers and theories to mention

### Fallback Mode
- Works without ChatGPT API (basic evaluation)
- Graceful degradation when API is unavailable
- No interruption to core functionality

## Troubleshooting

#### Port 5000 Already in Use (macOS)
If you see "Connection refused" on port 5000, this is because macOS uses port 5000 for AirPlay. The application is configured to use port 5001 instead.

#### Database Issues
If you encounter database errors:
1. Delete the `backend/instance/sociowizard.db` file
2. Run `python init_db.py` again to recreate the database

#### ChatGPT API Issues
1. Ensure your API key is correct and has sufficient credits
2. Check the `.env` file is in the backend directory
3. The app will work with basic evaluation if ChatGPT is unavailable

#### File Upload Issues
1. Ensure files are PDF, DOCX, or DOC format
2. Check file size (recommended under 5MB)
3. Some PDFs with images may not extract text properly

#### Import Errors
If you see "ImportError: cannot import name 'db'", ensure you're running the backend from the correct directory:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

#### Frontend Can't Connect to Backend
Ensure both services are running:
- Backend should show: "Running on http://127.0.0.1:5001"
- Frontend should show: "Local: http://localhost:3000"

## Technology Stack

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Styling framework
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API calls
- **Recharts** - Data visualization charts
- **Lucide React** - Icon library
- **clsx & tailwind-merge** - Conditional styling utilities

### Backend
- **Python Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **SQLite** - Development database
- **python-dotenv** - Environment variable management

### Development Tools
- **Virtual Environment** - Python dependency isolation
- **npm** - Node.js package management
- **PostCSS & Autoprefixer** - CSS processing

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/questions/random` - Get random PYQ
- `POST /api/answers/submit` - Submit answer for evaluation
- `GET /api/answers/history` - Get user's answer history
- `GET /api/progress/summary` - Get progress statistics

## Project Architecture

### Backend Architecture
- **Modular Design**: Blueprint-based routing for scalability
- **Database Models**: SQLAlchemy ORM with relationships
- **Authentication**: JWT-based with bcrypt password hashing
- **API Structure**: RESTful endpoints with proper error handling
- **Extension Pattern**: Centralized Flask extensions to avoid circular imports

### Frontend Architecture
- **Component-Based**: Reusable React components
- **Context API**: Global state management for authentication
- **Service Layer**: Axios-based API services with interceptors
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Chart Integration**: Recharts for data visualization

## Recent Updates & Fixes

### v1.1.0 - Port Configuration & Import Fixes
- **Fixed**: Circular import issues in Flask backend
- **Changed**: Backend port from 5000 to 5001 (macOS AirPlay conflict)
- **Added**: Centralized extensions module (`extensions.py`)
- **Improved**: Database initialization process
- **Enhanced**: Error handling and troubleshooting documentation

### v1.0.0 - Initial Release
- **Complete**: Full-stack UPSC Sociology Mentor application
- **Features**: User authentication, answer practice, evaluation, progress tracking
- **Database**: Sample PYQs and demo user account
- **UI/UX**: Modern, responsive interface with Tailwind CSS

## Development Roadmap

- [x] Project structure setup
- [x] Basic authentication system
- [x] Dashboard UI components
- [x] Answer practice interface
- [x] Evaluation system (placeholder)
- [x] Progress tracking with charts
- [x] PYQ database integration
- [x] Port configuration fixes
- [x] Import error resolution
- [ ] AI integration for answer evaluation
- [ ] File upload functionality
- [ ] Topic tagging system
- [ ] Advanced analytics dashboard 