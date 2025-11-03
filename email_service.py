import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
