import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'ivanlai2005@gmail.com'
email_password = 'eiqa dwdt ojlf rthf'
email_receiver = 'p23015609@student.newinti.edu.my'

# Set the subject and body of the email
subject = 'Registration Completed!'
body = """
Someone has registered this email account in the Car2U application. If this is not you, please contact Car2U as soon as possible. 
Please ignore this message if this was you.


Car2U contact: 016-407 5284
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())