# feedback.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from auth import verify_token

router = APIRouter()
db = firestore.client()

class EmailFeedback(BaseModel):
    email_id: str
    original_content: str
    edited_content: str
    rating: int  # 1-5 scale
    comments: Optional[str] = None

@router.post("/feedback")
async def save_feedback(
    feedback: EmailFeedback,
    user_info: dict = Depends(verify_token)
):
    user_id = user_info["uid"]
    
    # Save feedback to Firestore
    feedback_ref = db.collection("email_feedback").document()
    feedback_ref.set({
        "user_id": user_id,
        "email_id": feedback.email_id,
        "original_content": feedback.original_content,
        "edited_content": feedback.edited_content,
        "rating": feedback.rating,
        "comments": feedback.comments,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    
    # Calculate diff between original and edited for future training
    # (simplified example)
    return {"status": "success", "feedback_id": feedback_ref.id}

@router.get("/analytics/feedback")
async def get_feedback_analytics(user_info: dict = Depends(verify_token)):
    # Only allow admins to access analytics
    if user_info.get("admin") != True:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Query feedback data and calculate metrics
    # Return analytics dashboard data
    return {"average_rating": 4.2, "improvement_metrics": {...}}
def provide_feedback(email_content):
    # Basic feedback
    suggestions = []
    
    # Length check
    if len(email_content.split()) < 50:
        suggestions.append("Consider adding more detail to your email")
    elif len(email_content.split()) > 300:
        suggestions.append("Consider making your email more concise")
    
    # Common phrases check
    cliches = ["touch base", "circle back", "per our conversation", "as per my last email"]
    for cliche in cliches:
        if cliche in email_content.lower():
            suggestions.append(f"Consider replacing the cliché '{cliche}'")
    
    return {"suggestions": suggestions if suggestions else ["Your email looks good!"]}