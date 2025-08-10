from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

forms_bp = Blueprint('forms', __name__)

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    try:
        data = request.get_json()
        print(f"Consultation submission received: {data}")
        
        # Just return success for now - we'll add database later
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
        
        # Just return success for now - we'll add database later
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
        
        # Just return success for now - we'll add email later
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
        # Return empty list for now
        return jsonify({
            'success': True,
            'submissions': [],
            'total': 0
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
        # Return empty for now
        return jsonify({
            'success': True,
            'submission': {}
        }), 200
        
    except Exception as e:
        print(f"Error in get_submission: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while retrieving the submission'
        }), 500

