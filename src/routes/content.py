from flask import Blueprint, jsonify, request
from src.models.content import Content, LearningPath, Exercise, db
from src.models.learner import Learner
from src.services.ai_service import AIContentGenerator
import json
from datetime import datetime

content_bp = Blueprint("content", __name__)
ai_generator = AIContentGenerator()

@content_bp.route("/content", methods=["POST"])
def create_content():
    """Create new learning content"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ["title", "content_type", "niche"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        content = Content(
            title=data["title"],
            content_type=data["content_type"],
            niche=data["niche"],
            difficulty_level=data.get("difficulty_level", "intermediate"),
            content_body=data.get("content_body", ""),
            content_metadata=json.dumps(data.get("metadata", {})),
            learning_objectives=json.dumps(data.get("learning_objectives", [])),
            prerequisites=json.dumps(data.get("prerequisites", [])),
            concepts_covered=json.dumps(data.get("concepts_covered", [])),
            is_ai_generated=data.get("is_ai_generated", False),
            generation_prompt=data.get("generation_prompt", ""),
            personalization_params=json.dumps(data.get("personalization_params", {}))
        )
        
        db.session.add(content)
        db.session.commit()
        
        return jsonify(content.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/content", methods=["GET"])
def get_content():
    """Get content with optional filtering"""
    niche = request.args.get("niche")
    content_type = request.args.get("content_type")
    difficulty_level = request.args.get("difficulty_level")
    
    query = Content.query
    
    if niche:
        query = query.filter(Content.niche == niche)
    if content_type:
        query = query.filter(Content.content_type == content_type)
    if difficulty_level:
        query = query.filter(Content.difficulty_level == difficulty_level)
    
    content_items = query.all()
    return jsonify([item.to_dict() for item in content_items])

@content_bp.route("/content/<int:content_id>", methods=["GET"])
def get_content_by_id(content_id):
    """Get specific content by ID"""
    content = Content.query.get_or_404(content_id)
    return jsonify(content.to_dict())

@content_bp.route("/content/<int:content_id>", methods=["PUT"])
def update_content(content_id):
    """Update existing content"""
    try:
        content = Content.query.get_or_404(content_id)
        data = request.json
        
        # Update fields if provided
        if "title" in data:
            content.title = data["title"]
        if "content_body" in data:
            content.content_body = data["content_body"]
        if "difficulty_level" in data:
            content.difficulty_level = data["difficulty_level"]
        if "metadata" in data:
            content.content_metadata = json.dumps(data["metadata"])
        if "learning_objectives" in data:
            content.learning_objectives = json.dumps(data["learning_objectives"])
        if "prerequisites" in data:
            content.prerequisites = json.dumps(data["prerequisites"])
        if "concepts_covered" in data:
            content.concepts_covered = json.dumps(data["concepts_covered"])
        
        content.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(content.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/content/<int:content_id>", methods=["DELETE"])
def delete_content(content_id):
    """Delete content"""
    try:
        content = Content.query.get_or_404(content_id)
        db.session.delete(content)
        db.session.commit()
        return "", 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/learning-paths", methods=["POST"])
def create_learning_path():
    """Create a new learning path for a learner"""
    try:
        data = request.json
        
        if "learner_id" not in data:
            return jsonify({"error": "Missing learner_id"}), 400
        
        # Verify learner exists
        learner = Learner.query.get(data["learner_id"])
        if not learner:
            return jsonify({"error": "Learner not found"}), 404
        
        learning_path = LearningPath(
            learner_id=data["learner_id"],
            path_name=data.get("path_name", f"Learning Path for {learner.target_niche}"),
            target_goal=data.get("target_goal", ""),
            estimated_duration_hours=data.get("estimated_duration_hours", 40),
            content_sequence=json.dumps(data.get("content_sequence", [])),
            adaptation_history=json.dumps([]),
            performance_data=json.dumps({})
        )
        
        db.session.add(learning_path)
        db.session.commit()
        
        return jsonify(learning_path.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/learning-paths/<int:path_id>", methods=["GET"])
def get_learning_path(path_id):
    """Get learning path by ID"""
    path = LearningPath.query.get_or_404(path_id)
    return jsonify(path.to_dict())

@content_bp.route("/learning-paths/learner/<int:learner_id>", methods=["GET"])
def get_learner_paths(learner_id):
    """Get all learning paths for a learner"""
    learner = Learner.query.get_or_404(learner_id)
    paths = LearningPath.query.filter_by(learner_id=learner_id).all()
    return jsonify([path.to_dict() for path in paths])

@content_bp.route("/learning-paths/<int:path_id>/next-content", methods=["GET"])
def get_next_content(path_id):
    """Get the next content item in the learning path"""
    path = LearningPath.query.get_or_404(path_id)
    next_content_id = path.get_next_content()
    
    if next_content_id:
        content = Content.query.get(next_content_id)
        if content:
            return jsonify({
                "path_id": path_id,
                "current_position": path.current_position,
                "next_content": content.to_dict()
            })
        else:
            return jsonify({"error": "Content not found"}), 404
    else:
        return jsonify({
            "path_id": path_id,
            "message": "Learning path completed",
            "completion_status": path.completion_status
        })

@content_bp.route("/learning-paths/<int:path_id>/advance", methods=["POST"])
def advance_learning_path(path_id):
    """Advance to the next content item in the learning path"""
    try:
        path = LearningPath.query.get_or_404(path_id)
        
        # Record performance data if provided
        data = request.json or {}
        if "performance_score" in data:
            performance_data = json.loads(path.performance_data) if path.performance_data else {}
            performance_data[str(path.current_position)] = data["performance_score"]
            path.performance_data = json.dumps(performance_data)
        
        # Advance position
        has_more = path.advance_position()
        db.session.commit()
        
        return jsonify({
            "path_id": path_id,
            "new_position": path.current_position,
            "has_more_content": has_more,
            "completion_status": path.completion_status
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/learning-paths/<int:path_id>/add-content", methods=["POST"])
def add_content_to_path(path_id):
    """Add content to a learning path"""
    try:
        path = LearningPath.query.get_or_404(path_id)
        data = request.json
        
        if "content_id" not in data:
            return jsonify({"error": "Missing content_id"}), 400
        
        # Verify content exists
        content = Content.query.get(data["content_id"])
        if not content:
            return jsonify({"error": "Content not found"}), 404
        
        position = data.get("position")
        path.add_content_to_path(data["content_id"], position)
        db.session.commit()
        
        return jsonify(path.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/learning-paths/<int:path_id>/generate-adaptive", methods=["POST"])
def generate_adaptive_path(path_id):
    """Generate an adaptive learning path based on learner profile"""
    try:
        path = LearningPath.query.get_or_404(path_id)
        learner = Learner.query.get_or_404(path.learner_id)
        
        data = request.json or {}
        target_concepts = data.get("target_concepts", [])
        
        # Get learner\"s knowledge gaps
        knowledge_gaps = learner.get_knowledge_gaps()
        
        # Find relevant content for the learner\"s niche and knowledge gaps
        relevant_content = Content.query.filter(
            Content.niche == learner.target_niche,
            Content.difficulty_level == learner.experience_level
        ).all()
        
        # Simple adaptive algorithm: prioritize content that covers knowledge gaps
        adaptive_sequence = []
        
        # Add content for knowledge gaps first
        for content in relevant_content:
            concepts_covered = json.loads(content.concepts_covered) if content.concepts_covered else []
            if any(gap in concepts_covered for gap in knowledge_gaps):
                adaptive_sequence.append(content.id)
        
        # Add content for target concepts
        for content in relevant_content:
            concepts_covered = json.loads(content.concepts_covered) if content.concepts_covered else []
            if any(concept in concepts_covered for concept in target_concepts):
                if content.id not in adaptive_sequence:
                    adaptive_sequence.append(content.id)
        
        # Update the learning path
        path.content_sequence = json.dumps(adaptive_sequence)
        path.current_position = 0
        
        # Log the adaptation
        adaptation_log = json.loads(path.adaptation_history) if path.adaptation_history else []
        adaptation_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "reason": "adaptive_generation",
            "knowledge_gaps": knowledge_gaps,
            "target_concepts": target_concepts,
            "new_sequence_length": len(adaptive_sequence)
        })
        path.adaptation_history = json.dumps(adaptation_log)
        
        db.session.commit()
        
        return jsonify({
            "path_id": path_id,
            "adaptive_sequence": adaptive_sequence,
            "knowledge_gaps_addressed": knowledge_gaps,
            "target_concepts": target_concepts,
            "sequence_length": len(adaptive_sequence)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/exercises", methods=["POST"])
def create_exercise():
    """Create a new exercise"""
    try:
        data = request.json
        
        if "content_id" not in data or "question" not in data:
            return jsonify({"error": "Missing content_id or question"}), 400
        
        # Verify content exists
        content = Content.query.get(data["content_id"])
        if not content:
            return jsonify({"error": "Content not found"}), 404
        
        exercise = Exercise(
            content_id=data["content_id"],
            question=data["question"],
            exercise_type=data.get("exercise_type", "multiple_choice"),
            correct_answer=data.get("correct_answer", ""),
            explanation=data.get("explanation", ""),
            options=json.dumps(data.get("options", [])),
            starter_code=data.get("starter_code", ""),
            test_cases=json.dumps(data.get("test_cases", [])),
            difficulty_score=data.get("difficulty_score", 0.5),
            estimated_time_minutes=data.get("estimated_time_minutes", 5)
        )
        
        db.session.add(exercise)
        db.session.commit()
        
        return jsonify(exercise.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@content_bp.route("/exercises/content/<int:content_id>", methods=["GET"])
def get_exercises_for_content(content_id):
    """Get all exercises for a specific content item"""
    content = Content.query.get_or_404(content_id)
    exercises = Exercise.query.filter_by(content_id=content_id).all()
    return jsonify([exercise.to_dict() for exercise in exercises])

@content_bp.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    """Get specific exercise by ID"""
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify(exercise.to_dict())

@content_bp.route("/learners/<int:learner_id>/generate-content", methods=["POST"])
def generate_content_for_learner(learner_id):
    """Generate and save personalized content for a learner"""
    try:
        learner = Learner.query.get_or_404(learner_id)
        data = request.json
        
        if "concept" not in data:
            return jsonify({"error": "Missing concept"}), 400
        
        concept = data["concept"]
        content_type = data.get("content_type", "lesson")
        
        personalization_params = {
            "learning_style": learner.preferred_learning_style,
            "experience_level": learner.experience_level,
            "niche": learner.target_niche
        }

        # Generate content using AI service
        if content_type == "lesson":
            generated_data = ai_generator.generate_personalized_content(
                concept=concept,
                content_type="lesson",
                personalization_params=personalization_params
            )
            
            # Create content record
            content = Content(
                title=generated_data.get("title", f"{concept} - Personalized Lesson"),
                content_type="lesson",
                niche=learner.target_niche,
                difficulty_level=learner.experience_level,
                content_body=generated_data.get("content", ""),
                learning_objectives=json.dumps(generated_data.get("learning_objectives", [])),
                concepts_covered=json.dumps([concept]),
                is_ai_generated=True,
                generation_prompt=f"Generate lesson for {concept}",
                personalization_params=json.dumps(personalization_params)
            )
            
        elif content_type == "exercise":
            exercise_type = data.get("exercise_type", "multiple_choice")
            generated_data = ai_generator.generate_personalized_content(
                concept=concept,
                content_type="exercise",
                personalization_params=personalization_params,
                exercise_type=exercise_type
            )
            # Create content record for the exercise
            content = Content(
                title=generated_data.get("title", f"{concept} - Practice Exercise"),
                content_type="exercise",
                niche=learner.target_niche,
                difficulty_level=learner.experience_level,
                content_body=generated_data.get("question", ""),
                concepts_covered=json.dumps([concept]),
                is_ai_generated=True,
                generation_prompt=f"Generate {exercise_type} exercise for {concept}",
                personalization_params=json.dumps(personalization_params)
            )
            db.session.add(content)
            db.session.flush()  # Get the content ID

            # Create exercise record
            exercise = Exercise(
                content_id=content.id,
                question=generated_data.get("question", ""),
                exercise_type=exercise_type,
                correct_answer=generated_data.get("correct_answer", ""),
                explanation=generated_data.get("explanation", ""),
                options=json.dumps(generated_data.get("options", [])),
                starter_code=generated_data.get("starter_code", ""),
                test_cases=json.dumps(generated_data.get("test_cases", [])),
                difficulty_score=generated_data.get("difficulty_score", 0.5),
                estimated_time_minutes=generated_data.get("estimated_time_minutes", 5)
            )
            db.session.add(exercise)

        db.session.commit()
        return jsonify(content.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

