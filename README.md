# Document Classifier

A full-stack application that classifies legal documents into three categories:
- Stock Purchase Agreement (SPA)
- Certificate of Incorporation (COI) 
- Investors' Rights Agreement (IRA)


## Project Structure
```

document_classifier/
├── backend/
│   ├── classify.py          \# Flask server with classification logic
│   └── requirements.txt     \# Python dependencies
.
.
.
└── src/
│   ├── App.jsx          \# Main React component
│   ├── App.css          \# Styling
│   ├──main.jsx         \# React entry point
.
.
.

```

## Features
- File upload for PDF and DOCX documents
- Document preview functionality
- Document classification 

## Installation

### Backend Setup
```

cd document_classifier/backend
pip install -r requirements.txt

```

### Frontend Setup
```

cd document_classifier/
npm install

```

## Running the Application

### Start Backend Server (Flask)
```

cd document_classifier/backend
python classify.py

```
Server runs at `http://localhost:5000`

### Start Frontend (React)
```

cd document_classifier/
npm run dev

```
Access at `http://localhost:5173`

## Technical Details

### Backend Logic (`classify.py`)
1. **Text Extraction**:
   - PDF: Uses `PyPDF2` for text extraction
   - DOCX: Uses `python-docx` for paragraph parsing

2. **Classification Patterns**:
```

patterns = {
"Stock Purchase Agreement": [
r"\b(purchase\s+and\s+sale\s+of\s+shares",
r"\bclosing\s+conditions\b",
r"\brepresentations\s+and\s+warranties\b"
],
"Certificate of Incorporation": [
r"\barticles\s+of\s+incorporation\b",
r"\bauthorized\s+shares\b",
r"\bdelaware\s+general\s+corporation\s+law\b"
],
"Investors' Rights Agreement": [
r"\bregistration\s+rights\b",
r"\bright\s+of\s+first\s+refusal\b",
r"\bdrag-along\s+rights\b"
]
}

```

3. **Scoring System**:
   - Exact matches: 2 points
   - Partial matches: 1 point
   - Minimum 3 points required for classification

### Frontend Components
- **App.jsx**:
  - File upload handling
  - Document preview (PDF/DOCX)
  - API communication with backend
  - Result display

- **App.css**:
  - Preview styling for both PDF and DOCX
  - Error and loading states

