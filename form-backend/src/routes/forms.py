from flask import Blueprint, request, jsonify
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import sys

# Configure logging to ensure output appears in Render logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

forms_bp = Blueprint('forms', __name__)

def send_email_with_logging(to_email, subject, body, attachment_path=None):
    """Send email with detailed logging"""
    logger.info(f"=== EMAIL SEND ATTEMPT TO: {to_email} ===")
    
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_USERNAME', 'perfectlyrooted25@gmail.com')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        logger.info(f"Sender email: {sender_email}")
        logger.info(f"Password available: {bool(sender_password)}")
        logger.info(f"Password length: {len(sender_password) if sender_password else 0}")
        
        if not sender_password:
            logger.error("CRITICAL: EMAIL_PASSWORD environment variable not set!")
            return False, "Missing EMAIL_PASSWORD"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        logger.info("Email message created successfully")
        
        # Add attachment if provided
        if attachment_path:
            logger.info(f"Checking for attachment: {attachment_path}")
            if os.path.exists(attachment_path):
                logger.info(f"Attaching file: {attachment_path}")
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= rooted_in_success_ebook.pdf'
                )
                msg.attach(part)
                logger.info("PDF attachment added successfully")
            else:
                logger.warning(f"Attachment file not found: {attachment_path}")
        
        # Connect to Gmail and send
        logger.info("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        logger.info("Starting TLS encryption...")
        server.starttls()
        logger.info("Attempting Gmail login...")
        server.login(sender_email, sender_password)
        logger.info("Gmail login successful!")
        
        logger.info("Sending email...")
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        logger.info("EMAIL SENT SUCCESSFULLY!")
        return True, "Email sent successfully"
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"Gmail authentication failed: {str(e)}"
        logger.error(error_msg)
        logger.error("This usually means:")
        logger.error("  1. Wrong email password")
        logger.error("  2. Need to use App Password instead of regular password")
        logger.error("  3. 2-Factor Authentication not enabled")
        return False, error_msg
        
    except smtplib.SMTPException as e:
        error_msg = f"SMTP Error: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Error type: {type(e).__name__}")
        return False, error_msg

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    logger.info("=== CONSULTATION FUNCTION CALLED ===")
    
    try:
        data = request.get_json()
        logger.info(f"Consultation data received: {data}")
        
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        
        subject = "🤝 Consultation Request Received - Perfectly Rooted Solutions"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #002147;">🤝 Thank You for Your Consultation Request!</h2>
                <p>Hi {user_name},</p>
                <p>Thank you for reaching out to Perfectly Rooted Solutions! I've received your consultation request and will get back to you within 24 hours.</p>
                <p>Best regards,<br><strong>Toshen</strong><br>Founder, Perfectly Rooted Solutions</p>
            </div>
        </body>
        </html>
        """
        
        logger.info("Sending consultation confirmation email...")
        success, message = send_email_with_logging(user_email, subject, body)
        
        if success:
            logger.info("Consultation email sent successfully")
        else:
            logger.error(f"Failed to send consultation email: {message}")
        
        return jsonify({
            'success': True,
            'message': '🎉 Thank you! Your consultation request has been submitted successfully. Check your email for confirmation!'
        }), 200
        
    except Exception as e:
        logger.error(f"ERROR in consultation function: {str(e)}")
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submit-package', methods=['POST'])
def submit_package():
    logger.info("=== PACKAGE FUNCTION CALLED ===")
    
    try:
        data = request.get_json()
        logger.info(f"Package data: {data}")
        
        return jsonify({
            'success': True,
            'message': '📦 Thank you! Your package inquiry has been submitted successfully. We\'ll be in touch soon!'
        }), 200
        
    except Exception as e:
        logger.error(f"ERROR in package: {str(e)}")
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    logger.info("=== EBOOK FUNCTION CALLED ===")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    try:
        data = request.get_json()
        logger.info(f"Ebook data received: {data}")
        
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        
        logger.info(f"Processing ebook request for: {user_name} ({user_email})")
        
        # Create ebook email
        subject = "📚 Your Free Business Guide: 'Rooted in Success'"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #002147;">📚 Thank You for Downloading "Rooted in Success"!</h2>
                
                <p>Hi {user_name},</p>
                
                <p>Thank you for your interest in growing your business with strategic guidance! <strong>Your free business guide is attached to this email as a PDF.</strong></p>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style="color: #002147; margin-top: 0;">📖 What's Inside Your Guide:</h3>
                    <ul style="margin: 10px 0;">
                        <li>Strategic planning frameworks for sustainable growth</li>
                        <li>Essential business structure foundations</li>
                        <li>Proven systems for scaling your operations</li>
                        <li>Actionable insights from real business transformations</li>
                    </ul>
                </div>
                
                <p>Best regards,<br><strong>Toshen</strong><br>Founder, Perfectly Rooted Solutions</p>
            </div>
        </body>
        </html>
        """
        
        # Find PDF file
        possible_paths = [
            'rooted_in_success_ebook.pdf',
            './rooted_in_success_ebook.pdf',
            '/opt/render/project/src/rooted_in_success_ebook.pdf',
            '/opt/render/project/rooted_in_success_ebook.pdf',
            'src/rooted_in_success_ebook.pdf'
        ]
        
        pdf_path = None
        logger.info("Searching for PDF file...")
        for path in possible_paths:
            logger.info(f"Checking: {path}")
            if os.path.exists(path):
                pdf_path = path
                logger.info(f"Found PDF at: {pdf_path}")
                break
            else:
                logger.info(f"Not found: {path}")
        
        if not pdf_path:
            logger.warning("PDF file not found in any location")
            logger.info("Available files in current directory:")
            try:
                files = os.listdir('.')
                for file in files[:10]:
                    logger.info(f"  - {file}")
            except Exception as e:
                logger.error(f"Could not list directory: {e}")
        
        logger.info("Sending ebook email...")
        success, message = send_email_with_logging(user_email, subject, body, pdf_path)
        
        if success:
            logger.info("Ebook email sent successfully!")
        else:
            logger.error(f"Failed to send ebook email: {message}")
        
        return jsonify({
            'success': True,
            'message': '📚 Success! Your free business guide has been sent to your email. Check your inbox (and spam folder) for the PDF!'
        }), 200
        
    except Exception as e:
        logger.error(f"ERROR in ebook function: {str(e)}")
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submissions', methods=['GET'])
def get_submissions():
    logger.info("=== SUBMISSIONS FUNCTION CALLED ===")
    return jsonify({
        'success': True,
        'submissions': [],
        'total': 0
    }), 200

@forms_bp.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    logger.info(f"=== GET SUBMISSION FUNCTION CALLED: {submission_id} ===")
    return jsonify({
        'success': True,
        'submission': {}
    }), 200

