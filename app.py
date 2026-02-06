"""
CurricuForge - Generative AI Curriculum Designer
Flask Backend Application (Using OpenAI API)
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please add your OpenAI API key to the .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


@app.route('/')
def index():
    """
    Render the main form page where users input curriculum parameters
    """
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_curriculum():
    """
    Handle curriculum generation request
    - Receives form data from frontend
    - Builds a prompt for OpenAI API
    - Returns generated curriculum
    """
    try:
        # Extract form data
        subject = request.form.get('subject', '').strip()
        level = request.form.get('level', 'Beginner')
        duration = request.form.get('duration', '').strip()
        goal = request.form.get('goal', '').strip()
        
        # Validate required fields
        if not subject or not duration:
            return render_template('result.html', 
                                 error="Please provide both Subject and Duration fields.")
        
        # Build the prompt for OpenAI API
        prompt = f"""Create a detailed {duration} curriculum for {level} level students on {subject}.

Please include:
1. Course Overview
2. Week-wise Plan with topics for each week
3. Learning Objectives for each week
4. Assessment Plan
5. Recommended Resources

{f'Special Goal/Focus: {goal}' if goal else ''}

Format the response with clear headings and structured sections. Make it comprehensive and actionable."""

        # Call OpenAI API to generate curriculum
        print(f"Generating curriculum for: {subject} ({level}, {duration})")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4" for better results
            messages=[
                {"role": "system", "content": "You are an expert curriculum designer and educational consultant. Create detailed, well-structured curricula that are practical and actionable."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract the generated text
        curriculum_text = response.choices[0].message.content
        
        # Render result page with generated curriculum
        return render_template('result.html', 
                             curriculum=curriculum_text,
                             subject=subject,
                             level=level,
                             duration=duration,
                             goal=goal)
    
    except Exception as e:
        # Handle any errors during generation
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return render_template('result.html', error=error_message)


if __name__ == '__main__':
    # Run the Flask development server
    print("🚀 Starting CurricuForge - Generative AI Curriculum Designer")
    print("📍 Open your browser at: http://127.0.0.1:5000")
    print("🤖 Using OpenAI GPT-3.5-Turbo")
    app.run(debug=True, host='127.0.0.1', port=5000)
