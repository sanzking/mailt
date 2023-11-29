from flask import render_template, redirect, url_for, request, session, Flask
import imaplib
import email
from email.header import decode_header

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_email', methods=['POST'])
def check_email():
    email_address = request.form.get('email_address')
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login('kapofaqih730@gmail.com', 'tevrruxmpobgmbit')
    mail.select("inbox")
    status, messages = mail.search(None, f'TO "{email_address}"')
    email_ids = messages[0].split()
    emails = []
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(msg["Subject"])[0]
        subject = subject.decode(encoding) if isinstance(subject, bytes) else subject
        from_, encoding = decode_header(msg.get("From", ""))[0]
        from_ = from_.decode(encoding) if isinstance(from_, bytes) else from_
        if msg.is_multipart():
            body = ""
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
        emails.append({'subject': subject, 'from': from_, 'body': body})
    mail.logout()
    return render_template('result.html', emails=emails, emil=email_address)

if __name__ == '__main__':
    app.run(debug=True)
