import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Brain, User, Target, BookOpen, Clock, ChevronRight, ChevronLeft } from 'lucide-react'

const API_BASE_URL = 'http://localhost:5001/api'

function LearnerOnboarding({ onUserCreated }) {
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    // User data
    username: '',
    email: '',
    
    // Learner profile data
    target_niche: '',
    learning_goals: [],
    preferred_learning_style: '',
    experience_level: '',
    time_availability: 300, // minutes per week
    custom_goal: ''
  })

  const niches = [
    {
      id: 'tech_career',
      name: 'Tech Career Acceleration',
      description: 'Coding, AI, Data Science, Cloud Computing',
      icon: '💻'
    },
    {
      id: 'creator_business',
      name: 'Creator Business & Entrepreneurship',
      description: 'Building and monetizing creative businesses',
      icon: '🚀'
    }
  ]

  const learningStyles = [
    { id: 'visual', name: 'Visual', description: 'Learn through images, diagrams, and visual representations' },
    { id: 'auditory', name: 'Auditory', description: 'Learn through listening and verbal instruction' },
    { id: 'kinesthetic', name: 'Kinesthetic', description: 'Learn through hands-on activities and movement' },
    { id: 'reading_writing', name: 'Reading/Writing', description: 'Learn through reading and writing activities' }
  ]

  const experienceLevels = [
    { id: 'beginner', name: 'Beginner', description: 'New to this field' },
    { id: 'intermediate', name: 'Intermediate', description: 'Some experience and knowledge' },
    { id: 'advanced', name: 'Advanced', description: 'Experienced and looking to specialize' }
  ]

  const goalsByNiche = {
    tech_career: [
      'Learn Python Programming',
      'Master JavaScript & React',
      'Get AWS Certification',
      'Learn Data Science & Analytics',
      'Master DevOps & CI/CD',
      'Learn AI/ML Engineering'
    ],
    creator_business: [
      'Build Personal Brand',
      'Master Content Marketing',
      'Grow Social Media Following',
      'Launch Online Course',
      'Start Newsletter Business',
      'Learn Email Marketing'
    ]
  }

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleGoalToggle = (goal) => {
    setFormData(prev => ({
      ...prev,
      learning_goals: prev.learning_goals.includes(goal)
        ? prev.learning_goals.filter(g => g !== goal)
        : [...prev.learning_goals, goal]
    }))
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      // Create user
      const userResponse = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email
        })
      })

      if (!userResponse.ok) {
        throw new Error('Failed to create user')
      }

      const user = await userResponse.json()

      // Prepare learning goals
      let goals = [...formData.learning_goals]
      if (formData.custom_goal.trim()) {
        goals.push(formData.custom_goal.trim())
      }

      // Create learner profile
      const learnerResponse = await fetch(`${API_BASE_URL}/learners`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          target_niche: formData.target_niche,
          learning_goals: goals,
          preferred_learning_style: formData.preferred_learning_style,
          experience_level: formData.experience_level,
          time_availability: formData.time_availability
        })
      })

      if (!learnerResponse.ok) {
        throw new Error('Failed to create learner profile')
      }

      const learner = await learnerResponse.json()

      onUserCreated(user, learner)
    } catch (error) {
      console.error('Error creating user:', error)
      alert('Failed to create account. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const nextStep = () => {
    if (step < 4) setStep(step + 1)
  }

  const prevStep = () => {
    if (step > 1) setStep(step - 1)
  }

  const canProceed = () => {
    switch (step) {
      case 1:
        return formData.username && formData.email
      case 2:
        return formData.target_niche
      case 3:
        return formData.learning_goals.length > 0 || formData.custom_goal.trim()
      case 4:
        return formData.preferred_learning_style && formData.experience_level
      default:
        return false
    }
  }

  const progress = (step / 4) * 100

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Brain className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Learning Platform
            </span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Your Learning Profile</h1>
          <p className="text-gray-600">Let's personalize your learning experience</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-500 mb-2">
            <span>Step {step} of 4</span>
            <span>{Math.round(progress)}% Complete</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Step Content */}
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              {step === 1 && <><User className="h-5 w-5" /><span>Basic Information</span></>}
              {step === 2 && <><Target className="h-5 w-5" /><span>Choose Your Path</span></>}
              {step === 3 && <><BookOpen className="h-5 w-5" /><span>Learning Goals</span></>}
              {step === 4 && <><Brain className="h-5 w-5" /><span>Learning Preferences</span></>}
            </CardTitle>
            <CardDescription>
              {step === 1 && "Tell us about yourself"}
              {step === 2 && "Select your primary learning focus"}
              {step === 3 && "What do you want to achieve?"}
              {step === 4 && "How do you learn best?"}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Step 1: Basic Information */}
            {step === 1 && (
              <div className="space-y-4">
                <div>
                  <Label htmlFor="username">Username</Label>
                  <Input
                    id="username"
                    value={formData.username}
                    onChange={(e) => handleInputChange('username', e.target.value)}
                    placeholder="Enter your username"
                  />
                </div>
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    placeholder="Enter your email address"
                  />
                </div>
              </div>
            )}

            {/* Step 2: Choose Niche */}
            {step === 2 && (
              <div className="space-y-4">
                {niches.map((niche) => (
                  <Card
                    key={niche.id}
                    className={`cursor-pointer transition-all duration-200 hover:shadow-md ${
                      formData.target_niche === niche.id
                        ? 'ring-2 ring-blue-500 bg-blue-50'
                        : 'hover:bg-gray-50'
                    }`}
                    onClick={() => handleInputChange('target_niche', niche.id)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start space-x-3">
                        <span className="text-2xl">{niche.icon}</span>
                        <div>
                          <h3 className="font-semibold text-lg">{niche.name}</h3>
                          <p className="text-gray-600 text-sm">{niche.description}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Step 3: Learning Goals */}
            {step === 3 && (
              <div className="space-y-4">
                <div>
                  <Label className="text-base font-medium">Select your learning goals:</Label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                    {(goalsByNiche[formData.target_niche] || []).map((goal) => (
                      <Badge
                        key={goal}
                        variant={formData.learning_goals.includes(goal) ? "default" : "outline"}
                        className="cursor-pointer p-2 justify-center hover:bg-blue-100"
                        onClick={() => handleGoalToggle(goal)}
                      >
                        {goal}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div>
                  <Label htmlFor="custom_goal">Or add a custom goal:</Label>
                  <Textarea
                    id="custom_goal"
                    value={formData.custom_goal}
                    onChange={(e) => handleInputChange('custom_goal', e.target.value)}
                    placeholder="Describe your specific learning goal..."
                    rows={3}
                  />
                </div>
              </div>
            )}

            {/* Step 4: Learning Preferences */}
            {step === 4 && (
              <div className="space-y-6">
                <div>
                  <Label className="text-base font-medium">Preferred Learning Style:</Label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2">
                    {learningStyles.map((style) => (
                      <Card
                        key={style.id}
                        className={`cursor-pointer transition-all duration-200 ${
                          formData.preferred_learning_style === style.id
                            ? 'ring-2 ring-blue-500 bg-blue-50'
                            : 'hover:bg-gray-50'
                        }`}
                        onClick={() => handleInputChange('preferred_learning_style', style.id)}
                      >
                        <CardContent className="p-3">
                          <h4 className="font-medium">{style.name}</h4>
                          <p className="text-sm text-gray-600">{style.description}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>

                <div>
                  <Label className="text-base font-medium">Experience Level:</Label>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-2">
                    {experienceLevels.map((level) => (
                      <Card
                        key={level.id}
                        className={`cursor-pointer transition-all duration-200 ${
                          formData.experience_level === level.id
                            ? 'ring-2 ring-blue-500 bg-blue-50'
                            : 'hover:bg-gray-50'
                        }`}
                        onClick={() => handleInputChange('experience_level', level.id)}
                      >
                        <CardContent className="p-3 text-center">
                          <h4 className="font-medium">{level.name}</h4>
                          <p className="text-sm text-gray-600">{level.description}</p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>

                <div>
                  <Label htmlFor="time_availability" className="text-base font-medium">
                    Time Available per Week:
                  </Label>
                  <Select
                    value={formData.time_availability.toString()}
                    onValueChange={(value) => handleInputChange('time_availability', parseInt(value))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="120">2 hours (120 minutes)</SelectItem>
                      <SelectItem value="300">5 hours (300 minutes)</SelectItem>
                      <SelectItem value="480">8 hours (480 minutes)</SelectItem>
                      <SelectItem value="600">10 hours (600 minutes)</SelectItem>
                      <SelectItem value="900">15 hours (900 minutes)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Navigation */}
        <div className="flex justify-between mt-8">
          <Button
            variant="outline"
            onClick={prevStep}
            disabled={step === 1}
            className="flex items-center space-x-2"
          >
            <ChevronLeft className="h-4 w-4" />
            <span>Previous</span>
          </Button>

          {step < 4 ? (
            <Button
              onClick={nextStep}
              disabled={!canProceed()}
              className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              <span>Next</span>
              <ChevronRight className="h-4 w-4" />
            </Button>
          ) : (
            <Button
              onClick={handleSubmit}
              disabled={!canProceed() || loading}
              className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Creating Profile...</span>
                </>
              ) : (
                <>
                  <span>Complete Setup</span>
                  <ChevronRight className="h-4 w-4" />
                </>
              )}
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}

export default LearnerOnboarding

