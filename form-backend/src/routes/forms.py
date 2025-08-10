from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

# Try to import database models - if it fails, we'll handle it gracefully
try:
    from src.models.form_submission import FormSubmission, db
    DATABASE_AVAILABLE = True
    print("Database models imported successfully")
except ImportError as e:
    print(f"Database models not available: {e}")
    DATABASE_AVAILABLE = False

# Try to import email modules
try:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    EMAIL_MODULES_AVAILABLE = True
    print("Email modules imported successfully")
except ImportError as e:
    print(f"Email modules not available: {e}")
    EMAIL_MODULES_AVAILABLE = False

forms_bp = Blueprint('forms', __name__)

def send_simple_email(to_email, subject, body):
    """Send simple email without attachment first"""
    try:
        print(f"=== EMAIL DEBUG START ===")
        print(f"Attempting to send email to: {to_email}")
        
        if not EMAIL_MODULES_AVAILABLE:
            print("ERROR: Email modules not available")
            return False
        
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_USERNAME', 'perfectlyrooted25@gmail.com')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        print(f"Sender email: {sender_email}")
        print(f"Password available: {bool(sender_password)}")
        
        if not sender_password:
            print("ERROR: EMAIL_PASSWORD environment variable not set")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'html'))
        print("Email message created successfully")
        
        # Send email
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("SMTP connection established")
        
        server.login(sender_email, sender_password)
        print("SMTP login successful")
        
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        print(f"=== EMAIL DEBUG END ===")
        return True
        
    except Exception as e:
        print(f"ERROR sending email: {str(e)}")
        print(f"=== EMAIL DEBUG END (ERROR) ===")
        return False

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    try:
        data = request.get_json()
        print(f"Consultation submission received: {data}")
        
        # Try to save to database if available
        if DATABASE_AVAILABLE:
            try:
                submission = FormSubmission(
                    form_type='consultation',
                    name=data.get('name'),
                    email=data.get('email'),
                    phone=data.get('phone'),
                    company=data.get('company'),
                    message=data.get('message'),
                    additional_data=json.dumps({
                        'interest': data.get('interest'),
                        'submitted_at': datetime.utcnow().isoformat()
                    })
                )
                
                db.session.add(submission)
                db.session.commit()
                print(f"Consultation saved to database for {data.get('email')}")
                
            except Exception as db_error:
                print(f"Database save failed: {db_error}")
        
        return jsonify({
            'success': True,
            'message': 'Consultation request submitted successfully'
        }), 200
        
    except Exception as e:
        print(f"Error in submit_consultation: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@forms_bp.route('/submit-package', methods=['POST'])
def submit_package():
    try:
        data = request.get_json()
        print(f"Package submission received: {data}")
        
        # Try to save to database if available
        if DATABASE_AVAILABLE:
            try:
                submission = FormSubmission(
                    form_type='package',
                    name=data.get('name'),
                    email=data.get('email'),
                    phone=data.get('phone'),
                    company=data.get('company'),
                    message=data.get('message'),
                    additional_data=json.dumps({
                        'package': data.get('package'),
                        'submitted_at': datetime.utcnow().isoformat()
                    })
                )
                
                db.session.add(submission)
                db.session.commit()
                print(f"Package inquiry saved to database for {data.get('email')}")
                
            except Exception as db_error:
                print(f"Database save failed: {db_error}")
        
        return jsonify({
            'success': True,
            'message': 'Package inquiry submitted successfully'
        }), 200
        
    except Exception as e:
        print(f"Error in submit_package: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@forms_bp.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    try:
        data = request.get_json()
        print(f"Ebook submission received: {data}")
        
        # Try to save to database if available
        if DATABASE_AVAILABLE:
            try:
                submission = FormSubmission(
                    form_type='ebook',
                    name=data.get('name'),
                    email=data.get('email'),
                    company=data.get('business_name'),
                    additional_data=json.dumps({
                        'submitted_at': datetime.utcnow().isoformat()
                    })
                )
                
                db.session.add(submission)
                db.session.commit()
                print(f"Ebook request saved to database for {data.get('email')}")
                
            except Exception as db_error:
                print(f"Database save failed: {db_error}")
        
        # SEND EMAIL - This is the important part
        print("=== STARTING EMAIL PROCESS ===")
        
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        user_subject = "📚 Your Free Business Guide: 'Rooted in Success'"
        
        user_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #002147;">📚 Thank You for Downloading "Rooted in Success"!</h2>
                
                <p>Hi {user_name},</p>
                
                <p>Thank you for your interest in growing your business with strategic guidance!</p>
                
                <p><strong>Note:</strong> This is a test email to confirm email delivery is working. The PDF attachment will be added once we confirm emails are being sent successfully.</p>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style="color: #002147; margin-top: 0;">📖 What's Inside Your Guide:</h3>
                    <ul style="margin: 10px 0;">
                        <li>Strategic planning frameworks for sustainable growth</li>
                        <li>Essential business structure foundations</li>
                        <li>Proven systems for scaling your operations</li>
                        <li>Actionable insights from real business transformations</li>
                    </ul>
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
            </div>
        </body>
        </html>
        """
        
        # Send simple email first (without attachment)
        try:
            print("Calling send_simple_email function...")
            email_sent = send_simple_email(user_email, user_subject, user_body)
            
            if email_sent:
                print(f"SUCCESS: Email sent to {user_email}")
            else:
                print(f"FAILED: Could not send email to {user_email}")
                
        except Exception as email_error:
            print(f"EXCEPTION in email sending: {email_error}")
        
        print("=== EMAIL PROCESS COMPLETE ===")
        
        return jsonify({
            'success': True,
            'message': 'Ebook request processed successfully'
        }), 200
        
    except Exception as e:
        print(f"Error in submit_ebook: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@forms_bp.route('/submissions', methods=['GET'])
def get_submissions():
    try:
        if not DATABASE_AVAILABLE:
            return jsonify({
                'success': True,
                'submissions': [],
                'total': 0,
                'message': 'Database not available'
            }), 200
        
        submissions = FormSubmission.query.order_by(FormSubmission.created_at.desc()).all()
        
        submissions_data = []
        for submission in submissions:
            submission_dict = {
                'id': submission.id,
                'form_type': submission.form_type,
                'name': submission.name,
                'email': submission.email,
                'phone': submission.phone,
                'company': submission.company,
                'message': submission.message,
                'created_at': submission.created_at.isoformat() if submission.created_at else None
            }
            
            if submission.additional_data:
                try:
                    additional_data = json.loads(submission.additional_data)
                    submission_dict.update(additional_data)
                except json.JSONDecodeError:
                    pass
            
            submissions_data.append(submission_dict)
        
        return jsonify({
            'success': True,
            'submissions': submissions_data,
            'total': len(submissions_data)
        }), 200
        
    except Exception as e:
        print(f"Error in get_submissions: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while retrieving submissions'
        }), 500

@forms_bp.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    try:
        if not DATABASE_AVAILABLE:
            return jsonify({
                'success': True,
                'submission': {},
                'message': 'Database not available'
            }), 200
        
        submission = FormSubmission.query.get_or_404(submission_id)
        
        submission_dict = {
            'id': submission.id,
            'form_type': submission.form_type,
            'name': submission.name,
            'email': submission.email,
            'phone': submission.phone,
            'company': submission.company,
            'message': submission.message,
            'created_at': submission.created_at.isoformat() if submission.created_at else None
        }
        
        if submission.additional_data:
            try:
                additional_data = json.loads(submission.additional_data)
                submission_dict.update(additional_data)
            except json.JSONDecodeError:
                pass
        
        return jsonify({
            'success': True,
            'submission': submission_dict
        }), 200
        
    except Exception as e:
        print(f"Error in get_submission: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while retrieving the submission'
        }), 500

