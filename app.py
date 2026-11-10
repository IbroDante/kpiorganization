from flask import Flask, request, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from html import escape
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Brevo API Configuration
BREVO_CONFIG = {
    'api_key': os.getenv('BREVO_API_KEY', ''),
    'sender_email': os.getenv('BREVO_SENDER_EMAIL', '929aca001@smtp-brevo.com'),
    'sender_name': 'KPI Organization Nigeria Ltd',
    'recipient_email': os.getenv('BREVO_RECIPIENT_EMAIL', 'info@kpiorganization.ng'),
    'api_url': 'https://api.brevo.com/v3/smtp/email'
}

def send_brevo_email(name, email, phone, program, message, form_type='training'):
    """Send email using Brevo API"""
    if not BREVO_CONFIG['api_key']:
        print("⚠️ Brevo API key not configured. Email not sent.")
        return False

    try:
        # Escape user-provided values before embedding them in HTML email.
        name, email, phone, program, message = (escape(str(value), quote=True) for value in (name, email, phone, program, message))
        # Determine subject and template based on form type
        if form_type == 'training':
            subject = f"New Training Inquiry: {program} - {name}"
            email_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #0a1c2f, #0a2a3a); padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .header h2 {{ color: #ffd966; margin: 0; }}
                    .content {{ background: #fff; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .field {{ margin-bottom: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px; }}
                    .field-label {{ font-weight: bold; color: #0a1c2f; }}
                    .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
                    .badge {{ display: inline-block; background: #ffd966; color: #0a1c2f; padding: 5px 10px; border-radius: 5px; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>📋 New Training Inquiry</h2>
                        <p>Received: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    <div class="content">
                        <div class="field">
                            <div class="field-label">👤 Full Name:</div>
                            <div>{name}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">📧 Email Address:</div>
                            <div><a href="mailto:{email}">{email}</a></div>
                        </div>
                        <div class="field">
                            <div class="field-label">📞 Phone Number:</div>
                            <div>{phone if phone else 'Not provided'}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">🎯 Program of Interest:</div>
                            <div><span class="badge">{program}</span></div>
                        </div>
                        <div class="field">
                            <div class="field-label">💬 Message:</div>
                            <div style="white-space: pre-wrap;">{message if message else 'No message provided'}</div>
                        </div>
                    </div>
                    <div class="footer">
                        <p>This inquiry was submitted from the KPI Organization website.<br>
                        Please respond within 24 hours.</p>
                        <p>🔗 <a href="https://kpiorganization.ng/trainings">View All Training Programs</a></p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            subject = f"New Contact Form Inquiry: {name}"
            email_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #0a1c2f, #0a2a3a); padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .header h2 {{ color: #ffd966; margin: 0; }}
                    .content {{ background: #fff; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .field {{ margin-bottom: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px; }}
                    .field-label {{ font-weight: bold; color: #0a1c2f; }}
                    .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>📧 New Contact Form Submission</h2>
                        <p>Received: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    <div class="content">
                        <div class="field">
                            <div class="field-label">👤 Name:</div>
                            <div>{name}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">📧 Email:</div>
                            <div><a href="mailto:{email}">{email}</a></div>
                        </div>
                        <div class="field">
                            <div class="field-label">🎯 Service Interest:</div>
                            <div>{program}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">💬 Message:</div>
                            <div style="white-space: pre-wrap;">{message}</div>
                        </div>
                    </div>
                    <div class="footer">
                        <p>This message was submitted from the KPI Organization contact form.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        # Prepare the email payload for Brevo
        payload = {
            "sender": {
                "name": BREVO_CONFIG['sender_name'],
                "email": BREVO_CONFIG['sender_email']
            },
            "to": [
                {
                    "email": BREVO_CONFIG['recipient_email'],
                    "name": "KPI Organization Team"
                }
            ],
            "subject": subject,
            "htmlContent": email_body,
            "headers": {
                "X-Mailin-custom": "training_inquiry",
                "X-Entity-Ref-ID": datetime.now().strftime('%Y%m%d%H%M%S')
            }
        }
        
        # Optional: Add CC or BCC if needed
        # payload["cc"] = [{"email": "backup@kpiorganization.ng", "name": "Backup"}]
        
        # Make the API request to Brevo
        headers = {
            'accept': 'application/json',
            'api-key': BREVO_CONFIG['api_key'],
            'content-type': 'application/json'
        }
        
        response = requests.post(
            BREVO_CONFIG['api_url'],
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
        
        if response.status_code == 201:
            print(f"✓ Email sent successfully via Brevo to {BREVO_CONFIG['recipient_email']}")
            return True
        else:
            print(f"✗ Brevo API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {e}")
        return False
    except Exception as e:
        print(f"✗ Email error: {e}")
        return False

@app.post('/api/training-inquiry')
def training_inquiry():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    program = str(data.get('program', '')).strip()
    if not name or not email or not program:
        return jsonify(message='Please provide your name, email and program interest.'), 400
    sent = send_brevo_email(name, email, str(data.get('phone', '')), program, str(data.get('message', '')), form_type='training')
    if sent:
        return jsonify(message='Thank you for your training inquiry! Our training consultant will contact you within 24 hours.')
    return jsonify(message='We could not send your enquiry. Please try again or email info@kpiorganization.ng.'), 503

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_app(path):
    # Serve built React assets and allow direct navigation to React routes.
    dist = os.path.join(app.root_path, 'dist')
    if path and os.path.isfile(os.path.join(dist, path)):
        return send_from_directory(dist, path)
    return send_from_directory(dist, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
