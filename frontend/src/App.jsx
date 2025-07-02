import React, { useState } from 'react';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  const handleGenerateContent = async () => {
    setLoading(true);
    setResult('');
    
    try {
      console.log('🚀 Generate Practice Content button clicked!');
      
      const response = await fetch('/api/learners/1/generate-content', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify({
          concept: 'Content Marketing',
          content_type: 'lesson'
        })
      });
      
      if (response.ok) {
        const content = await response.json();
        setResult(`✅ Generated: ${content.concept || 'Content generated successfully!'}`);
        console.log('Generated content:', content);
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      setResult(`❌ Error: ${error.message}`);
      console.error('Error generating content:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStartSession = async () => {
    setLoading(true);
    setResult('');
    
    try {
      console.log('🚀 Start Session button clicked!');
      
      const response = await fetch('/api/learners/1/sessions', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json' 
        }
      });
      
      if (response.ok) {
        const session = await response.json();
        setResult(`✅ Session started: ID ${session.id || 'Session created successfully!'}`);
        console.log('Session started:', session);
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    } catch (error) {
      setResult(`❌ Error: ${error.message}`);
      console.error('Error starting session:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Learning Platform</h1>
        <p>React is now working! 🚀</p>
      </header>
      
      <div>
        <button 
          onClick={handleStartSession} 
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Start Session'}
        </button>
        
        <button 
          onClick={handleGenerateContent} 
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Generate Practice Content'}
        </button>
      </div>
      
      {result && (
        <div style={{ 
          marginTop: '20px', 
          padding: '15px', 
          backgroundColor: result.includes('❌') ? '#f8d7da' : '#d4edda',
          border: `1px solid ${result.includes('❌') ? '#f5c6cb' : '#c3e6cb'}`,
          borderRadius: '4px',
          color: result.includes('❌') ? '#721c24' : '#155724'
        }}>
          {result}
        </div>
      )}
    </div>
  );
}

export default App;
