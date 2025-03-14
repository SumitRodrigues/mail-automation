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
CSV_FILE = "/Users/sumitrodrigues/Documents/mail-automation/target-recipients.csv"
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
SUBJECT = "Application for Full Stack Engineer (UI-Focused) Role at Target (Job ID: R0000385926)"
MESSAGE = """\
Hi [Recipient Name],

I recently applied for the Full Stack Engineer (UI-Focused) role at Target and wanted to follow up to express my enthusiasm for this opportunity. With my strong expertise in React.js, TypeScript, Java, and scalable UI/UX development, I believe I can contribute meaningfully to Target’s Owned Brands Cost Management team in building robust, user-friendly solutions for cost visibility and vendor negotiations.

Job Link: https://corporate.target.com/jobs/w59/26/full-stack-engineer-ui-focused-owned-brands-costing-management

Why I’m a Strong Fit for This Role:

- Frontend Engineering & Scalable UI Development → Built responsive, high-performance SPAs using React.js, TypeScript, and SCSS, ensuring seamless cost tracking interfaces for finance dashboards.
- Full-Stack Development & API Integration → Designed RESTful APIs using Java & Spring Boot, integrating NoSQL (PostgreSQL, MongoDB) for real-time financial data processing—aligning with Target’s need for backend expertise.
- Cloud & Scalable Application Development → Deployed microservices-based applications on AWS & Google Cloud, optimizing cost analysis systems for enterprise-scale decision-making.
- Collaboration & Agile Development → Worked closely with UX designers, product managers, and backend teams, improving data visualization workflows and vendor cost negotiation tools.

I’m excited about the opportunity to bring my technical expertise, customer-focused mindset, and problem-solving approach to Target’s Costing Management team. I’d love the chance to discuss how my skills align with this role—please let me know if we can set up a time to connect.

Looking forward to hearing from you!

Best regards,  
Sumit Rodrigues  
Los Angeles, CA  
Phone: +1562-549-9508  
Email: sumitrod11@gmail.com  
"""

# ✅ Resume file path validation
RESUME_FILENAME = "/Users/sumitrodrigues/Documents/mail-automation/Sumit_Rodrigues_Resume - Target Frontend.pdf"
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
