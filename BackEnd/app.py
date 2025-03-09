# filepath: c:\Users\saikr\OneDrive\Desktop\ai_email_generator\BackEnd\app.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from tone_analyzer import analyze_tone
from feedback import provide_feedback, router as feedback_router
from auth import verify_token
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow only trusted origins
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="../FrontEnd"), name="static")

# Include feedback router
app.include_router(feedback_router)

# Configure GenAI API Key
genai.configure(api_key=("AIzaSyAlFvGmE0bu7nTnUqlu1QI1ipaSa_1YaFI"))  # Hardcoded (not recommended)

class EmailRequest(BaseModel):
    recipient_name: str
    recipient_email: str
    context: str
    purpose: str
    tone: str = "professional"
    language: str = "english"

@app.post("/generate-email")
async def generate_email(request: EmailRequest):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Use Google's AI model
        detected_language = None
        words = request.context.lower().split()
        for i, word in enumerate(words):
            if word == "in" and i + 1 < len(words):  # Example: "in Hindi"
                detected_language = words[i + 1].capitalize()
            elif word == "written" and i + 2 < len(words) and words[i + 1] == "in":  # Example: "written in Russian"
                detected_language = words[i + 2].capitalize()
                break

        # Determine the response language based on user input
        if detected_language:
            if "written in" in request.context.lower():
                response_language = request.language  # Use user-specified language (default: English)
            else:
                response_language = detected_language  # Use the detected language from context
        else:
            response_language = request.language  # Default user-selected language

        prompt = f"""
        Write a {request.tone} email in {response_language} to {request.recipient_name} ({request.recipient_email}).
        
        Context: {request.context}
        Purpose: {request.purpose}

        - If the user specifies "written in [language]", write the response in {request.language} but refer to the content in the specified language.
        - If the user specifies "in [language]", write the entire email in that language.
        - Do not provide explanations or formatting suggestions.
        - Only return the generated email content, nothing else.
        """

        response = model.generate_content(prompt)

        email_content = response.text if response.text else "AI failed to generate email."

        tone_analysis = analyze_tone(email_content)
        feedback = provide_feedback(email_content)

        return {"email_content": email_content, "tone_analysis": tone_analysis, "feedback": feedback}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/user/preferences")
async def save_preferences(
    preferences: dict,
    user_info: dict = Depends(verify_token)
):
    user_id = user_info["uid"]
    # Save preferences to database
    return {"status": "success"}

@app.get("/")
def read_root():
    return {"message": "AI Email Generator API is running!"}