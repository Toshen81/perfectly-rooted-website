from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Try to import database models - if it fails, we'll handle it gracefully
try:
    from src.models.form_submission import FormSubmission, db
    DATABASE_AVAILABLE = True
    print("Database models imported successfully")
except ImportError as e:
    print(f"Database models not available: {e}")
    DATABASE_AVAILABLE = False

forms_bp = Blueprint('forms', __name__)

def send_email_with_attachment(to_email, subject, body, attachment_path=None):
    """Send email with optional PDF attachment"""
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_USERNAME', 'perfectlyrooted25@gmail.com')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        if not sender_password:
            print("ERROR: EMAIL_PASSWORD environment variable not set")
            return False
            
        print(f"Attempting to send email to: {to_email}")
        print(f"Using sender email: {sender_email}")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'html'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            print(f"Attaching file: {attachment_path}")
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(attachment_path)}'
            )
            msg.attach(part)
            print("PDF attachment added successfully")
        elif attachment_path:
            print(f"WARNING: Attachment file not found: {attachment_path}")
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"ERROR sending email: {str(e)}")
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
                # Continue anyway - don't let database errors break the form
        
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
                # Continue anyway - don't let database errors break the form
        
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
                # Continue anyway - don't let database errors break the form
        
        # Send ebook email with PDF attachment
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        user_subject = "📚 Your Free Business Guide: 'Rooted in Success'"
        
        user_body = f"""
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
                    If you have any questions, please don't hesitate to reach out!
                </p>
            </div>
        </body>
        </html>
        """
        
        # Find the PDF file - try multiple possible locations
        possible_paths = [
            'rooted_in_success_ebook.pdf',
            './rooted_in_success_ebook.pdf',
            '/opt/render/project/src/rooted_in_success_ebook.pdf',
            '/opt/render/project/rooted_in_success_ebook.pdf',
            os.path.join(os.path.dirname(__file__), '..', '..', 'rooted_in_success_ebook.pdf'),
            os.path.join(os.getcwd(), 'rooted_in_success_ebook.pdf')
        ]
        
        pdf_path = None
        for path in possible_paths:
            if os.path.exists(path):
                pdf_path = path
                print(f"Found PDF at: {pdf_path}")
                break
        
        if not pdf_path:
            print("WARNING: PDF file not found in any of the expected locations:")
            for path in possible_paths:
                print(f"  - {path} (exists: {os.path.exists(path)})")
        
        # Send email with PDF attachment
        try:
            email_sent = send_email_with_attachment(user_email, user_subject, user_body, pdf_path)
            
            if email_sent:
                print(f"Ebook email with PDF sent successfully to {user_email}")
            else:
                print(f"Failed to send ebook email to {user_email}")
        except Exception as email_error:
            print(f"Email sending failed: {email_error}")
            # Don't let email errors break the form submission
        
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

