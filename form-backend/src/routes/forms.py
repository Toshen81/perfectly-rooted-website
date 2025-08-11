from flask import Blueprint, request, jsonify

forms_bp = Blueprint('forms', __name__)

@forms_bp.route('/submit-consultation', methods=['POST'])
def submit_consultation():
    print("CONSULTATION FUNCTION CALLED")
    try:
        data = request.get_json()
        print(f"Consultation data: {data}")
        
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
    print("PACKAGE FUNCTION CALLED")
    try:
        data = request.get_json()
        print(f"Package data: {data}")
        
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
    print("EBOOK FUNCTION CALLED - FIRST LINE")
    
    try:
        print("EBOOK FUNCTION - INSIDE TRY BLOCK")
        
        data = request.get_json()
        print(f"EBOOK DATA RECEIVED: {data}")
        
        user_email = data.get('email')
        print(f"USER EMAIL: {user_email}")
        
        # Test if we can import email modules
        try:
            print("TESTING EMAIL IMPORTS...")
            import smtplib
            import os
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            print("EMAIL IMPORTS SUCCESSFUL")
            
            # Test environment variables
            sender_email = os.getenv('EMAIL_USERNAME', 'perfectlyrooted25@gmail.com')
            sender_password = os.getenv('EMAIL_PASSWORD')
            
            print(f"SENDER EMAIL: {sender_email}")
            print(f"PASSWORD EXISTS: {bool(sender_password)}")
            
            if sender_password:
                print("ATTEMPTING TO SEND EMAIL...")
                
                # Create simple message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = user_email
                msg['Subject'] = "Test Email from Perfectly Rooted"
                
                body = f"<html><body><h2>Test Email</h2><p>This is a test email to {user_email}</p></body></html>"
                msg.attach(MIMEText(body, 'html'))
                
                print("EMAIL MESSAGE CREATED")
                
                # Send email
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                print("SMTP CONNECTION ESTABLISHED")
                
                server.login(sender_email, sender_password)
                print("GMAIL LOGIN SUCCESSFUL")
                
                server.sendmail(sender_email, user_email, msg.as_string())
                server.quit()
                
                print("EMAIL SENT SUCCESSFULLY!")
                
            else:
                print("NO PASSWORD AVAILABLE")
                
        except Exception as email_error:
            print(f"EMAIL ERROR: {str(email_error)}")
        
        print("RETURNING SUCCESS RESPONSE")
        
        return jsonify({
            'success': True,
            'message': 'Ebook request processed successfully'
        }), 200
        
    except Exception as e:
        print(f"MAJOR ERROR in submit_ebook: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request'
        }), 500

@forms_bp.route('/submissions', methods=['GET'])
def get_submissions():
    print("SUBMISSIONS FUNCTION CALLED")
    return jsonify({
        'success': True,
        'submissions': [],
        'total': 0
    }), 200

@forms_bp.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    print(f"GET SUBMISSION FUNCTION CALLED: {submission_id}")
    return jsonify({
        'success': True,
        'submission': {}
    }), 200

