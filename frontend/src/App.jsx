import React, { useState } from 'react';
import { HashRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';

// Onboarding Components 
function OnboardingFlow() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    username: '',
    learningGoals: '',
    experience: ''
  });
  const navigate = useNavigate();

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      // Complete onboarding and go to dashboard
      navigate('/dashboard');
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  return (
    <div style={{ padding: '40px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Welcome to AI Learning Platform</h1>
      <p>Step {step} of 3</p>
      
      {step === 1 && (
        <div>
          <h2>What's your name?</h2>
          <input
            type="text"
            placeholder="Enter your username"
            value={formData.username}
            onChange={(e) => handleInputChange('username', e.target.value)}
            style={{ width: '100%', padding: '10px', marginBottom: '20px' }}
          />
        </div>
      )}
      
      {step === 2 && (
        <div>
          <h2>What are your learning goals?</h2>
          <textarea
            placeholder="Tell us what you want to learn..."
            value={formData.learningGoals}
            onChange={(e) => handleInputChange('learningGoals', e.target.value)}
            style={{ width: '100%', padding: '10px', marginBottom: '20px', height: '100px' }}
          />
        </div>
      )}
      
      {step === 3 && (
        <div>
          <h2>What's your experience level?</h2>
          <select
            value={formData.experience}
            onChange={(e) => handleInputChange('experience', e.target.value)}
            style={{ width: '100%', padding: '10px', marginBottom: '20px' }}
          >
            <option value="">Select your level</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      )}
      
      <div>
        {step > 1 && (
          <button onClick={handleBack} style={{ marginRight: '10px' }}>
            Back
          </button>
        )}
        <button onClick={handleNext}>
          {step === 3 ? 'Complete Setup' : 'Next'}
        </button>
      </div>
    </div>
  );
}

// Dashboard Component (with your test buttons)
function Dashboard() {
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
        <h1>AI Learning Platform - Dashboard</h1>
        <p>Welcome! Your onboarding is complete. 🚀</p>
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

// Home Component (Landing Page)
function Home() {
  const navigate = useNavigate();

  console.log("Home component rendered!"); // ADD THIS LINE

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Learning Platform</h1>
        <p>Personalized learning powered by AI</p>
      </header>

      {/* CORRECTED INDENTATION FOR THE DIV CONTAINING BUTTONS */}
      <div>
        <button onClick={() => {
          console.log("Start Learning Now button clicked!"); // ADD THIS LINE
          navigate('/onboarding');
        }}>
          Start Learning Now
        </button>
        <button onClick={() => navigate('/onboarding')}>
          Get Started
        </button>
      </div>
    </div>
  );
}



// Main App Component with Router
function App() {
  return (
    <Router>
      <Routes>
        {/* TEMPORARY DEBUGGING CHANGE: Render OnboardingFlow directly on the root path */}
        <Route path="/" element={<OnboardingFlow />} />
        <Route path="/onboarding" element={<OnboardingFlow />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
