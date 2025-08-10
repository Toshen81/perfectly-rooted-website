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

forms_bp = Blueprint('forms', __name__)

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

