import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group.jsx'
import { Label } from '@/components/ui/label.jsx'
import { 
  Brain, 
  BookOpen, 
  CheckCircle, 
  XCircle, 
  ArrowRight, 
  ArrowLeft, 
  Home,
  Lightbulb,
  Target,
  Clock,
  Zap
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:5001/api'

function LearningSession({ user, learner }) {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  
  const [session, setSession] = useState(null)
  const [currentContent, setCurrentContent] = useState(null)
  const [currentExercise, setCurrentExercise] = useState(null)
  const [userAnswer, setUserAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [sessionProgress, setSessionProgress] = useState(0)
  const [loading, setLoading] = useState(true)
  const [generatingContent, setGeneratingContent] = useState(false)
  const [contentHistory, setContentHistory] = useState([])

  // Sample concepts for the session
  const sessionConcepts = {
    tech_career: [
      'Python Functions',
      'Data Structures',
      'API Design',
      'Testing Strategies',
      'Version Control'
    ],
    creator_business: [
      'Content Marketing Strategy',
      'Personal Branding',
      'Social Media Growth',
      'Email Marketing',
      'Monetization Strategies'
    ]
  }

  useEffect(() => {
    if (sessionId) {
      fetchSession()
    } else {
      // Start a new session
      startNewSession()
    }
  }, [sessionId])

  const fetchSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/learners/${learner.id}/sessions`)
      if (response.ok) {
        const sessions = await response.json()
        const currentSession = sessions.find(s => s.id.toString() === sessionId)
        if (currentSession) {
          setSession(currentSession)
        }
      }
    } catch (error) {
      console.error('Error fetching session:', error)
    } finally {
      setLoading(false)
    }
  }

  const startNewSession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/learners/${learner.id}/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      })

      if (response.ok) {
        const newSession = await response.json()
        setSession(newSession)
        generateNextContent()
      }
    } catch (error) {
      console.error('Error starting session:', error)
    } finally {
      setLoading(false)
    }
  }

  const generateNextContent = async () => {
    setGeneratingContent(true)
    try {
      // Get a random concept for the learner's niche
      const concepts = sessionConcepts[learner.target_niche] || sessionConcepts.tech_career
      const concept = concepts[Math.floor(Math.random() * concepts.length)]

      // Generate lesson content
      const lessonResponse = await fetch(`${API_BASE_URL}/learners/${learner.id}/generate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          concept: concept,
          content_type: 'lesson'
        })
      })

      if (lessonResponse.ok) {
        const lessonData = await lessonResponse.json()
        setCurrentContent(lessonData)
        setContentHistory(prev => [...prev, { type: 'lesson', data: lessonData }])
      }

      // Generate exercise
      const exerciseResponse = await fetch(`${API_BASE_URL}/learners/${learner.id}/generate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          concept: concept,
          content_type: 'exercise',
          exercise_type: 'multiple_choice'
        })
      })

      if (exerciseResponse.ok) {
        const exerciseData = await exerciseResponse.json()
        setCurrentExercise(exerciseData)
      }

    } catch (error) {
      console.error('Error generating content:', error)
    } finally {
      setGeneratingContent(false)
    }
  }

  const submitAnswer = async () => {
    if (!userAnswer || !currentExercise) return

    try {
      const response = await fetch(`${API_BASE_URL}/learners/${learner.id}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          learner_answer: userAnswer,
          correct_answer: currentExercise.generated_content.correct_answer,
          concept: currentExercise.concept
        })
      })

      if (response.ok) {
        const feedbackData = await response.json()
        setFeedback(feedbackData)
        setShowFeedback(true)
        
        // Update session progress
        setSessionProgress(prev => Math.min(prev + 20, 100))
      }
    } catch (error) {
      console.error('Error submitting answer:', error)
    }
  }

  const nextContent = () => {
    setCurrentContent(null)
    setCurrentExercise(null)
    setUserAnswer('')
    setFeedback(null)
    setShowFeedback(false)
    generateNextContent()
  }

  const endSession = async () => {
    if (session) {
      try {
        await fetch(`${API_BASE_URL}/learners/${learner.id}/sessions/${session.id}/end`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            completion_rate: sessionProgress / 100
          })
        })
      } catch (error) {
        console.error('Error ending session:', error)
      }
    }
    navigate('/dashboard')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Starting your learning session...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm" onClick={() => navigate('/dashboard')}>
                <Home className="h-4 w-4 mr-2" />
                Dashboard
              </Button>
              <div className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-blue-600" />
                <span className="font-semibold">Learning Session</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                Progress: {sessionProgress}%
              </div>
              <Button variant="outline" size="sm" onClick={endSession}>
                End Session
              </Button>
            </div>
          </div>
          <div className="pb-4">
            <Progress value={sessionProgress} className="h-2" />
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {generatingContent ? (
          <Card className="text-center py-12">
            <CardContent>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold mb-2">Generating Personalized Content</h3>
              <p className="text-gray-600">
                Our AI is creating content tailored specifically for your learning style and goals...
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-8">
            {/* Lesson Content */}
            {currentContent && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <BookOpen className="h-5 w-5 text-blue-600" />
                      <CardTitle>{currentContent.generated_content.title}</CardTitle>
                    </div>
                    <Badge className="bg-blue-100 text-blue-800">
                      {currentContent.concept}
                    </Badge>
                  </div>
                  <CardDescription>
                    Personalized for {learner.preferred_learning_style} learners
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Learning Objectives */}
                  {currentContent.generated_content.learning_objectives && (
                    <div>
                      <h4 className="font-semibold mb-2 flex items-center">
                        <Target className="h-4 w-4 mr-2 text-green-600" />
                        Learning Objectives
                      </h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-700">
                        {currentContent.generated_content.learning_objectives.map((objective, index) => (
                          <li key={index}>{objective}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Main Content */}
                  <div className="prose max-w-none">
                    <div className="whitespace-pre-wrap text-gray-800">
                      {currentContent.generated_content.content}
                    </div>
                  </div>

                  {/* Examples */}
                  {currentContent.generated_content.examples && (
                    <div>
                      <h4 className="font-semibold mb-2 flex items-center">
                        <Lightbulb className="h-4 w-4 mr-2 text-yellow-600" />
                        Examples
                      </h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-700">
                        {currentContent.generated_content.examples.map((example, index) => (
                          <li key={index}>{example}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Key Takeaways */}
                  {currentContent.generated_content.key_takeaways && (
                    <div>
                      <h4 className="font-semibold mb-2 flex items-center">
                        <Zap className="h-4 w-4 mr-2 text-purple-600" />
                        Key Takeaways
                      </h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-700">
                        {currentContent.generated_content.key_takeaways.map((takeaway, index) => (
                          <li key={index}>{takeaway}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Exercise */}
            {currentExercise && !showFeedback && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <span>Practice Exercise</span>
                  </CardTitle>
                  <CardDescription>
                    Test your understanding of {currentExercise.concept}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div>
                    <h4 className="font-semibold mb-4">{currentExercise.generated_content.question}</h4>
                    
                    {currentExercise.generated_content.options && (
                      <RadioGroup value={userAnswer} onValueChange={setUserAnswer}>
                        {currentExercise.generated_content.options.map((option, index) => (
                          <div key={index} className="flex items-center space-x-2">
                            <RadioGroupItem value={option.charAt(0)} id={`option-${index}`} />
                            <Label htmlFor={`option-${index}`} className="cursor-pointer">
                              {option}
                            </Label>
                          </div>
                        ))}
                      </RadioGroup>
                    )}
                  </div>

                  <Button 
                    onClick={submitAnswer} 
                    disabled={!userAnswer}
                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                  >
                    Submit Answer
                  </Button>
                </CardContent>
              </Card>
            )}

            {/* Feedback */}
            {showFeedback && feedback && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    {userAnswer === currentExercise.generated_content.correct_answer ? (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-600" />
                    )}
                    <span>
                      {userAnswer === currentExercise.generated_content.correct_answer ? 'Correct!' : 'Not quite right'}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-gray-800">{feedback.feedback}</p>
                  </div>
                  
                  {currentExercise.generated_content.explanation && (
                    <div>
                      <h4 className="font-semibold mb-2">Explanation:</h4>
                      <p className="text-gray-700">{currentExercise.generated_content.explanation}</p>
                    </div>
                  )}

                  <div className="flex space-x-4">
                    <Button onClick={nextContent} className="flex-1">
                      <ArrowRight className="mr-2 h-4 w-4" />
                      Continue Learning
                    </Button>
                    <Button variant="outline" onClick={endSession}>
                      End Session
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Next Steps */}
            {currentContent && currentContent.generated_content.next_steps && !currentExercise && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <ArrowRight className="h-5 w-5 text-blue-600" />
                    <span>Next Steps</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 mb-4">{currentContent.generated_content.next_steps}</p>
                  <Button onClick={nextContent} className="w-full">
                    Continue to Practice Exercise
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default LearningSession
