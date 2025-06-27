import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Brain, 
  BookOpen, 
  Target, 
  TrendingUp, 
  Clock, 
  Play, 
  Settings, 
  LogOut,
  Zap,
  Award,
  Calendar,
  BarChart3
} from 'lucide-react'

import { API_BASE_URL } from '../config/api.js'

function Dashboard({ user, learner, onLogout }) {
  const [learningStats, setLearningStats] = useState({
    totalSessions: 0,
    totalTimeSpent: 0,
    completionRate: 0,
    currentStreak: 0
  })
  const [recentSessions, setRecentSessions] = useState([])
  const [knowledgeGaps, setKnowledgeGaps] = useState([])
  const [loading, setLoading] = useState(true)
  const [generatingContent, setGeneratingContent] = useState(false)
  const [generatedContent, setGeneratedContent] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [learner.id])

  const fetchDashboardData = async () => {
    try {
      // Fetch learning sessions
      const sessionsResponse = await fetch(`${API_BASE_URL}/learners/${learner.id}/sessions`)
      if (sessionsResponse.ok) {
        const sessions = await sessionsResponse.json()
        setRecentSessions(sessions.slice(0, 5)) // Get last 5 sessions
        
        // Calculate stats
        const totalSessions = sessions.length
        const totalTimeSpent = sessions.reduce((total, session) => total + (session.duration_minutes || 0), 0)
        const avgCompletion = sessions.length > 0 
          ? sessions.reduce((total, session) => total + (session.completion_rate || 0), 0) / sessions.length 
          : 0

        setLearningStats({
          totalSessions,
          totalTimeSpent,
          completionRate: Math.round(avgCompletion * 100),
          currentStreak: 3 // Mock data for now
        })
      }

      // Fetch knowledge gaps
      const gapsResponse = await fetch(`${API_BASE_URL}/learners/${learner.id}/knowledge-gaps`)
      if (gapsResponse.ok) {
        const gaps = await gapsResponse.json()
        setKnowledgeGaps(gaps.knowledge_gaps || [])
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const startLearningSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/learners/${learner.id}/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      })

      if (response.ok) {
        const session = await response.json()
        window.location.href = `/learn/${session.id}`
      }
    } catch (error) {
      console.error('Error starting learning session:', error)
    }
  }

  const generatePracticeContent = async () => {
  console.log('🚀 Generate button clicked - starting...');
  setGeneratingContent(true);
  
  try {
    console.log('📡 Making API call...');
    
    const response = await fetch(`${API_BASE_URL}/learners/${learner.id}/generate-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        concept: 'Content Marketing',
        content_type: 'lesson'
      })
    });

    console.log('📥 Response received:', response.status);

    if (response.ok) {
      const content = await response.json();
      console.log('✅ Content generated:', content);
      setGeneratedContent(content);
      
      alert(`✅ Generated personalized content about "${content.concept}"!\n\nCheck the console (F12) to see the full AI-generated lesson!`);
    } else {
      throw new Error(`HTTP ${response.status}`);
    }
  } catch (error) {
    console.error('❌ Error generating content:', error);
    alert('❌ Error generating content: ' + error.message);
  } finally {
    setGeneratingContent(false);
  }
}

  const getNicheInfo = () => {
    const niches = {
      tech_career: {
        name: 'Tech Career Acceleration',
        icon: '💻',
        color: 'bg-blue-500'
      },
      creator_business: {
        name: 'Creator Business & Entrepreneurship',
        icon: '🚀',
        color: 'bg-purple-500'
      }
    }
    return niches[learner.target_niche] || niches.tech_career
  }

  const nicheInfo = getNicheInfo()

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-blue-600" />
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI Learning Platform
                </span>
              </div>
              <div className="hidden sm:block">
                <Badge className={`${nicheInfo.color} text-white`}>
                  {nicheInfo.icon} {nicheInfo.name}
                </Badge>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user.username}!</span>
              <Button variant="outline" size="sm">
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>
              <Button variant="outline" size="sm" onClick={onLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user.username}!
          </h1>
          <p className="text-gray-600">
            Ready to continue your {nicheInfo.name.toLowerCase()} journey?
          </p>
        </div>

        {/* Quick Action */}
        <Card className="mb-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white border-0">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2">Continue Learning</h2>
                <p className="opacity-90">
                  Your personalized AI tutor is ready with new content tailored just for you
                </p>
              </div>
              <Button 
                onClick={startLearningSession}
                size="lg" 
                className="bg-white text-blue-600 hover:bg-gray-100"
              >
                <Play className="mr-2 h-5 w-5" />
                Start Session
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Sessions</CardTitle>
              <BookOpen className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{learningStats.totalSessions}</div>
              <p className="text-xs text-muted-foreground">
                Learning sessions completed
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Time Spent</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{Math.round(learningStats.totalTimeSpent / 60)}h</div>
              <p className="text-xs text-muted-foreground">
                Total learning time
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completion Rate</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{learningStats.completionRate}%</div>
              <p className="text-xs text-muted-foreground">
                Average session completion
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
              <Award className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{learningStats.currentStreak}</div>
              <p className="text-xs text-muted-foreground">
                Days in a row
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Learning Goals Progress */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="h-5 w-5" />
                <span>Learning Goals</span>
              </CardTitle>
              <CardDescription>Your progress towards your learning objectives</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {learner.learning_goals && learner.learning_goals.length > 0 ? (
                learner.learning_goals.map((goal, index) => (
                  <div key={index} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium">{goal}</span>
                      <span className="text-muted-foreground">{Math.floor(Math.random() * 40 + 30)}%</span>
                    </div>
                    <Progress value={Math.floor(Math.random() * 40 + 30)} className="h-2" />
                  </div>
                ))
              ) : (
                <p className="text-muted-foreground">No learning goals set yet.</p>
              )}
            </CardContent>
          </Card>

          {/* Knowledge Gaps */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5" />
                <span>Focus Areas</span>
              </CardTitle>
              <CardDescription>Concepts that need more attention</CardDescription>
            </CardHeader>
            <CardContent>
              {knowledgeGaps.length > 0 ? (
                <div className="space-y-2">
                  {knowledgeGaps.slice(0, 5).map((gap, index) => (
                    <Badge key={index} variant="outline" className="mr-2 mb-2">
                      {gap}
                    </Badge>
                  ))}
                </div>
              ) : (
                <div className="space-y-2">
                  <Badge variant="outline" className="mr-2 mb-2">Python Functions</Badge>
                  <Badge variant="outline" className="mr-2 mb-2">Data Structures</Badge>
                  <Badge variant="outline" className="mr-2 mb-2">API Design</Badge>
                  <Badge variant="outline" className="mr-2 mb-2">Testing Strategies</Badge>
                </div>
              )}
              <Button 
                variant="outline" 
                size="sm" 
                className="mt-4 w-full" 
                onClick={generatePracticeContent}
                disabled={generatingContent}
              >
                <BookOpen className="mr-2 h-4 w-4" />
                {generatingContent ? 'Generating...' : 'Generate Practice Content'}
              </Button>
              {generatedContent && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-sm font-medium text-green-800">
                    ✅ Generated content about "{generatedContent.concept}"
                  </p>
                  <p className="text-xs text-green-600 mt-1">
                    Check the browser console (F12) to view the full lesson!
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Recent Sessions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Calendar className="h-5 w-5" />
                <span>Recent Sessions</span>
              </CardTitle>
              <CardDescription>Your latest learning activities</CardDescription>
            </CardHeader>
            <CardContent>
              {recentSessions.length > 0 ? (
                <div className="space-y-3">
                  {recentSessions.map((session, index) => (
                    <div key={session.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium text-sm">
                          Session {session.id}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {session.duration_minutes ? `${session.duration_minutes} minutes` : 'In progress'}
                        </p>
                      </div>
                      <Badge variant={session.completion_rate > 0.8 ? "default" : "secondary"}>
                        {session.completion_rate ? `${Math.round(session.completion_rate * 100)}%` : 'Active'}
                      </Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-6">
                  <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-muted-foreground">No sessions yet</p>
                  <p className="text-sm text-muted-foreground">Start your first learning session!</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Learning Style & Preferences */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5" />
                <span>Your Learning Profile</span>
              </CardTitle>
              <CardDescription>Personalization settings</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm font-medium">Learning Style</p>
                <Badge className="mt-1 capitalize">{learner.preferred_learning_style}</Badge>
              </div>
              <div>
                <p className="text-sm font-medium">Experience Level</p>
                <Badge variant="outline" className="mt-1 capitalize">{learner.experience_level}</Badge>
              </div>
              <div>
                <p className="text-sm font-medium">Weekly Time Commitment</p>
                <p className="text-sm text-muted-foreground">{Math.round(learner.time_availability / 60)} hours per week</p>
              </div>
              <Button variant="outline" size="sm" className="w-full">
                <Settings className="mr-2 h-4 w-4" />
                Update Preferences
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
