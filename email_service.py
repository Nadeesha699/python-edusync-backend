import datetime
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, jsonify, request

email_bp = Blueprint('email_bp',__name__)

def send_otp(sender_email, receiver_email, subject, body, app_password,otp):
    # Set up the MIME message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message['Reply-To'] = sender_email

    # Attach the email body
    message.attach(MIMEText(body, 'plain')) 

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server
        server.starttls()  # Secure the connection

        # Log in to the server using the app password
        server.login(sender_email, app_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()  # Close the server connection
        return otp

    except Exception as e:
        return f"Failed to send email: {str(e)}"

@email_bp.route('/send_otp', methods=['POST'])
def send_otp_route():
    otp = random.randint(100000, 999999)
    
   #  Get JSON data from request
    data = request.get_json()

    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = data.get('receiver_email')
    subject = 'EduSync ICT Teacher Password Change Verification'
    body = f"""
Dear ICT Teacher,

We received a request to change your EduSync account password.

To verify this action, please use the One-Time Password (OTP) provided below:

🔐 Your OTP Code: {otp}

This code will expire in 5 minutes.

If you did not request this change, please ignore this email or contact EduSync Support immediately.

Best regards,  
EduSync ICT Support Team

"""
    app_password = os.getenv('GMAIL_APP_PASSWORD') # App password for Gmail

   #  Call the send_email function
   #  otp = send_otp(sender_email, receiver_email, subject, body, app_password,otp)
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)

    return jsonify({"message": "OTP sent successfully"})   