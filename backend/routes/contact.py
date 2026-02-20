from fastapi import APIRouter, HTTPException
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from models import ContactMessage, ContactMessageCreate, ContactResponse
from email_service import email_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Database will be injected by server.py
db = None

def set_db(database):
    global db
    db = database

@router.post("/contact/send", response_model=ContactResponse)
async def send_contact_message(contact_data: ContactMessageCreate):
    """
    Handle contact form submission:
    1. Save message to database
    2. Send email notification
    """
    try:
        # Create contact message object
        contact_msg = ContactMessage(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message
        )
        
        # Save to database
        await db.contact_messages.insert_one(contact_msg.dict())
        logger.info(f"Contact message saved to database from {contact_data.email}")
        
        # Send email notification
        email_sent = email_service.send_contact_email(
            name=contact_data.name,
            email=contact_data.email,
            message=contact_data.message
        )
        
        if email_sent:
            return ContactResponse(
                success=True,
                message="Thank you for reaching out! I'll get back to you soon."
            )
        else:
            # Email failed but message is saved
            logger.warning("Email sending failed, but message saved to database")
            return ContactResponse(
                success=True,
                message="Message received! I'll respond shortly."
            )
            
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your message. Please try again or email directly."
        )
