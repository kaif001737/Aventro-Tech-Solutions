from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
ADMIN_EMAIL = "aventrotechsolutions@gmail.com"
ADMIN_PASSWORD = "xdqs ztmo xxto wdgs"

def send_email(to_email, subject, body, is_admin_notification=False):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        text = msg.as_string()
        server.sendmail(ADMIN_EMAIL, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        inquiry_type = request.form.get("inquiry_type", "General Inquiry")
        service_program = request.form.get("service_program", "Not specified")
        
        # Email to admin
        admin_subject = f"New Contact Form Submission: {subject}"
        admin_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #6366f1;">New Contact Form Submission</h2>
            <div style="background: #f4f4f4; padding: 20px; border-radius: 5px;">
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Inquiry Type:</strong> {inquiry_type}</p>
                <p><strong>Service/Program:</strong> {service_program}</p>
                <p><strong>Message:</strong></p>
                <p style="background: white; padding: 15px; border-left: 4px solid #6366f1;">{message}</p>
            </div>
        </body>
        </html>
        """
        
        # Confirmation email to user
        user_subject = "Thank you for contacting Aventro Tech Solutions"
        user_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #6366f1;">Thank You, {name}!</h2>
                <p>Your response has been submitted successfully. We have received your inquiry regarding <strong>{service_program}</strong>.</p>
                <p>Our team will review your message and get back to you soon.</p>
                <div style="background: #f4f4f4; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Your Inquiry Details:</strong></p>
                    <p><strong>Subject:</strong> {subject}</p>
                    <p><strong>Inquiry Type:</strong> {inquiry_type}</p>
                </div>
                <p>Best regards,<br><strong>Aventro Tech Solutions Team</strong></p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    This is an automated confirmation email. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Send emails
        admin_sent = send_email(ADMIN_EMAIL, admin_subject, admin_body, is_admin_notification=True)
        user_sent = send_email(email, user_subject, user_body)
        
        if admin_sent and user_sent:
            return jsonify({"success": True, "message": "Message sent successfully! Check your email for confirmation."})
        else:
            return jsonify({"success": False, "message": "There was an error sending your message. Please try again."}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='192.168.29.207', port=5000, debug=True)
