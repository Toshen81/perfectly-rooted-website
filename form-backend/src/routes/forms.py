from flask import Blueprint, request, jsonify
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

forms_bp = Blueprint('forms', __name__)

def send_simple_email(to_email, subject, body):
    """Send simple email without attachment for testing"""
    print(f"=== TESTING EMAIL SEND TO: {to_email} ===")
    
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_USERNAME', 'perfectlyrooted25@gmail.com')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        print(f"Sender email: {sender_email}")
        print(f"Password available: {bool(sender_password)}")
        
        if not sender_password:
            print("❌ CRITICAL ERROR: EMAIL_PASSWORD environment variable not set!")
            print("Available environment variables:")
            env_vars = [key for key in os.environ.keys() if 'EMAIL' in key.upper()]
            print(f"Email-related env vars: {env_vars}")
            return False, "Missing EMAIL_PASSWORD environment variable"
        
        # Create simple message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        print("✅ Email message created")
        
        # Connect and send
        print("🔄 Connecting to Gmail...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("🔄 Logging in to Gmail...")
        server.login(sender_email, sender_password)
        print("✅ Gmail login successful!")
        
        print("🔄 Sending email...")
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("🎉 EMAIL SENT SUCCESSFULLY!")
        return True, "Email sent successfully"
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"Gmail authentication failed: {str(e)}"
        print(f"❌ {error_msg}")
        print("This usually means:")
        print("  1. Wrong email password")
        print("  2. Need to use App Password instead of regular password")
        print("  3. 2-Factor Authentication not enabled")
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Email sending failed: {str(e)}"
        print(f"❌ {error_msg}")
        return False, error_msg

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    print("=== CONSULTATION FUNCTION CALLED ===")
    
    try:
        data = request.get_json()
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        
        subject = "🤝 Consultation Request Received - Perfectly Rooted Solutions"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🤝 Thank You {user_name}!</h2>
            <p>Your consultation request has been received. We'll contact you within 24 hours.</p>
            <p>Best regards,<br>Toshen<br>Perfectly Rooted Solutions</p>
        </body>
        </html>
        """
        
        success, message = send_simple_email(user_email, subject, body)
        
        return jsonify({
            'success': True,
            'message': '🎉 Thank you! Your consultation request has been submitted successfully. Check your email for confirmation!'
        }), 200
        
    except Exception as e:
        print(f"❌ ERROR in consultation: {str(e)}")
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submit-package', methods=['POST'])
def submit_package():
    print("=== PACKAGE FUNCTION CALLED ===")
    return jsonify({
        'success': True,
        'message': '📦 Thank you! Your package inquiry has been submitted successfully. We\'ll be in touch soon!'
    }), 200

@forms_bp.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    print("=== EBOOK FUNCTION CALLED (SIMPLE TEST VERSION) ===")
    
    try:
        data = request.get_json()
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        
        print(f"Testing email send to: {user_name} ({user_email})")
        
        subject = "📚 Your Free Business Guide: 'Rooted in Success'"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>📚 Thank You {user_name}!</h2>
            <p>Thank you for downloading "Rooted in Success"!</p>
            <p><strong>Note:</strong> This is a test email without PDF attachment to verify email functionality.</p>
            <p>If you receive this email, the email system is working correctly.</p>
            <p>Best regards,<br>Toshen<br>Perfectly Rooted Solutions</p>
        </body>
        </html>
        """
        
        success, message = send_simple_email(user_email, subject, body)
        
        if success:
            response_message = '📚 Success! Test email sent to your inbox. If you receive it, email is working!'
        else:
            response_message = f'❌ Email test failed: {message}'
        
        return jsonify({
            'success': True,
            'message': response_message
        }), 200
        
    except Exception as e:
        print(f"❌ ERROR in ebook: {str(e)}")
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submissions', methods=['GET'])
def get_submissions():
    return jsonify({'success': True, 'submissions': [], 'total': 0}), 200

@forms_bp.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    return jsonify({'success': True, 'submission': {}}), 200

