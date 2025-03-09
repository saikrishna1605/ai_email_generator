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
    allow_origins=["http://127.0.0.1:5500"], 
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

app.mount("/static", StaticFiles(directory="../FrontEnd"), name="static")

app.include_router(feedback_router)

genai.configure(api_key=("genai_api_key"))  

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
        model = genai.GenerativeModel("gemini-1.5-pro")  
        detected_language = None
        words = request.context.lower().split()
        for i, word in enumerate(words):
            if word == "in" and i + 1 < len(words):
                detected_language = words[i + 1].capitalize()
            elif word == "written" and i + 2 < len(words) and words[i + 1] == "in": 
                detected_language = words[i + 2].capitalize()
                break

        if detected_language:
            if "written in" in request.context.lower():
                response_language = request.language 
            else:
                response_language = detected_language 
        else:
            response_language = request.language 

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
    return {"status": "success"}

@app.get("/")
def read_root():
    return {"message": "AI Email Generator API is running!"}