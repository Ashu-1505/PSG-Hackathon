import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


otp = 696969
# Email details
sender_email = "harshadkrishnas@gmail.com"  # Replace with your email
receiver_email = "harshadkrishnas@gmail.com"  # Replace with recipient's email
password = "ygxb ehji ryje ppyn"  # Replace with your email account password

subject = "Safe Nest OTP"
body = f"Your OTP for LogIn is {otp}"


# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "plain"))


try:
    # Connect to Gmail's SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Upgrade the connection to secure
    server.login(sender_email, password)  # Login to the email account

    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()  # Close the connection
