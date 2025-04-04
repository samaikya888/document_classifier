import React, { useState } from 'react';
import './App.css';
import * as mammoth from 'mammoth'; // Add DOCX text extraction

const App = () => {
  const [file, setFile] = useState(null);
  const [previewContent, setPreviewContent] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    setFile(uploadedFile);

    // Preview handling
    if (uploadedFile?.type === 'application/pdf') {
      setPreviewContent(URL.createObjectURL(uploadedFile));
    } else if (uploadedFile?.name.endsWith('.docx')) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const arrayBuffer = e.target.result;
        const result = await mammoth.extractRawText({ arrayBuffer });
        setPreviewContent(result.value);
      };
      reader.readAsArrayBuffer(uploadedFile);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:5000/classify', {
        method: 'POST',
        body: formData,
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Classification failed" });
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Document Classifier</h1>
      <input
        type="file"
        accept="application/pdf,.docx"
        onChange={handleFileUpload}
      />

      {file && (
        <div className="preview-section">
          <h2>Preview</h2>
          {file.type === 'application/pdf' ? (
            <embed
              className="pdf-preview"
              src={previewContent}
              type="application/pdf"
            />
          ) : (
            <div className="docx-preview">
              <pre>{previewContent}</pre>
            </div>
          )}
        </div>
      )}

      <button onClick={handleSubmit} disabled={!file || loading}>
        {loading ? 'Analyzing...' : 'Classify Document'}
      </button>

      {result && (
        <div className="results">
          {result.error ? (
            <div className="error">{result.error}</div>
          ) : (
            <>
              <h2>Classification Result</h2>
              <div className="document-type">
                Type: <span>{result.document_type}</span>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
