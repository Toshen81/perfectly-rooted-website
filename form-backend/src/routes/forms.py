from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from src.models.form_submission import FormSubmission, db
from datetime import datetime
import json

forms_bp = Blueprint('forms', __name__)

def send_notification_email(submission_data, form_type):
    """Send email notification for new form submission"""
    try:
        from src.main import mail
        
        # Create email subject based on form type
        if form_type == 'consultation':
            subject = f"🗓️ New Consultation Request from {submission_data.get('name', 'Unknown')}"
        elif form_type == 'package':
            subject = f"📦 New Package Inquiry: {submission_data.get('package', 'Unknown Package')}"
        elif form_type == 'contact':
            subject = f"📧 New Contact Form Submission from {submission_data.get('name', 'Unknown')}"
        else:
            subject = f"📝 New Form Submission ({form_type})"
        
        # Create email body
        body = f"""
New form submission received on Perfectly Rooted Solutions website!

Form Type: {form_type.title()}
Submission Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Contact Information:
• Name: {submission_data.get('name', 'Not provided')}
• Email: {submission_data.get('email', 'Not provided')}
• Phone: {submission_data.get('phone', 'Not provided')}
• Business: {submission_data.get('business', 'Not provided')}

"""
        
        if form_type == 'package':
            body += f"• Package Interest: {submission_data.get('package', 'Not specified')}\n"
        
        if submission_data.get('message'):
            body += f"\nMessage:\n{submission_data.get('message')}\n"
        
        body += f"""
---
You can view all submissions at: https://perfectly-rooted-forms-backend.onrender.com/api/submissions

Best regards,
Perfectly Rooted Solutions Form System
"""
        
        # Send email
        notification_email = current_app.config.get('NOTIFICATION_EMAIL', 'info@perfectly-rooted.com')
        
        msg = Message(
            subject=subject,
            recipients=[notification_email],
            body=body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")
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
        
        # Send email notification
        send_notification_email(data, 'consultation')
        
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
        
        # Send email notification
        send_notification_email(data, 'package')
        
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

@forms_bp.route('/submit-contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Create new form submission
        submission = FormSubmission(
            form_type='contact',
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
        
        # Send email notification
        send_notification_email(data, 'contact')
        
        return jsonify({
            'success': True,
            'message': 'Contact form submitted successfully!',
            'submission_id': submission.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting form: {str(e)}'
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

