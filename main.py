import smtplib
import os
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Hardcoded sender email credentials (use environment variables for security)
EMAIL_USER = os.getenv("sumitrod11@gmail.com")  # Your email
EMAIL_PASS = os.getenv("uttzjjkdjrhmqlql")  # Your app password

# SMTP settings (for Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Load recipient emails from CSV
df = pd.read_csv("recipients.csv")  # Ensure the file contains 'Email' column

# Hardcoded email subject and message
SUBJECT = "Interest in Software Engineer III Role at Walmart (R-2108907)"
MESSAGE = """\
Hi [Recipient Name],

I hope you're doing well! I recently applied for the Software Engineer III position at Walmart Global Tech and wanted to express my enthusiasm for this opportunity. With a strong background in Java, Spring Boot, microservices, and cloud computing (AWS, Azure, GCP), I am excited about the chance to contribute to Walmart’s Omni Merchant Tools team.

Here’s a bit about my experience:

Backend Development: Built and optimized microservices with Java, Spring Boot, and Hibernate, reducing API latency by 25%.
Cloud & Scalability: Developed and deployed large-scale applications using AWS Lambda, S3, and Kubernetes, improving system efficiency.
Service-Oriented Architecture (SOA): Designed and integrated RESTful and GraphQL APIs, reducing redundant data calls by 85%.
Frontend Expertise: Built React + Node.js applications with state management (Redux) and optimized UI performance for millions of users.
CI/CD & DevOps: Automated deployments with Jenkins, Docker, and Kubernetes, cutting deployment time from 4 hours to 20 minutes.
I’m particularly excited about this role’s focus on high-performance systems, real-time data processing, and cloud-native solutions. I would love the opportunity to discuss how my skills align with Walmart’s engineering needs. Would you be available for a quick chat this week?

Looking forward to hearing from you!  
"""

# Resume attachment
RESUME_FILENAME = "resume.pdf"  # Ensure this file is in the same directory

# Function to send email with attachment
def send_email(receiver_email, receiver_name):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = receiver_email
        msg["Subject"] = SUBJECT

        # Personalize email body
        body = MESSAGE.replace("[Recipient Name]", receiver_name)
        msg.attach(MIMEText(body, "plain"))

        # Attach resume file
        with open(RESUME_FILENAME, "rb") as resume_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(resume_file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={RESUME_FILENAME}")
            msg.attach(part)

        # Connect to SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, receiver_email, msg.as_string())
        server.quit()

        print(f"Email sent successfully to {receiver_email}")

    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {e}")

# Send emails to all recipients
for index, row in df.iterrows():
    send_email(row["Email"], row.get("Name", "there"))  # Default to "there" if no name is provided
    time.sleep(5)  # Delay to prevent spam detection

print("All emails sent successfully!")
