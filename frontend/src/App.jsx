import React, { useState, useRef, useEffect } from 'react';
import { Upload, MessageSquare, Send, FileUp } from 'lucide-react';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [documents, setDocuments] = useState([]);
  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

   const fetchDocuments = async () => {
   try {
      const response = await fetch('http://localhost:8000/documents');
      const data = await response.json();
      // If documents is directly an array, use it as is
      // If it's in a documents property, extract it
      setDocuments(Array.isArray(data) ? data : data.documents || []);
   } catch (error) {
      console.error('Error fetching documents:', error);
   }
   };
  useEffect(() => {
    fetchDocuments();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setUploadStatus('Uploading...');

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus(`Successfully uploaded ${file.name}`);
        setMessages(prev => [...prev, {
          type: 'system',
          content: `Document "${file.name}" has been uploaded and indexed.`
        }]);
        fetchDocuments(); // Refresh document list
      } else {
        setUploadStatus('Upload failed');
      }
    } catch (error) {
      setUploadStatus('Upload failed: ' + error.message);
    }
  };

  const handleDeleteDocument = async (filename) => {
   try {
     console.log(`Attempting to delete: ${filename}`);
     const response = await fetch(`http://localhost:8000/document/${filename}`, {
       method: 'DELETE',
       headers: {
         'Content-Type': 'application/json'
       }
     });
 
     console.log('Delete response status:', response.status);
 
     if (!response.ok) {
       throw new Error(`HTTP error! status: ${response.status}`);
     }
 
     const data = await response.json();
     console.log('Delete response:', data);
 
     fetchDocuments(); // Refresh the list
     setMessages(prev => [...prev, {
       type: 'system',
       content: `Document "${filename}" has been deleted.`
     }]);
   } catch (error) {
     console.error('Error deleting document:', error);
     setMessages(prev => [...prev, {
       type: 'error',
       content: `Failed to delete "${filename}": ${error.message}`
     }]);
   }
 };
 
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setInputMessage('');
    setIsLoading(true);

    try {
        // Add console.log to see what's happening
      console.log('Sending request to:', 'http://localhost:8000/query');
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage }),
      });

        // Log the response status
      console.log('Response status:', response.status);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Response data:', data);

      setMessages(prev => [...prev, {
        type: 'bot',
        content: data.content,
        metrics: data.metrics
      }]);
    } catch (error) {
      console.error('Error details:', error);  // Log the full error
      setMessages(prev => [...prev, {
        type: 'error',
        content: `Error: ${error.message}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 p-4 bg-gray-100 rounded-lg">
        <h1 className="text-xl font-bold">RAG Chat</h1>
        <div className="flex items-center gap-4">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            <FileUp size={20} />
            Upload Document
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            className="hidden"
            accept=".pdf,.sv,.v,.txt"
          />
        </div>
      </div>

      {/* Upload Status */}
      {uploadStatus && (
        <div className="mb-4 p-2 text-sm text-gray-600 bg-gray-100 rounded">
          {uploadStatus}
        </div>
      )}

      {/* Document List */}
      <div className="mb-4 p-2 bg-gray-100 rounded">
        <h2 className="font-bold mb-2">Uploaded Documents:</h2>
        <div className="flex flex-wrap gap-2">
          {documents.map((doc,index) => (
            <div key={`doc-${index}-${doc.filename}`} className="flex items-center gap-2 bg-white p-2 rounded shadow">
              <span>{doc.filename}</span>
              <button
                onClick={() => handleDeleteDocument(doc.filename)}
                className="text-red-500 hover:text-red-700"
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-50 rounded-lg">
        {messages.map((message, index) => (
          <div
            ///key={index}
            key={`message-${index}-${message.type}`}  // More unique key
            className={`mb-4 ${
              message.type === 'user' 
                ? 'ml-auto max-w-[80%]' 
                : 'mr-auto max-w-[80%]'
            }`}
          >
            <div
              className={`p-3 rounded-lg ${
                message.type === 'user'
                  ? 'bg-blue-500 text-white'
                  : message.type === 'system'
                  ? 'bg-gray-200 text-gray-800'
                  : message.type === 'error'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-white border border-gray-200'
              }`}
            >
              {message.content}
              {message.metrics && (
                <div className="mt-2 text-xs text-gray-500 border-t pt-2">
                  <div>Total Duration: {(message.metrics.total_duration / 1e9).toFixed(2)}s</div>
                  <div>Eval Count: {message.metrics.eval_count}</div>
                  <div>Prompt Tokens: {message.metrics.prompt_eval_count}</div>
                  <div>Eval Duration: {(message.metrics.eval_duration / 1e9).toFixed(2)}s</div>
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="flex gap-2 p-2 bg-white border rounded-lg">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Type your message..."
          className="flex-1 p-2 focus:outline-none"
        />
        <button
          onClick={handleSendMessage}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors disabled:bg-gray-400"
        >
          {isLoading ? 'Sending...' : <Send size={20} />}
        </button>
      </div>
    </div>
  );
};

export default App;