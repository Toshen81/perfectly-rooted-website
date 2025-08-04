from flask import Blueprint, request, jsonify
from src.models.form_submission import FormSubmission, db
from datetime import datetime
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

forms_bp = Blueprint('forms', __name__)

def send_email_with_attachment(to_email, subject, body, attachment_path=None):
    """Send email with optional attachment"""
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "perfectlyrooted25@gmail.com"
        sender_password = os.environ.get('EMAIL_PASSWORD', 'your-app-password-here')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'html'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(attachment_path)}',
            )
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    """Handle consultation form submissions"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Create new form submission
        submission = FormSubmission(
            form_type='consultation',
            name=data.get('name', ''),
            email=data.get('email', ''),
            company=data.get('company', ''),
            interest=data.get('interest', ''),
            message=data.get('message', ''),
            phone=data.get('phone', ''),
            submission_data=json.dumps(data),
            submitted_at=datetime.utcnow()
        )
        
        db.session.add(submission)
        db.session.commit()
        
        # Send admin notification email
        admin_subject = f"New Consultation Request from {submission.name}"
        admin_body = f"""
        <html>
        <body>
            <h2>New Consultation Request</h2>
            <p><strong>Name:</strong> {submission.name}</p>
            <p><strong>Email:</strong> {submission.email}</p>
            <p><strong>Phone:</strong> {submission.phone or 'Not provided'}</p>
            <p><strong>Business:</strong> {submission.company or 'Not provided'}</p>
            <p><strong>Interest:</strong> {submission.interest or 'Not provided'}</p>
            <p><strong>Message:</strong> {submission.message or 'Not provided'}</p>
            <p><strong>Submitted:</strong> {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """
        
        send_email_with_attachment(
            to_email="info@perfectly-rooted.com",
            subject=admin_subject,
            body=admin_body
        )
        
        return jsonify({
            'success': True,
            'message': 'Form submitted successfully!',
            'submission_id': submission.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting form: {str(e)}'
        }), 500

@forms_bp.route('/submit-package', methods=['POST'])
def submit_package():
    """Handle package inquiry form submissions"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Create new form submission
        submission = FormSubmission(
            form_type='package',
            name=data.get('name', ''),
            email=data.get('email', ''),
            company=data.get('company', ''),
            interest=data.get('package', ''),
            message=data.get('message', ''),
            phone=data.get('phone', ''),
            submission_data=json.dumps(data),
            submitted_at=datetime.utcnow()
        )
        
        db.session.add(submission)
        db.session.commit()
        
        # Send admin notification email
        admin_subject = f"New Package Inquiry from {submission.name}"
        admin_body = f"""
        <html>
        <body>
            <h2>New Package Inquiry</h2>
            <p><strong>Name:</strong> {submission.name}</p>
            <p><strong>Email:</strong> {submission.email}</p>
            <p><strong>Phone:</strong> {submission.phone or 'Not provided'}</p>
            <p><strong>Business:</strong> {submission.company or 'Not provided'}</p>
            <p><strong>Package Interest:</strong> {submission.interest or 'Not provided'}</p>
            <p><strong>Message:</strong> {submission.message or 'Not provided'}</p>
            <p><strong>Submitted:</strong> {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """
        
        send_email_with_attachment(
            to_email="info@perfectly-rooted.com",
            subject=admin_subject,
            body=admin_body
        )
        
        return jsonify({
            'success': True,
            'message': 'Package inquiry submitted successfully!',
            'submission_id': submission.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting form: {str(e)}'
        }), 500

@forms_bp.route('/submit-ebook', methods=['POST'])
def submit_ebook():
    """Handle ebook download form submissions"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Create new form submission
        submission = FormSubmission(
            form_type='ebook',
            name=data.get('name', ''),
            email=data.get('email', ''),
            company=data.get('business_name', ''),
            interest='ebook_download',
            message='Ebook download request',
            submission_data=json.dumps(data),
            submitted_at=datetime.utcnow()
        )
        
        db.session.add(submission)
        db.session.commit()
        
        # Send ebook to user
        user_subject = "Your Free Business Guide: 'Rooted in Success'"
        user_body = f"""
        <html>
        <body>
            <h2>Thank you, {submission.name}!</h2>
            <p>Here's your free business guide: <strong>"Rooted in Success: A Strategic Guide for Growing Entrepreneurs"</strong></p>
            
            <p>This comprehensive guide includes:</p>
            <ul>
                <li>Strategic planning frameworks</li>
                <li>Systems and processes for growth</li>
                <li>Leadership development strategies</li>
                <li>Actionable steps for scaling your business</li>
            </ul>
            
            <p>I hope you find tremendous value in this guide. If you have any questions or would like to discuss how we can help your business grow, please don't hesitate to reach out.</p>
            
            <p>Best regards,<br>
            <strong>Toshen Poole</strong><br>
            Perfectly Rooted Solutions<br>
            <a href="https://perfectly-rooted.com">perfectly-rooted.com</a><br>
            info@perfectly-rooted.com</p>
        </body>
        </html>
        """
        
        # Get the ebook path
        ebook_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rooted_in_success_ebook.pdf')
        
        send_email_with_attachment(
            to_email=submission.email,
            subject=user_subject,
            body=user_body,
            attachment_path=ebook_path
        )
        
        # Send admin notification
        admin_subject = f"New Ebook Download from {submission.name}"
        admin_body = f"""
        <html>
        <body>
            <h2>New Ebook Download</h2>
            <p><strong>Name:</strong> {submission.name}</p>
            <p><strong>Email:</strong> {submission.email}</p>
            <p><strong>Business:</strong> {submission.company or 'Not provided'}</p>
            <p><strong>Downloaded:</strong> {submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """
        
        send_email_with_attachment(
            to_email="info@perfectly-rooted.com",
            subject=admin_subject,
            body=admin_body
        )
        
        return jsonify({
            'success': True,
            'message': 'Ebook sent successfully!',
            'submission_id': submission.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error processing ebook request: {str(e)}'
        }), 500

@forms_bp.route('/submissions', methods=['GET'])
def get_submissions():
    """Get all form submissions (for admin access)"""
    try:
        submissions = FormSubmission.query.order_by(FormSubmission.submitted_at.desc()).all()
        
        submissions_data = []
        for submission in submissions:
            submissions_data.append({
                'id': submission.id,
                'form_type': submission.form_type,
                'name': submission.name,
                'email': submission.email,
                'company': submission.company,
                'interest': submission.interest,
                'message': submission.message,
                'phone': submission.phone,
                'submitted_at': submission.submitted_at.isoformat(),
                'submission_data': json.loads(submission.submission_data) if submission.submission_data else {}
            })
        
        return jsonify({
            'success': True,
            'submissions': submissions_data,
            'total': len(submissions_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving submissions: {str(e)}'
        }), 500

@forms_bp.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    """Get a specific form submission"""
    try:
        submission = FormSubmission.query.get_or_404(submission_id)
        
        return jsonify({
            'success': True,
            'submission': {
                'id': submission.id,
                'form_type': submission.form_type,
                'name': submission.name,
                'email': submission.email,
                'company': submission.company,
                'interest': submission.interest,
                'message': submission.message,
                'phone': submission.phone,
                'submitted_at': submission.submitted_at.isoformat(),
                'submission_data': json.loads(submission.submission_data) if submission.submission_data else {}
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving submission: {str(e)}'
        }), 500

