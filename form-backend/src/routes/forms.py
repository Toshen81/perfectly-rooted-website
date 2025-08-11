from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

forms_bp = Blueprint('forms', __name__)

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    try:
        data = request.get_json()
        print(f"Consultation submission received: {data}")
        
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
    print("=== EBOOK FUNCTION STARTED ===")
    
    try:
        data = request.get_json()
        print(f"Ebook submission received: {data}")
        
        # SEND EMAIL IMMEDIATELY - FIRST THING WE DO
        print("=== STARTING EMAIL PROCESS ===")
        
        user_email = data.get('email')
        user_name = data.get('name', 'Friend')
        
        print(f"User email: {user_email}")
        print(f"User name: {user_name}")
        
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv('EMAIL_USERNAME', 'perfectlyrooted25@gmail.com')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        print(f"Sender email: {sender_email}")
        print(f"Password available: {bool(sender_password)}")
        
        if not sender_password:
            print("ERROR: EMAIL_PASSWORD environment variable not set")
        else:
            print("Password is available, proceeding with email...")
            
            try:
                # Create simple email
                subject = "📚 Your Free Business Guide: 'Rooted in Success'"
                
                body = f"""
                <html>
                <body>
                    <h2>📚 Thank You {user_name}!</h2>
                    <p>Thank you for downloading our free business guide!</p>
                    <p>This email confirms that our email system is working.</p>
                    <p>The PDF attachment will be added in the next version.</p>
                    <p>Best regards,<br>Toshen<br>Perfectly Rooted Solutions</p>
                </body>
                </html>
                """
                
                print("Creating email message...")
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = user_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                print("Email message created")
                
                print("Connecting to Gmail SMTP...")
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                print("SMTP connection established")
                
                print("Logging into Gmail...")
                server.login(sender_email, sender_password)
                print("Gmail login successful")
                
                print("Sending email...")
                text = msg.as_string()
                server.sendmail(sender_email, user_email, text)
                server.quit()
                
                print(f"SUCCESS: Email sent to {user_email}")
                
            except Exception as email_error:
                print(f"EMAIL ERROR: {str(email_error)}")
        
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

