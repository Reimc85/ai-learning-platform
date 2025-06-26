import os
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI library not installed. Using mock responses.")

class AIContentGenerator:
    def __init__(self):
        self.openai_available = OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY')
        if self.openai_available:
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        else:
            self.client = None
        
    def generate_personalized_content(self, concept: str, content_type: str, 
                                    personalization_params: Dict[str, Any], 
                                    exercise_type: str = None) -> Dict[str, Any]:
        """
        Generate personalized educational content using OpenAI API or fallback to mock
        """
        if self.openai_available:
            return self._generate_with_openai(concept, content_type, personalization_params, exercise_type)
        else:
            return self._generate_mock_content(concept, content_type, personalization_params, exercise_type)
    
    def _generate_with_openai(self, concept: str, content_type: str, 
                             personalization_params: Dict[str, Any], 
                             exercise_type: str = None) -> Dict[str, Any]:
        """
        Generate content using OpenAI API
        """
        try:
            # Build personalized prompt based on learner profile
            prompt = self._build_prompt(concept, content_type, personalization_params, exercise_type)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using 3.5-turbo for cost efficiency
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator and personalized tutor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content_text = response.choices[0].message.content.strip()
            
            # Parse the response based on content type
            if content_type == "lesson":
                return self._parse_lesson_content(content_text, concept)
            elif content_type == "exercise":
                return self._parse_exercise_content(content_text, concept, exercise_type)
            else:
                return {"content": content_text}
                
        except Exception as e:
            print(f"Error generating content with OpenAI: {e}")
            # Fallback to mock content if API fails
            return self._generate_mock_content(concept, content_type, personalization_params, exercise_type)
    
    def _build_prompt(self, concept: str, content_type: str, 
                     personalization_params: Dict[str, Any], 
                     exercise_type: str = None) -> str:
        """
        Build a personalized prompt based on learner characteristics
        """
        learning_style = personalization_params.get('learning_style', 'visual')
        experience_level = personalization_params.get('experience_level', 'beginner')
        niche = personalization_params.get('niche', 'tech_career')
        
        # Base prompt structure
        if content_type == "lesson":
            prompt = f"""Create a comprehensive lesson about "{concept}" for a {experience_level} learner in {niche.replace('_', ' ')} who learns best through {learning_style} methods.

Structure the lesson as follows:
1. Title: A clear, engaging title
2. Learning Objectives: 3-4 specific learning objectives
3. Content: Main lesson content (500-800 words) optimized for {learning_style} learners
4. Examples: 2-3 practical examples relevant to {niche.replace('_', ' ')}
5. Key Takeaways: 3-5 key points to remember
6. Next Steps: What the learner should do next

Make the content engaging, practical, and appropriate for {experience_level} level."""

        elif content_type == "exercise" and exercise_type == "multiple_choice":
            prompt = f"""Create a multiple choice question about "{concept}" for a {experience_level} learner in {niche.replace('_', ' ')}.

Format your response as:
Question: [Your question here]
A) [Option A]
B) [Option B] 
C) [Option C]
D) [Option D]
Correct Answer: [A, B, C, or D]
Explanation: [Brief explanation of why the answer is correct]

Make the question challenging but appropriate for {experience_level} level, and ensure it's relevant to {niche.replace('_', ' ')}."""

        else:
            prompt = f"Create educational content about {concept} for a {experience_level} learner in {niche.replace('_', ' ')}."
        
        return prompt
    
    def _parse_lesson_content(self, content_text: str, concept: str) -> Dict[str, Any]:
        """
        Parse lesson content from OpenAI response
        """
        lines = content_text.split('\n')
        parsed_content = {
            "title": f"Understanding {concept}",
            "learning_objectives": [],
            "content": content_text,
            "examples": [],
            "key_takeaways": [],
            "next_steps": "Continue practicing and apply these concepts in real projects."
        }
        
        # Try to extract structured content
        current_section = None
        for line in lines:
            line = line.strip()
            if line.lower().startswith('title:'):
                parsed_content["title"] = line.split(':', 1)[1].strip()
            elif 'learning objectives' in line.lower():
                current_section = 'objectives'
            elif 'examples' in line.lower():
                current_section = 'examples'
            elif 'key takeaways' in line.lower() or 'takeaways' in line.lower():
                current_section = 'takeaways'
            elif 'next steps' in line.lower():
                current_section = 'next_steps'
            elif line and current_section:
                if current_section == 'objectives' and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    parsed_content["learning_objectives"].append(line.lstrip('-•0123456789. '))
                elif current_section == 'examples' and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    parsed_content["examples"].append(line.lstrip('-•0123456789. '))
                elif current_section == 'takeaways' and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    parsed_content["key_takeaways"].append(line.lstrip('-•0123456789. '))
                elif current_section == 'next_steps':
                    parsed_content["next_steps"] = line
        
        return parsed_content
    
    def _parse_exercise_content(self, content_text: str, concept: str, exercise_type: str) -> Dict[str, Any]:
        """
        Parse exercise content from OpenAI response
        """
        lines = content_text.split('\n')
        parsed_content = {
            "question": f"What is the main concept behind {concept}?",
            "options": [
                "A) A fundamental concept in the field",
                "B) An advanced technique requiring expertise", 
                "C) A deprecated approach no longer used",
                "D) A tool used only by beginners"
            ],
            "correct_answer": "A",
            "explanation": f"{concept} is indeed a fundamental concept that forms the basis for more advanced learning."
        }
        
        # Try to extract structured content
        for i, line in enumerate(lines):
            line = line.strip()
            if line.lower().startswith('question:'):
                parsed_content["question"] = line.split(':', 1)[1].strip()
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                if "options" not in parsed_content:
                    parsed_content["options"] = []
                parsed_content["options"].append(line)
            elif line.lower().startswith('correct answer:'):
                parsed_content["correct_answer"] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('explanation:'):
                parsed_content["explanation"] = line.split(':', 1)[1].strip()
        
        return parsed_content
    
    def _generate_mock_content(self, concept: str, content_type: str, 
                              personalization_params: Dict[str, Any], 
                              exercise_type: str = None) -> Dict[str, Any]:
        """
        Generate mock content when OpenAI API is not available
        """
        learning_style = personalization_params.get('learning_style', 'visual')
        experience_level = personalization_params.get('experience_level', 'beginner')
        niche = personalization_params.get('niche', 'tech_career')
        
        if content_type == "lesson":
            return {
                "title": f"Understanding {concept}",
                "learning_objectives": [
                    f"Understand the core principles of {concept}",
                    f"Apply {concept} in practical scenarios",
                    f"Identify common patterns and best practices"
                ],
                "content": f"""Welcome to this personalized lesson on {concept}, designed specifically for {learning_style} learners at the {experience_level} level in {niche.replace('_', ' ')}.

{concept} is a fundamental concept that every professional in {niche.replace('_', ' ')} should master. This lesson will guide you through the essential aspects, providing clear explanations and practical examples.

Key Concepts:
Understanding {concept} requires grasping its core principles and how they apply in real-world scenarios. As a {experience_level} learner, we'll start with the basics and build up your knowledge systematically.

For {learning_style} learners like yourself, we'll use diagrams, visual examples, and step-by-step breakdowns to make the concepts clear and memorable.

Practical Applications:
In {niche.replace('_', ' ')}, {concept} is used extensively for solving complex problems and building robust solutions. You'll encounter this concept in various forms throughout your career.

This personalized approach ensures that the content matches your learning style and experience level, making it easier to understand and retain the information.""",
                "examples": [
                    f"Example 1: Basic implementation of {concept} in a real project",
                    f"Example 2: Advanced use case showing {concept} optimization",
                    f"Example 3: Common mistakes to avoid when working with {concept}"
                ],
                "key_takeaways": [
                    f"{concept} is essential for {niche.replace('_', ' ')} professionals",
                    f"Understanding the fundamentals enables advanced applications",
                    f"Practice and real-world application solidify learning"
                ],
                "next_steps": f"Practice implementing {concept} in small projects and gradually work on more complex applications."
            }
        
        elif content_type == "exercise" and exercise_type == "multiple_choice":
            return {
                "question": f"Which of the following best describes {concept} in the context of {niche.replace('_', ' ')}?",
                "options": [
                    "A) A fundamental concept that forms the foundation for advanced learning",
                    "B) An advanced technique requiring years of experience",
                    "C) A deprecated approach no longer used in modern practices",
                    "D) A tool used exclusively by beginners"
                ],
                "correct_answer": "A",
                "explanation": f"{concept} is indeed a fundamental concept that forms the basis for more advanced learning in {niche.replace('_', ' ')}. Understanding it well is crucial for career progression."
            }
        
        return {"content": f"Content about {concept} for {learning_style} learners"}
    
    def generate_personalized_feedback(self, learner_answer: str, correct_answer: str, 
                                     concept: str, personalization_params: Dict[str, Any]) -> str:
        """
        Generate personalized feedback based on learner's answer
        """
        learning_style = personalization_params.get('learning_style', 'visual')
        experience_level = personalization_params.get('experience_level', 'beginner')
        
        if self.openai_available:
            try:
                prompt = f"""Provide personalized feedback for a {experience_level} learner who prefers {learning_style} learning.

The question was about: {concept}
Their answer: {learner_answer}
Correct answer: {correct_answer}

Provide encouraging, constructive feedback that:
1. Acknowledges their effort
2. Explains why their answer was right/wrong
3. Provides guidance for improvement
4. Uses {learning_style} learning techniques in the explanation

Keep it supportive and educational."""

                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a supportive, personalized tutor."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"Error generating feedback with OpenAI: {e}")
        
        # Fallback feedback
        if learner_answer == correct_answer:
            return f"Excellent work! You correctly understood {concept}. Your {learning_style} learning approach is paying off. Keep practicing to reinforce this knowledge!"
        else:
            return f"Good attempt! While your answer shows you're thinking about {concept}, let me help clarify. The key point is... Try visualizing this concept as... Keep practicing - you're on the right track!"

    def analyze_knowledge_gaps(self, learner_responses: List[Dict[str, Any]], 
                              learner_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Advanced knowledge gap analysis with scoring and prioritization
        """
        from collections import defaultdict
        import math
        
        gaps = defaultdict(lambda: {'incorrect_count': 0, 'total_count': 0, 'difficulty_levels': []})
        
        # Analyze response patterns
        for response in learner_responses:
            concept = response.get('concept', 'Unknown')
            is_correct = response.get('is_correct', False)
            difficulty = response.get('difficulty_level', 'beginner')
            
            gaps[concept]['total_count'] += 1
            gaps[concept]['difficulty_levels'].append(difficulty)
            
            if not is_correct:
                gaps[concept]['incorrect_count'] += 1
        
        # Calculate gap scores and prioritize
        prioritized_gaps = []
        for concept, data in gaps.items():
            if data['total_count'] > 0:
                error_rate = data['incorrect_count'] / data['total_count']
                
                # Weight by difficulty level
                difficulty_weight = {
                    'beginner': 1.0,
                    'intermediate': 1.5,
                    'advanced': 2.0
                }.get(max(set(data['difficulty_levels']), key=data['difficulty_levels'].count), 1.0)
                
                # Calculate priority score
                priority_score = error_rate * difficulty_weight * math.log(data['total_count'] + 1)
                
                prioritized_gaps.append({
                    'concept': concept,
                    'error_rate': round(error_rate, 2),
                    'priority_score': round(priority_score, 2),
                    'attempts': data['total_count'],
                    'difficulty_level': max(set(data['difficulty_levels']), key=data['difficulty_levels'].count),
                    'severity': 'high' if error_rate > 0.7 else 'medium' if error_rate > 0.4 else 'low'
                })
        
        # Sort by priority score
        prioritized_gaps.sort(key=lambda x: x['priority_score'], reverse=True)
        
        # Add niche-specific common gaps if needed
        niche = learner_profile.get('target_niche', 'tech_career')
        experience_level = learner_profile.get('experience_level', 'beginner')
        
        if len(prioritized_gaps) < 3:
            common_gaps = self._get_common_gaps_for_niche(niche, experience_level)
            for gap in common_gaps:
                if not any(g['concept'] == gap for g in prioritized_gaps):
                    prioritized_gaps.append({
                        'concept': gap,
                        'error_rate': 0.5,  # Estimated
                        'priority_score': 1.0,
                        'attempts': 0,
                        'difficulty_level': experience_level,
                        'severity': 'medium',
                        'type': 'predicted'
                    })
        
        return prioritized_gaps[:5]  # Return top 5 gaps
    
    def recommend_learning_path(self, learner_profile: Dict[str, Any], 
                              knowledge_gaps: List[Dict[str, Any]], 
                              current_performance: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Advanced personalized learning path recommendations
        """
        niche = learner_profile.get('target_niche', 'tech_career')
        experience_level = learner_profile.get('experience_level', 'beginner')
        learning_style = learner_profile.get('preferred_learning_style', 'visual')
        time_availability = learner_profile.get('time_availability', 300)  # minutes per week
        
        recommendations = []
        
        # Process knowledge gaps first (highest priority)
        for gap in knowledge_gaps[:3]:
            concept = gap.get('concept') if isinstance(gap, dict) else gap
            severity = gap.get('severity', 'medium') if isinstance(gap, dict) else 'medium'
            
            # Calculate estimated time based on complexity and learner profile
            base_time = self._estimate_learning_time(concept, experience_level, niche)
            
            # Adjust for learning style
            style_multiplier = {
                'visual': 0.9,      # Faster with visual aids
                'auditory': 1.0,    # Standard time
                'kinesthetic': 1.2, # Needs more hands-on practice
                'reading_writing': 0.95  # Efficient with text-based learning
            }.get(learning_style, 1.0)
            
            estimated_time = int(base_time * style_multiplier)
            
            recommendations.append({
                'concept': concept,
                'priority': 'high' if severity == 'high' else 'medium',
                'estimated_time_minutes': estimated_time,
                'content_types': self._get_optimal_content_sequence(concept, learning_style, experience_level),
                'reason': f"Addressing this gap will significantly improve your {niche.replace('_', ' ')} skills",
                'difficulty_level': gap.get('difficulty_level', experience_level) if isinstance(gap, dict) else experience_level,
                'prerequisites': self._get_prerequisites(concept, niche),
                'learning_objectives': self._generate_learning_objectives(concept, experience_level)
            })
        
        # Add progression recommendations based on current mastery
        if current_performance:
            mastery_level = current_performance.get('overall_mastery', 0.5)
            if mastery_level > 0.7:
                # Ready for advanced topics
                advanced_topics = self._get_advanced_topics(niche, experience_level)
                for topic in advanced_topics[:2]:
                    recommendations.append({
                        'concept': topic,
                        'priority': 'medium',
                        'estimated_time_minutes': self._estimate_learning_time(topic, 'advanced', niche),
                        'content_types': ['lesson', 'project', 'case_study'],
                        'reason': 'Ready to advance to more challenging topics',
                        'difficulty_level': 'advanced',
                        'prerequisites': [],
                        'learning_objectives': self._generate_learning_objectives(topic, 'advanced')
                    })
        
        # Add skill reinforcement recommendations
        reinforcement_topics = self._get_reinforcement_topics(niche, experience_level)
        for topic in reinforcement_topics[:1]:
            recommendations.append({
                'concept': topic,
                'priority': 'low',
                'estimated_time_minutes': 30,
                'content_types': ['practice', 'quiz', 'review'],
                'reason': 'Reinforce and maintain existing knowledge',
                'difficulty_level': experience_level,
                'prerequisites': [],
                'learning_objectives': [f"Review and strengthen understanding of {topic}"]
            })
        
        # Sort by priority and estimated impact
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def adjust_difficulty(self, current_difficulty: str, performance_score: float) -> str:
        """
        Adjust content difficulty based on learner performance
        """
        if performance_score >= 0.8:
            # High performance - increase difficulty
            if current_difficulty == 'beginner':
                return 'intermediate'
            elif current_difficulty == 'intermediate':
                return 'advanced'
        elif performance_score <= 0.4:
            # Low performance - decrease difficulty
            if current_difficulty == 'advanced':
                return 'intermediate'
            elif current_difficulty == 'intermediate':
                return 'beginner'
        
        return current_difficulty  # No change needed
    
    def _get_common_gaps_for_niche(self, niche: str, experience_level: str) -> List[str]:
        """
        Get common knowledge gaps for specific niche and experience level
        """
        gaps_by_niche = {
            'tech_career': {
                'beginner': ['Python Basics', 'Git Version Control', 'Problem Solving Fundamentals', 'Code Documentation'],
                'intermediate': ['Algorithm Optimization', 'System Design Principles', 'Testing Strategies', 'Code Review Best Practices'],
                'advanced': ['Scalability Patterns', 'Performance Tuning', 'Architecture Design', 'Team Leadership']
            },
            'creator_business': {
                'beginner': ['Content Planning', 'Audience Research', 'Basic Analytics', 'Social Media Fundamentals'],
                'intermediate': ['Email Marketing', 'SEO Optimization', 'Brand Development', 'Monetization Strategies'],
                'advanced': ['Advanced Analytics', 'Automation Systems', 'Partnership Development', 'Scale Management']
            }
        }
        
        return gaps_by_niche.get(niche, {}).get(experience_level, ['General Problem Solving', 'Best Practices', 'Advanced Concepts'])
    
    def _estimate_learning_time(self, concept: str, experience_level: str, niche: str) -> int:
        """
        Estimate learning time in minutes for a concept
        """
        # Base times by experience level
        base_times = {
            'beginner': 60,
            'intermediate': 45,
            'advanced': 30
        }
        
        # Complexity multipliers for different concept types
        complexity_keywords = {
            'basics': 0.8,
            'fundamentals': 0.9,
            'advanced': 1.5,
            'optimization': 1.3,
            'design': 1.4,
            'architecture': 1.6,
            'leadership': 1.2,
            'automation': 1.3
        }
        
        base_time = base_times.get(experience_level, 45)
        
        # Check for complexity keywords
        multiplier = 1.0
        concept_lower = concept.lower()
        for keyword, mult in complexity_keywords.items():
            if keyword in concept_lower:
                multiplier = mult
                break
        
        return int(base_time * multiplier)
    
    def _get_optimal_content_sequence(self, concept: str, learning_style: str, experience_level: str) -> List[str]:
        """
        Get optimal content sequence based on learning style and experience
        """
        sequences = {
            'visual': ['lesson', 'diagram', 'example', 'exercise', 'practice'],
            'auditory': ['lesson', 'discussion', 'example', 'exercise', 'review'],
            'kinesthetic': ['example', 'practice', 'lesson', 'exercise', 'project'],
            'reading_writing': ['lesson', 'notes', 'exercise', 'summary', 'practice']
        }
        
        base_sequence = sequences.get(learning_style, ['lesson', 'example', 'exercise', 'practice'])
        
        # Adjust for experience level
        if experience_level == 'beginner':
            # Add more foundational content
            return ['overview'] + base_sequence + ['review']
        elif experience_level == 'advanced':
            # Focus on application and advanced concepts
            return ['lesson', 'case_study', 'project', 'peer_review']
        
        return base_sequence
    
    def _get_prerequisites(self, concept: str, niche: str) -> List[str]:
        """
        Get prerequisites for a concept
        """
        prerequisites_map = {
            'tech_career': {
                'Algorithm Optimization': ['Python Basics', 'Data Structures'],
                'System Design Principles': ['Programming Fundamentals', 'Database Basics'],
                'Testing Strategies': ['Code Writing', 'Debugging'],
                'Performance Tuning': ['Algorithm Optimization', 'System Design Principles']
            },
            'creator_business': {
                'Email Marketing': ['Content Planning', 'Audience Research'],
                'SEO Optimization': ['Content Creation', 'Basic Analytics'],
                'Monetization Strategies': ['Audience Building', 'Brand Development'],
                'Advanced Analytics': ['Basic Analytics', 'Data Interpretation']
            }
        }
        
        return prerequisites_map.get(niche, {}).get(concept, [])
    
    def _generate_learning_objectives(self, concept: str, experience_level: str) -> List[str]:
        """
        Generate learning objectives for a concept
        """
        if experience_level == 'beginner':
            return [
                f"Understand the basic principles of {concept}",
                f"Identify key components of {concept}",
                f"Apply {concept} in simple scenarios"
            ]
        elif experience_level == 'intermediate':
            return [
                f"Master the core concepts of {concept}",
                f"Apply {concept} to solve complex problems",
                f"Analyze and optimize {concept} implementations"
            ]
        else:  # advanced
            return [
                f"Design advanced solutions using {concept}",
                f"Evaluate trade-offs in {concept} approaches",
                f"Lead others in implementing {concept}"
            ]
    
    def _get_advanced_topics(self, niche: str, current_level: str) -> List[str]:
        """
        Get advanced topics for progression
        """
        advanced_topics = {
            'tech_career': ['Microservices Architecture', 'Machine Learning Integration', 'Cloud Native Development', 'DevOps Automation'],
            'creator_business': ['Advanced Automation', 'Multi-Platform Strategy', 'Community Building', 'Product Development']
        }
        
        return advanced_topics.get(niche, ['Advanced Problem Solving', 'Leadership Skills'])
    
    def _get_reinforcement_topics(self, niche: str, experience_level: str) -> List[str]:
        """
        Get topics for skill reinforcement
        """
        reinforcement_topics = {
            'tech_career': ['Code Review Practice', 'Algorithm Practice', 'Design Pattern Review'],
            'creator_business': ['Content Audit', 'Analytics Review', 'Strategy Refinement']
        }
        
        return reinforcement_topics.get(niche, ['Best Practices Review'])

