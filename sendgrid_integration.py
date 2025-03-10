# # sendgrid_integration.py
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail, Content, Email
# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel

# router = APIRouter()

# class EmailSendRequest(BaseModel):
#     email_content: str
#     recipient_email: str
#     sender_email: str
#     subject: str
#     sender_name: str = "AI Email Generator"

# @router.post("/send-email")
# async def send_email(request: EmailSendRequest):
#     from_email = Email(request.sender_email)
#     to_email = Email(request.recipient_email)
#     content = Content("text/plain", request.email_content)
    
#     message = Mail(from_email=from_email, to_emails=to_email, subject=request.subject, plain_text_content=content)
    
#     try:
#         response = sg.send(message)
#         return {"status": "success", "status_code": response.status_code}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

class EmailRequest(BaseModel):
    from_email: str
    to_email: str
    subject: str
    content: str

def send_email_with_sendgrid(from_email, to_email, subject, content):
    try:
        if not SENDGRID_API_KEY:
            raise ValueError("SendGrid API key is missing!")

        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

        message = Mail(
            from_email=Email(from_email),
            to_emails=To(to_email),
            subject=subject,
            plain_text_content=Content("text/plain", content)
        )

        response = sg.send(message)
        if response.status_code != 202:
            raise Exception(f"SendGrid Error: {response.status_code} - {response.body}")

        return {"message": "Email sent successfully!", "status": response.status_code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-email")
async def send_email(request: EmailRequest):
    return send_email_with_sendgrid(request.from_email, request.to_email, request.subject, request.content)
