# send_mail_service.py (Flask example)
from flask import Flask, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
SG_API_KEY = os.environ['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']

@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.json
    to_email = data.get('to')
    subject  = data.get('subject')
    body     = data.get('body')
    message = Mail(from_email='illworkafterthis@gmail.com',
                   to_emails=to_email,
                   subject=subject,
                   html_content=body)
    try:
        sg = SendGridAPIClient(SG_API_KEY)
        sg.send(message)
        return jsonify(status='ok')
    except Exception as e:
        return jsonify(status='error', detail=str(e)), 500

if __name__ == '__main__':
    app.run()
