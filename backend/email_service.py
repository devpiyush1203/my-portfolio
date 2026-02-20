import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.email_user = os.environ.get('EMAIL_USER')
        self.email_pass = os.environ.get('EMAIL_PASS')
        self.email_to = os.environ.get('EMAIL_TO')
        
    def send_contact_email(self, name: str, email: str, message: str) -> bool:
        """
        Send contact form email using Gmail SMTP
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = self.email_to
            msg['Subject'] = f'Portfolio Contact Form: Message from {name}'
            
            # Email body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #0891b2;">New Contact Form Submission</h2>
                    <div style="background-color: #f1f5f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Message:</strong></p>
                        <p style="background-color: white; padding: 15px; border-radius: 4px;">{message}</p>
                    </div>
                    <p style="color: #64748b; font-size: 12px;">This email was sent from your portfolio website contact form.</p>
                </body>
            </html>
            """
            
            text_body = f"""
            New Contact Form Submission
            
            Name: {name}
            Email: {email}
            
            Message:
            {message}
            
            ---
            This email was sent from your portfolio website contact form.
            """
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Connect to Gmail SMTP server
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
                
            logger.info(f"Contact form email sent successfully to {self.email_to}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {str(e)}")
            logger.error("Please ensure you're using a Gmail App Password, not your regular password")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

email_service = EmailService()