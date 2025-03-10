from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from tone_analyzer import analyze_tone
from feedback import provide_feedback, router as feedback_router
from auth import verify_token
import google.generativeai as genai
import os
from sendgrid_integration import router as sendgrid_router
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PIL import Image
import io
from typing import List


load_dotenv() 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sendgrid_router, prefix="/email", tags=["email"])
app.include_router(feedback_router)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        model = genai.GenerativeModel("gemini-1.5-pro-vision")
        response = model.generate_content(image)
        return response.text if response.text else "No insights extracted."
    except Exception as e:
        return str(e)

@app.post("/generate-email")
async def generate_email(
    recipient_name: str = Form(...),
    recipient_email: str = Form(...),
    context: str = Form(...),
    purpose: str = Form(...),
    tone: str = Form("professional"),
    language: str = Form("english"),
    files: List[UploadFile] = File(None)
):
    try:
        additional_context = ""
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # Detect language from context
        detected_language = None
        words = context.lower().split()
        for i, word in enumerate(words):
            if word == "in" and i + 1 < len(words):  # Example: "in Hindi"
                detected_language = words[i + 1].capitalize()
            elif word == "written" and i + 2 < len(words) and words[i + 1] == "in":  # Example: "written in Russian"
                detected_language = words[i + 2].capitalize()
                break

        # Handle file uploads
        if files:
            for file in files:
                file_content = await file.read()
                if file.content_type.startswith("image/"):
                    extracted_text = extract_text_from_image(file_content)
                    additional_context += f"\n\nInsights from {file.filename}: {extracted_text}"
                else:
                    additional_context += f"\n\nExtracted from {file.filename}: {file_content.decode(errors='ignore')[:500]}"
        
        # Set response language
        response_language = language if "written in" in context.lower() else (detected_language or language)

        prompt = f"""
        Write a {tone} email in {response_language} to {recipient_name} ({recipient_email}).

        Context: {context}
        Purpose: {purpose}
        Additional Information:{additional_context}

        - If the user specifies "written in [language]", write the response in {language} but refer to the content in the specified language.
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