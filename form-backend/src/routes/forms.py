from flask import Blueprint, request, jsonify
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

forms_bp = Blueprint('forms', __name__)

def send_email(to_email, subject, body, attachment_path=None):
    """Send email with optional attachment"""
    print(f"=== SENDING EMAIL TO: {to_email} ===")
    
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_USERNAME', 'perfectlyrooted25@gmail.com')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        print(f"Sender: {sender_email}")
        print(f"Password available: {bool(sender_password)}")
        
        if not sender_password:
            print("ERROR: No email password available")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        print("Email message created")
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            print(f"Attaching file: {attachment_path}")
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= rooted_in_success_ebook.pdf'
            )
            msg.attach(part)
            print("PDF attachment added")
        elif attachment_path:
            print(f"WARNING: Attachment file not found: {attachment_path}")
        
        # Connect to Gmail and send
        print("Connecting to Gmail...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("Gmail login...")
        server.login(sender_email, sender_password)
        print("Gmail login successful")
        
        print("Sending email...")
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        print("EMAIL SENT SUCCESSFULLY!")
        return True
        
    except Exception as e:
        print(f"ERROR sending email: {str(e)}")
        return False

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    print("=== CONSULTATION FUNCTION CALLED ===")
    
    try:
        data = request.get_json()
        print(f"Consultation data: {data}")
        
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        
        # Send confirmation email to user
        subject = "🤝 Consultation Request Received - Perfectly Rooted Solutions"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #002147;">🤝 Thank You for Your Consultation Request!</h2>
                
                <p>Hi {user_name},</p>
                
                <p>Thank you for reaching out to Perfectly Rooted Solutions! I've received your consultation request and will get back to you within 24 hours.</p>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style="color: #002147; margin-top: 0;">📋 Your Request Details:</h3>
                    <p><strong>Name:</strong> {data.get('name', 'Not provided')}</p>
                    <p><strong>Email:</strong> {data.get('email', 'Not provided')}</p>
                    <p><strong>Phone:</strong> {data.get('phone', 'Not provided')}</p>
                    <p><strong>Company:</strong> {data.get('company', 'Not provided')}</p>
                    <p><strong>Message:</strong> {data.get('message', 'Not provided')}</p>
                </div>
                
                <p>I'm excited to learn more about your business and discuss how we can help you achieve your goals!</p>
                
                <p>Best regards,<br>
                <strong>Toshen</strong><br>
                Founder, Perfectly Rooted Solutions<br>
                📧 perfectlyrooted25@gmail.com<br>
                📞 800.893.0006</p>
            </div>
        </body>
        </html>
        """
        
        print("Sending consultation confirmation email...")
        email_sent = send_email(user_email, subject, body)
        
        if email_sent:
            print("Consultation email sent successfully")
        else:
            print("Failed to send consultation email")
        
        return jsonify({
            'success': True,
            'message': '🎉 Thank you! Your consultation request has been submitted successfully. Check your email for confirmation!'
        }), 200
        
    except Exception as e:
        print(f"ERROR in consultation: {str(e)}")
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submit-package', methods=['POST'])
def submit_package():
    print("=== PACKAGE FUNCTION CALLED ===")
    
    try:
        data = request.get_json()
        print(f"Package data: {data}")
        
        return jsonify({
            'success': True,
            'message': '📦 Thank you! Your package inquiry has been submitted successfully. We\'ll be in touch soon!'
        }), 200
        
    except Exception as e:
        print(f"ERROR in package: {str(e)}")
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    print("=== EBOOK FUNCTION CALLED ===")
    
    try:
        data = request.get_json()
        print(f"Ebook data: {data}")
        
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        
        print(f"Processing ebook request for: {user_name} ({user_email})")
        
        # Create beautiful ebook email
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
                
                <div style="background: #002147; color: white; padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center;">
                    <p style="margin: 0; font-size: 16px;"><strong>📎 Your PDF guide is attached to this email!</strong></p>
                    <p style="margin: 5px 0 0 0; font-size: 14px;">Look for "rooted_in_success_ebook.pdf" in your email attachments</p>
                </div>
                
                <p>Ready to take the next step? I'd love to discuss how we can help your business grow and thrive.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://perfectly-rooted.com/contact.html" style="background: #002147; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; display: inline-block;">📅 Schedule Your Free Consultation</a>
                </div>
                
                <p>Best regards,<br>
                <strong>Toshen</strong><br>
                Founder, Perfectly Rooted Solutions<br>
                📧 perfectlyrooted25@gmail.com<br>
                📞 800.893.0006</p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="font-size: 12px; color: #666;">
                    You're receiving this email because you downloaded our free business guide from perfectly-rooted.com.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Find PDF file - check multiple possible locations
        possible_paths = [
            'rooted_in_success_ebook.pdf',
            './rooted_in_success_ebook.pdf',
            '/opt/render/project/src/rooted_in_success_ebook.pdf',
            '/opt/render/project/rooted_in_success_ebook.pdf',
            '/opt/render/project/src/form-backend/rooted_in_success_ebook.pdf',
            '/opt/render/project/form-backend/rooted_in_success_ebook.pdf'
        ]
        
        pdf_path = None
        print("Searching for PDF file...")
        for path in possible_paths:
            print(f"Checking: {path}")
            if os.path.exists(path):
                pdf_path = path
                print(f"✅ Found PDF at: {pdf_path}")
                break
            else:
                print(f"❌ Not found: {path}")
        
        if not pdf_path:
            print("⚠️ WARNING: PDF file not found in any location")
            print("Available files in current directory:")
            try:
                for file in os.listdir('.'):
                    print(f"  - {file}")
            except:
                print("  Could not list directory contents")
        
        print("Sending ebook email with PDF attachment...")
        email_sent = send_email(user_email, subject, body, pdf_path)
        
        if email_sent:
            print("✅ Ebook email sent successfully!")
        else:
            print("❌ Failed to send ebook email")
        
        return jsonify({
            'success': True,
            'message': '📚 Success! Your free business guide has been sent to your email. Check your inbox (and spam folder) for the PDF!'
        }), 200
        
    except Exception as e:
        print(f"ERROR in ebook function: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': '❌ An error occurred while processing your request. Please try again.'
        }), 500

@forms_bp.route('/submissions', methods=['GET'])
def get_submissions():
    print("=== SUBMISSIONS FUNCTION CALLED ===")
    return jsonify({
        'success': True,
        'submissions': [],
        'total': 0
    }), 200

@forms_bp.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    print(f"=== GET SUBMISSION FUNCTION CALLED: {submission_id} ===")
    return jsonify({
        'success': True,
        'submission': {}
    }), 200

