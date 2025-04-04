from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from docx import Document
import re
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_text(file):
    text = ""
    try:
        if file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in pdf_reader.pages])
        elif file.filename.endswith('.docx'):
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text

def classify_document(text):
    text = text.lower()
    
    # Define semantic patterns for each document type
    patterns = {
        "Stock Purchase Agreement": [
            r"\b(purchase\s+and\s+sale\s+of\s+shares|closing\s+conditions|representations\s+and\s+warranties|"
            r"preferred\s+stock\s+purchase|escrow\s+arrangements|indemnification\s+provisions|"
            r"closing\s+deliverables|subscription\s+amount|definitive\s+agreement)\b",
            r"\b(conditions\s+precedent|survival\s+period|bring-down\s+certificate|material\s+adverse\s+effect|"
            r"lock-up\s+provisions|post-closing\s+covenants)\b"
        ],
        "Certificate of Incorporation": [
            r"\b(articles\s+of\s+incorporation|authorized\s+shares|par\s+value|corporate\s+existence|"
            r"board\s+of\s+directors\s+election|fiscal\s+year|stockholder\s+meetings|"
            r"delaware\s+general\s+corporation\s+law|amendment\s+procedures)\b",
            r"\b(preemptive\s+rights\s+exclusion|dividend\s+preferences|liquidation\s+preference|"
            r"antidilution\s+protections|redemption\s+rights|voting\s+power\s+structure)\b"
        ],
        "Investors' Rights Agreement": [
            r"\b(registration\s+rights|demand\s+registration|piggyback\s+registration|"
            r"right\s+of\s+first\s+refusal|co-sale\s+agreement|drag-along\s+rights|"
            r"information\s+rights|board\s+observation\s+rights|voting\s+agreement)\b",
            r"\b(lock-up\s+agreement|termination\s+of\s+rights|assignability\s+of\s+rights|"
            r"most\s+favored\s+nation|fn\s+round\s+provisions|waiver\s+of\s+corporate\s+opportunity)\b"
        ]
    }

    # Score matches with weights for key terms
    scores = defaultdict(int)
    for doc_type, doc_patterns in patterns.items():
        for pattern in doc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            # Weight exact phrases higher than partial matches
            scores[doc_type] += len(matches) * (2 if '\\b' in pattern else 1)

    # Classify based on highest score with minimum threshold
    max_score = max(scores.values())
    if max_score < 3:  # Minimum confidence threshold
        return "Not any type"
    
    return max(scores, key=scores.get)


@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty file"}), 400

    text = extract_text(file)
    if not text:
        return jsonify({"error": "Could not extract text"}), 400

    try:
        doc_type = classify_document(text)
        return jsonify({
            "document_type": doc_type
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
