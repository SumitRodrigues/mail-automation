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
CSV_FILE = "/Users/sumitrodrigues/Documents/mail-automation/nike-recipients.csv"
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
SUBJECT = "Interest in Software Engineer (Fullstack) Role at RudderStack"
MESSAGE = """\
Hi [Recipient Name],

I hope this email finds you well! I’m a Software Engineer Student Assistant at California State University, Fullerton, studying Computer Science, and currently preparing to recruit for full-time software engineering positions. I’m passionate about building scalable distributed systems and leveraging real-time data pipelines to drive efficient decision-making.

Here’s a little more about me:

- Work Experience: I’ve worked on full-stack applications using Node.js, TypeScript, React.js, and PostgreSQL, developing optimized microservices and implementing event-driven architectures with Kafka. Previously, I worked at BNP Paribas, where I helped design high-performance distributed systems for fintech applications.
- On-Campus Involvement: At CSUF, I have contributed to modernizing CI/CD workflows, migrating legacy infrastructure to AWS, and improving developer productivity by automating deployment pipelines.
- Personal Interests: Outside of coding, I enjoy hiking, experimenting with home automation projects, and staying up to date on the latest cloud computing advancements.

I’m preparing to apply for the Software Engineer (Fullstack) role at RudderStack this spring and would appreciate the opportunity to ask you a few specific questions about the role and your experience. Would you be available for a quick 15-minute chat at [Insert Specific Time]?

Thanks so much in advance for your time!

Best regards,  
Sumit Rodrigues  
Los Angeles, CA  
Phone: +1562-549-9508  
Email: sumitrod11@gmail.com  
"""

# ✅ Resume file path validation
RESUME_FILENAME = "/Users/sumitrodrigues/Documents/mail-automation/Sumit_Rodrigues_Resume - Nike SDE 1.pdf"
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
