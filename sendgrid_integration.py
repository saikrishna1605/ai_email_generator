import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from fastapi import FastAPI,APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
app = FastAPI() 
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
print(f"SENDGRID_API_KEY: {SENDGRID_API_KEY}")

class EmailRequest(BaseModel):
    from_email: str
    to_email: str
    subject: str
    content: str
def send_email_with_sendgrid(from_email, to_email, subject, content):
    try:
        if not SENDGRID_API_KEY:
            raise ValueError("SendGrid API key is missing!")
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        message = Mail(
            from_email=Email(from_email),
            to_emails=To(to_email),
            subject=subject,
            plain_text_content=content 
        )
        response = sg.send(message)
        if response.status_code != 202:
            raise Exception(f"SendGrid Error: {response.status_code} - {response.body}")

        return {"message": "Email sent successfully!", "status": response.status_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/test-sendgrid")
async def test_sendgrid():
    return {"message": "SendGrid integration is working"}
@router.post("/send-email")
async def send_email(request: EmailRequest):
    return send_email_with_sendgrid(request.from_email, request.to_email, request.subject, request.content)
app.include_router(router)