// Updated after file reorganization - trigger rebuild

import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Brain, BookOpen, Target, Users, Zap, ChevronRight, Star, TrendingUp } from 'lucide-react'
import './App.css'

// Import components
import LearnerOnboarding from './components/LearnerOnboarding'
import Dashboard from './components/Dashboard'
import LearningSession from './components/LearningSession'

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [currentLearner, setCurrentLearner] = useState(null)

  // Check for existing user session
  useEffect(() => {
    const savedUser = localStorage.getItem('currentUser')
    const savedLearner = localStorage.getItem('currentLearner')
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser))
    }
    if (savedLearner) {
      setCurrentLearner(JSON.parse(savedLearner))
    }
  }, [])

  const handleUserCreated = (user, learner) => {
    setCurrentUser(user)
    setCurrentLearner(learner)
    localStorage.setItem('currentUser', JSON.stringify(user))
    localStorage.setItem('currentLearner', JSON.stringify(learner))
  }

  const handleLogout = () => {
    setCurrentUser(null)
    setCurrentLearner(null)
    localStorage.removeItem('currentUser')
    localStorage.removeItem('currentLearner')
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Routes>
          <Route 
            path="/" 
            element={
              currentUser && currentLearner ? 
                <Navigate to="/dashboard" replace /> : 
                <LandingPage onGetStarted={() => window.location.href = '/onboarding'} />
            } 
          />
          <Route 
            path="/onboarding" 
            element={
              currentUser && currentLearner ? 
                <Navigate to="/dashboard" replace /> : 
                <LearnerOnboarding onUserCreated={handleUserCreated} />
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              currentUser && currentLearner ? 
                <Dashboard 
                  user={currentUser} 
                  learner={currentLearner} 
                  onLogout={handleLogout}
                /> : 
                <Navigate to="/" replace />
            } 
          />
          <Route 
            path="/learn/:sessionId?" 
            element={
              currentUser && currentLearner ? 
                <LearningSession 
                  user={currentUser} 
                  learner={currentLearner} 
                /> : 
                <Navigate to="/" replace />
            } 
          />
        </Routes>
      </div>
    </Router>
  )
}

function LandingPage({ onGetStarted }) {
  const features = [
    {
      icon: <Brain className="h-8 w-8 text-blue-600" />,
      title: "AI-Powered Personalization",
      description: "Content adapts to your learning style, pace, and goals in real-time"
    },
    {
      icon: <Target className="h-8 w-8 text-purple-600" />,
      title: "Goal-Oriented Learning",
      description: "Focused paths for tech careers, creator business, and certifications"
    },
    {
      icon: <BookOpen className="h-8 w-8 text-green-600" />,
      title: "Dynamic Content Generation",
      description: "Fresh, relevant content generated specifically for your needs"
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-orange-600" />,
      title: "Adaptive Progress Tracking",
      description: "Smart analytics that adjust your learning path based on performance"
    }
  ]

  const niches = [
    {
      title: "Tech Career Acceleration",
      description: "Master coding, AI, data science, and cloud technologies",
      categories: ["Python & JavaScript", "AI/ML Engineering", "Cloud Certifications", "DevOps & Platform Engineering"],
      color: "bg-blue-500"
    },
    {
      title: "Creator Business & Entrepreneurship",
      description: "Build and monetize your creative business",
      categories: ["Content Marketing", "Personal Branding", "Social Media Strategy", "Email Marketing"],
      color: "bg-purple-500"
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <Brain className="h-8 w-8 text-blue-600" />
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI Learning Platform
              </span>
            </div>
            <Button onClick={onGetStarted} className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
              Get Started
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <Badge className="mb-6 bg-blue-100 text-blue-800 hover:bg-blue-200">
            <Zap className="mr-1 h-3 w-3" />
            AI-Powered Learning Revolution
          </Badge>
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-gray-900 via-blue-900 to-purple-900 bg-clip-text text-transparent">
            Personalized Learning
            <br />
            <span className="text-blue-600">That Adapts to You</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Experience the future of education with AI that creates custom content, adapts to your learning style, 
            and accelerates your progress in tech careers, creator business, and professional certifications.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              onClick={onGetStarted}
              size="lg" 
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-lg px-8 py-3"
            >
              Start Learning Now
              <ChevronRight className="ml-2 h-5 w-5" />
            </Button>
            <Button variant="outline" size="lg" className="text-lg px-8 py-3">
              Watch Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why Choose AI Learning Platform?</h2>
            <p className="text-xl text-gray-600">Revolutionary features that make learning faster, smarter, and more effective</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-300">
                <CardHeader className="text-center">
                  <div className="mx-auto mb-4 p-3 bg-gray-50 rounded-full w-fit">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-center">{feature.description}</CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Niches Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Choose Your Learning Path</h2>
            <p className="text-xl text-gray-600">Specialized content for high-value career advancement</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {niches.map((niche, index) => (
              <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <CardHeader>
                  <div className={`w-full h-2 ${niche.color} rounded-t-lg -mt-6 -mx-6 mb-4`}></div>
                  <CardTitle className="text-xl">{niche.title}</CardTitle>
                  <CardDescription>{niche.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {niche.categories.map((category, catIndex) => (
                      <Badge key={catIndex} variant="secondary" className="mr-2 mb-2">
                        {category}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Learning?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of learners who are accelerating their careers with personalized AI education
          </p>
          <Button 
            onClick={onGetStarted}
            size="lg" 
            className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-3"
          >
            Get Started Free
            <ChevronRight className="ml-2 h-5 w-5" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Brain className="h-6 w-6 text-blue-400" />
            <span className="text-xl font-bold">AI Learning Platform</span>
          </div>
          <p className="text-gray-400">
            Revolutionizing education through personalized AI-powered learning experiences
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
