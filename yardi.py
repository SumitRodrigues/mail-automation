import smtplib
import os
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ✅ Fix environment variable usage
EMAIL_USER = os.getenv("EMAIL_USER")  # Your email
EMAIL_PASS = os.getenv("EMAIL_PASS")  # Your App Password

# ✅ SMTP settings for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ✅ Ensure CSV file exists before reading
CSV_FILE = "/Users/sumitrodrigues/Documents/mail-automation/yardi-recipients.csv"
if not os.path.exists(CSV_FILE):
    print(f"Error: '{CSV_FILE}' file not found.")
    exit()

# ✅ Read CSV safely (strip spaces, ensure string type)
df = pd.read_csv(CSV_FILE, dtype=str)
df.columns = df.columns.str.strip()  # Remove accidental spaces in column names

# ✅ Check if Email column exists
if "Email" not in df.columns:
    print("Error: 'Email' column not found in CSV. Ensure the header is correct.")
    exit()

# ✅ Hardcoded email subject and message
SUBJECT = "Excited to Apply for Software Development Engineer I – Yardi (RES24423720)"
MESSAGE = """\
Hi [Recipient Name],

I hope you're doing well! My name is Sumit Rodrigues, and I’m currently pursuing my Master’s in Computer Science at California State University, Fullerton. I recently applied for the Software Development Engineer I position at Yardi in Santa Barbara, CA, and wanted to follow up to express my strong interest in the role and see if you might be able to help ensure my application reaches the appropriate team.

A bit about me:

I bring over 2 years of experience in full-stack development with a strong foundation in Java, Spring Boot, Angular, and MySQL. At CSUF, I currently serve as a Web Developer Student Assistant, where I’ve led the integration of ChatGPT-4o for student support, developed responsive Angular components from Figma designs, and enhanced real-time data handling with robust API integrations. Previously, at BNP Paribas, I worked on fintech microservices, optimized real-time dashboards using Angular and D3.js, and automated CI/CD pipelines using Jenkins, Docker, and Kubernetes.

I’d be grateful for the opportunity to connect and discuss how I could contribute to Yardi’s innovative development efforts. If possible, could you kindly review my profile or help direct my application to the right team?

Looking forward to hearing from you!

Job Link: https://careers.yardi.com/openings/job-posting/RES24423720/

Best regards,  
Sumit Rodrigues  
Los Angeles, CA  
Phone: +1562-549-9508  
Email: sumitrod11@gmail.com  
"""

# ✅ Resume file path validation
RESUME_FILENAME = "/Users/sumitrodrigues/Documents/mail-automation/Sumit_Rodrigues_Resume - Yardi SDE.pdf"
if not os.path.exists(RESUME_FILENAME):
    print(f"Error: Resume file '{RESUME_FILENAME}' not found. Exiting.")
    exit()

# ✅ Function to send email


def send_email(receiver_email, receiver_name):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = receiver_email
        msg["Subject"] = SUBJECT

        # ✅ Personalized email body
        body = MESSAGE.replace("[Recipient Name]", receiver_name)
        msg.attach(MIMEText(body, "plain"))

        # ✅ Attach resume safely
        with open(RESUME_FILENAME, "rb") as resume_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(resume_file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename={os.path.basename(RESUME_FILENAME)}")
            msg.attach(part)

        # ✅ Ensure email credentials are loaded correctly
        if not EMAIL_USER or not EMAIL_PASS:
            print("Error: Email credentials not set. Check environment variables.")
            return

        # ✅ Connect to SMTP and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, receiver_email, msg.as_string())

        print(f"✅ Email sent successfully to {receiver_email}")

    except Exception as e:
        print(f"❌ Failed to send email to {receiver_email}: {e}")


# ✅ Send emails to all recipients
for index, row in df.iterrows():
    receiver_email = row["Email"].strip()  # Remove spaces if any
    receiver_name = row.get("Name", "there")
    if pd.isna(receiver_name):  # If NaN, replace it with "there"
        receiver_name = "there"
    # Convert to string, avoid NaN issues
    receiver_name = str(receiver_name).strip()
    print(f"📧 Sending email to: {receiver_email}")  # Debugging print
    send_email(receiver_email, receiver_name)
    time.sleep(5)  # Delay to prevent spam detection

print("✅ All emails sent successfully!")
