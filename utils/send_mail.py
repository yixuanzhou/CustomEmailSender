# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import base64
import datetime
from sendgrid.helpers.mail import *
from faker import Faker

faker = Faker()
sg = sendgrid.SendGridAPIClient(api_key="")
ATTACHMENT_FOLDER = "static/uploads/"


def send_mail(mail_from, mail_to, mail_subject, mail_content, sender_name, mail_attachment=None, mail_headers=None, mail_cc=None, mail_bcc=None):
    message = Mail()
    message.from_email = From(mail_from, sender_name)
    to_emails = [to.strip() for to in mail_to.split(',')]
    for idx, to_email in enumerate(to_emails):
        to_emails[idx] = To(to_email)
    message.to = to_emails
    message.subject = Subject(mail_subject)
    message.content = Content("text/html", "<pre>" + mail_content + "</pre>")
    headers, ccs, bccs = [], [], []

    if mail_attachment:
        with open(ATTACHMENT_FOLDER + mail_attachment, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attached_file = Attachment(
            FileContent(encoded_file),
            FileName(mail_attachment),
            FileType('application/octet-stream'),
            Disposition('attachment')
        )
        message.attachment = attached_file

    if mail_headers != [[''], ['']]:
        for mail_header in mail_headers:
            headers.append(Header(mail_header[0], mail_header[1]))
        message.header = headers

    if mail_cc:
        for cc in mail_cc:
            ccs.append(Cc(cc[0], cc[1]))
        message.cc = ccs

    if mail_bcc:
        for bcc in mail_bcc:
            bccs.append(Bcc(bcc[0], bcc[1]))
        message.bcc = bccs

    response = sg.client.mail.send.post(request_body=message.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

if __name__ == "__main__":
    # send_mail(faker.email(), "admin@armorblox.dev", "hello world", faker.paragraph(), faker.name(), "", [("X-TEST", "OKOK"), ("X-TEST2", "HHH")])
    pass
