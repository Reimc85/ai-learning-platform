import React from 'react';

function App() {
  const handleClick = async () => {
    console.log('🚀 Generate button clicked!');
    alert('Button is working! React is running!');
    
    try {
      const response = await fetch('/api/learners/1/generate-content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          concept: 'Content Marketing',
          content_type: 'lesson'
        })
      });
      
      if (response.ok) {
        const content = await response.json();
        alert('✅ Generated: ' + content.concept);
        console.log('Generated content:', content);
      } else {
        throw new Error('HTTP ' + response.status);
      }
    } catch (error) {
      alert('❌ Error: ' + error.message);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Learning Platform - Test</h1>
      <button onClick={handleClick} style={{ padding: '10px 20px', fontSize: '16px' }}>
        Generate Practice Content
      </button>
      <p>If you can see this and the button works, React is running!</p>
    </div>
  );
}

export default App;
