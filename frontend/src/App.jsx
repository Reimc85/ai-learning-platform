import React from 'react';

function App() {
  const handleClick = () => {
    alert('Button clicked! React is working!');
  };

  return (
    <div>
      <h1>AI Learning Platform</h1>
      <button onClick={handleClick}>
        Test Button
      </button>
    </div>
  );
}

export default App;
