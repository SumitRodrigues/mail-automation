import smtplib

email = input("Senders email: ")
receiver_email = input("Receivers email: ")

subject = input("Subject: ")
message = input("Message: ")

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, "uttzjjkdjrhmqlql")
server.sendmail(email, receiver_email, text)
print("Email has been sent successfully to " + receiver_email)