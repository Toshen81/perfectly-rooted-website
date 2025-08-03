from flask import Blueprint, request, jsonify
from src.models.form_submission import FormSubmission, db
from datetime import datetime
import json

forms_bp = Blueprint('forms', __name__)

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
