import smtplib
import time
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load SMTP credentials from environment variables
EMAIL_USER = os.getenv("EMAIL_USER", "sumitrod11@gmail.com")  # Your email
EMAIL_PASS = os.getenv("EMAIL_PASS", "RodChangeIt@110300")  # Your email app password

# SMTP server settings (change based on your provider)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Load recipient details from CSV file
df = pd.read_csv("/Users/sumitrodrigues/Downloads/recipients.csv")  # Ensure CSV has 'Name' and 'Email' columns

# Email Subject and Body
SUBJECT = "Interest in Software Engineer III Role at Walmart (R-2108907)"
BODY_TEMPLATE = """\
Hi {name},

I hope you're doing well! I recently applied for the Software Engineer III position at Walmart Global Tech and wanted to express my enthusiasm for this opportunity. With a strong background in Java, Spring Boot, microservices, and cloud computing (AWS, Azure, GCP), I am excited about the chance to contribute to Walmart’s Omni Merchant Tools team.

Here’s a bit about my experience:

Backend Development: Built and optimized microservices with Java, Spring Boot, and Hibernate, reducing API latency by 25%.
Cloud & Scalability: Developed and deployed large-scale applications using AWS Lambda, S3, and Kubernetes, improving system efficiency.
Service-Oriented Architecture (SOA): Designed and integrated RESTful and GraphQL APIs, reducing redundant data calls by 85%.
Frontend Expertise: Built React + Node.js applications with state management (Redux) and optimized UI performance for millions of users.
CI/CD & DevOps: Automated deployments with Jenkins, Docker, and Kubernetes, cutting deployment time from 4 hours to 20 minutes.
I’m particularly excited about this role’s focus on high-performance systems, real-time data processing, and cloud-native solutions. I would love the opportunity to discuss how my skills align with Walmart’s engineering needs. Would you be available for a quick chat this week?

Looking forward to hearing from you!

Best regards,
Sumit Rodrigues
"""

# Function to send an email
def send_email(recipient_name, recipient_email):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = recipient_email
        msg["Subject"] = SUBJECT

        # Personalize email body
        body = BODY_TEMPLATE.format(name=recipient_name)
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, recipient_email, msg.as_string())
        server.quit()

        print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Send emails to all recipients
for index, row in df.iterrows():
    send_email(row["Name"], row["Email"])
    time.sleep(5)  # Add delay to prevent spam detection

print("All emails sent successfully!")
