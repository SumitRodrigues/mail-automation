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
CSV_FILE = "/Users/sumitrodrigues/Documents/mail-automation/applovin-recipients.csv"
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
SUBJECT = "Enthusiastic Applicant for Software Engineering Intern Role – Summer 2025"
MESSAGE = """\
Hi [Recipient Name],

I hope you're doing well! I recently applied for the Software Engineering Intern position at AppLovin and am excited about the opportunity to contribute to your team.

A bit about me:

- Backend Development: Experience with Java and Spring Boot, developing scalable microservices and data pipelines.
- High-Performance Systems: Built and optimized ETL pipelines using Apache Spark, Kubernetes, and Cassandra, reducing data processing time by 50%.
- Cloud & DevOps: Worked with AWS (EC2, Lambda, S3), Docker, and Kubernetes to improve system efficiency.
- Data Structures & Algorithms: Strong foundation in sorting algorithms, multithreading, and parallel processing, improving backend request handling by 40%.
- Testing & Security: Implemented Spring Security with OAuth2 and conducted unit testing with JUnit & Postman, ensuring secure and stable deployments.

I’m currently pursuing my Master’s in Computer Science at California State University, Fullerton, and will graduate in December 2025. I would love the opportunity to discuss how my skills align with AppLovin’s engineering team and how I can contribute to building high-performance, scalable applications.

If you're the right contact, I’d appreciate the chance to connect. Otherwise, I’d be grateful if you could point me in the direction of the hiring manager.

Looking forward to hearing from you!

Best regards,  
Sumit Rodrigues  
Los Angeles, CA  
Phone: +1562-549-9508  
Email: sumitrod11@gmail.com  
"""

# ✅ Resume file path validation
RESUME_FILENAME = "/Users/sumitrodrigues/Documents/mail-automation/Sumit_Rodrigues_Resume - Applovin Intern.pdf"
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
