import imaplib
import email
from email.header import decode_header

def search_emails(username, password, subject_match):
    # Connect to the Outlook IMAP server
    mail = imaplib.IMAP4_SSL('outlook.office365.com')

    # Login to the server
    mail.login(username, password)

    # Select the inbox
    mail.select('inbox')

    # Search for emails with a matching subject
    status, messages = mail.search(None, f'SUBJECT "{subject_match}"')

    # Convert the result to a list of email IDs
    messages = messages[0].split()

    # List to store the matching emails
    matching_emails = []

    for mail_id in messages:
        # Fetch the email by its ID (RFC822 protocol for full email)
        status, data = mail.fetch(mail_id, '(RFC822)')

        # Raw email part
        raw_email = data[0][1]

        # Converts byte literal to string removing b''
        raw_email_string = raw_email.decode('utf-8')

        # Parses the email into an email message object
        email_message = email.message_from_string(raw_email_string)

        # Decode the email subject
        subject, encoding = decode_header(email_message['Subject'])[0]
        if isinstance(subject, bytes):
            # if it's a bytes type, decode to str
            subject = subject.decode(encoding or 'utf-8')

        # Decode the email body
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')

        # Add the matching email to the list
        matching_emails.append({'Subject': subject, 'Body': body})

    # Close the mailbox
    mail.close()

    # Return the matching emails
    return matching_emails