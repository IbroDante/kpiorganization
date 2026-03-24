from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # For flash messages in contact form

# Email configuration (optional - for production)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'info@kpiorganization.ng',  # Update with your email
    'sender_password': '',  # Update with your password
    'recipient_email': 'info@kpiorganization.ng'
}

def send_email(name, email, phone, program, message):
    """Send email notification for training inquiries"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        msg['Subject'] = f"Training Inquiry: {program} - {name}"
        
        body = f"""
        New Training Inquiry:
        
        Name: {name}
        Email: {email}
        Phone: {phone}
        Program: {program}
        Message: {message}
        
        Please respond within 24 hours.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Simple form handling
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        service = request.form.get('service', 'General Inquiry')
        
        # Flash success message
        flash('Thank you for your message! We will get back to you soon.', 'success')
        
        # Optional: Send email notification
        # send_email(name, email, '', service, message)
        
        return redirect(url_for('home') + '#contact')
    
    return render_template('index.html')

@app.route('/trainings.html', methods=['GET', 'POST'])
def trainings():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        program = request.form.get('program', 'Not specified')
        message = request.form.get('message', '')
        
        # Flash success message
        flash('Thank you for your training inquiry! Our SEC training consultant will contact you within 24 hours.', 'success')
        
        # Optional: Send email notification
        # send_email(name, email, phone, program, message)
        
        return redirect(url_for('trainings') + '#contact')
    
    return render_template('trainings.html')

@app.route('/trainings/<program_type>')
def training_category(program_type):
    """Optional: Route for filtering training programs by category"""
    return render_template('trainings.html', active_category=program_type)

if __name__ == '__main__':
    app.run(debug=True)