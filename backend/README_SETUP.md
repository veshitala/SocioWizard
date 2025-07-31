# ChatGPT Integration & File Upload Setup Guide

## Overview
This guide explains how to set up ChatGPT API integration and file upload functionality for the SocioWizard application.

## Features Added

### 1. ChatGPT API Integration
- AI-powered answer evaluation using OpenAI's GPT-4
- Intelligent feedback generation
- Keyword, thinker, and theory extraction
- Strengths and areas for improvement analysis

### 2. File Upload Support
- PDF, DOCX, and DOC file upload
- Automatic text extraction from uploaded files
- AI evaluation of uploaded answers
- File download functionality

### 3. AI Suggestions
- Real-time suggestions for answer improvement
- Structure, content, and theoretical recommendations
- Examples and concepts to include

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure OpenAI API
Create a `.env` file in the backend directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
DATABASE_URL=sqlite:///sociowizard.db

# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Optional: Configure OpenAI model (default: gpt-4)
# OPENAI_MODEL=gpt-3.5-turbo
```

### 3. Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and paste it in your `.env` file

### 4. Create Upload Directory
The application will automatically create an `uploads` directory, but you can create it manually:
```bash
mkdir backend/uploads
```

### 5. Start the Application
```bash
cd backend
python app.py
```

## Usage

### Text Answer Evaluation
1. Go to the Answer Practice page
2. Write your answer in the text editor
3. Click "Submit for Evaluation"
4. View AI-powered feedback and scores

### File Upload Evaluation
1. Go to the Answer Practice page
2. Upload a PDF, DOCX, or DOC file containing your answer
3. Click "Upload & Evaluate"
4. View AI-powered feedback and scores

### AI Suggestions
1. Write your answer in the text editor
2. Click "AI Suggestions" button
3. View personalized recommendations for improvement

## API Endpoints

### File Upload
- `POST /api/file-upload/upload-answer` - Upload and evaluate answer file
- `POST /api/file-upload/get-suggestions` - Get AI suggestions for answer
- `GET /api/file-upload/download/<answer_id>` - Download uploaded file

### Enhanced Evaluation
- All existing evaluation endpoints now use ChatGPT when available
- Fallback to basic evaluation if ChatGPT is not configured

## File Support

### Supported Formats
- **PDF**: Handwritten or typed answers
- **DOCX**: Microsoft Word documents
- **DOC**: Legacy Word documents

### File Size Limits
- Maximum file size: 10MB
- Recommended: Under 5MB for faster processing

## Troubleshooting

### ChatGPT API Issues
1. **API Key Error**: Ensure your OpenAI API key is correct and has sufficient credits
2. **Rate Limiting**: The app includes fallback evaluation if API calls fail
3. **Model Issues**: Check if the specified model is available in your OpenAI account

### File Upload Issues
1. **File Type Error**: Ensure file is PDF, DOCX, or DOC format
2. **Text Extraction Error**: Some PDFs with images may not extract text properly
3. **File Size**: Reduce file size if upload fails

### Performance Optimization
1. Use `gpt-3.5-turbo` instead of `gpt-4` for faster responses
2. Implement caching for repeated evaluations
3. Consider batch processing for multiple files

## Security Considerations

1. **API Key Security**: Never commit your `.env` file to version control
2. **File Upload**: Implement virus scanning for uploaded files in production
3. **Data Privacy**: Consider data retention policies for uploaded files
4. **Rate Limiting**: Implement rate limiting for API endpoints

## Cost Optimization

1. **Model Selection**: Use `gpt-3.5-turbo` for cost-effective evaluation
2. **Token Management**: Monitor API usage and implement caching
3. **Batch Processing**: Group multiple evaluations to reduce API calls

## Future Enhancements

1. **Multi-language Support**: Extend evaluation to other languages
2. **Advanced Analytics**: Detailed performance tracking and insights
3. **Custom Prompts**: Allow users to customize evaluation criteria
4. **Offline Mode**: Enhanced fallback evaluation without API dependency 