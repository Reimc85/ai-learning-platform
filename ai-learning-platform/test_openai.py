#!/usr/bin/env python3.11

import os
import sys
sys.path.insert(0, '/home/ubuntu/ai_learning_platform')

from dotenv import load_dotenv
load_dotenv('/home/ubuntu/ai_learning_platform/.env')

print("Testing OpenAI API connectivity...")
print(f"OpenAI API Key present: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

if os.getenv('OPENAI_API_KEY'):
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key starts with: {api_key[:10]}...")
    print(f"API Key length: {len(api_key)}")

try:
    from openai import OpenAI
    print("OpenAI library imported successfully")
    
    if os.getenv('OPENAI_API_KEY'):
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("OpenAI client created successfully")
        
        # Test a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello, AI integration test successful!'"}
            ],
            max_tokens=50
        )
        
        print("API call successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    else:
        print("No API key found - would use mock content")
        
except ImportError as e:
    print(f"OpenAI library import failed: {e}")
except Exception as e:
    print(f"OpenAI API call failed: {e}")

# Test the AI service directly
try:
    from src.services.ai_service import AIContentGenerator
    ai_gen = AIContentGenerator()
    print(f"AI Generator openai_available: {ai_gen.openai_available}")
    
    # Test content generation
    test_params = {
        'learning_style': 'visual',
        'experience_level': 'beginner',
        'niche': 'tech_career'
    }
    
    result = ai_gen.generate_personalized_content(
        concept="Test Concept",
        content_type="lesson",
        personalization_params=test_params
    )
    
    print("Content generation test:")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Content length: {len(result.get('content', ''))}")
    
except Exception as e:
    print(f"AI service test failed: {e}")

