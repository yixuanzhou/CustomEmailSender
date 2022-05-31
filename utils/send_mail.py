# !/usr/bin/env python
# @Date    : 2022-05-05
# @Author  : Yixuan Zhou (ethanzhou@alumni.usc.edu)
import base64
import os
import sendgrid
from sendgrid.helpers.mail import *
from faker import Faker

faker = Faker()
sg = sendgrid.SendGridAPIClient(api_key=os.environ['API_KEY'])
ATTACHMENT_FOLDER = "static/uploads/"


def send_mail(mail_from, mail_to, mail_subject, mail_content, sender_name, mail_attachment=None, mail_headers=None,
              mail_cc=None, mail_bcc=None) -> bool:
    """Using SendGrid's Python Library: https://github.com/sendgrid/sendgrid-python

    Args:
        mail_from (str): Email From Address -> sender
        mail_to (str): List of Email To Address -> recipients (comma separated)
        mail_subject (str): Email Subject
        mail_content (str): Email Body in Text/Html
        sender_name (str): Sender Name
        mail_attachment (str): Mail Attachment Filepath (default None)
        mail_headers (list): List of Email Headers (default None)
        mail_cc (str): List of Email CC Address (comma separated, default None)
        mail_bcc (str): List of Email BCC Address (comma separated, default None)

    Returns:
        bool: success/failure of email sending
    """
    for name, value in vars().items():
        print(name, value)

    message = Mail()
    message.from_email = From(mail_from, sender_name)
    to_emails = [to.strip() for to in mail_to.split(',')]
    for idx, to_email in enumerate(to_emails):
        to_emails[idx] = To(to_email)
    message.to = to_emails
    message.subject = Subject(mail_subject)
    message.content = Content("text/html", "<pre>" + mail_content + "</pre>")
    headers, cc_mails, bcc_mails = [], [], []

    if mail_attachment:
        filename, filetype = mail_attachment[0], mail_attachment[1]
        with open(ATTACHMENT_FOLDER + filename, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()
        attached_file = Attachment(
            FileContent(encoded_file),
            FileName(filename),
            FileType(filetype),
            Disposition('attachment')
        )
        message.attachment = attached_file

    if mail_headers != [[''], ['']]:
        for hdr, val in zip(mail_headers[0], mail_headers[1]):
            headers.append(Header(hdr, val))
        message.header = headers

    if mail_cc:
        cc_addrs = [cc.strip() for cc in mail_cc.split(',')]
        for cc_addr in cc_addrs:
            cc_mails.append(Cc(cc_addr))
        message.cc = cc_mails

    if mail_bcc:
        bcc_addrs = [bcc.strip() for bcc in mail_bcc.split(',')]
        for bcc_addr in bcc_addrs:
            bcc_mails.append(Bcc(bcc_addr))
        message.bcc = bcc_mails

    try:
        response = sg.client.mail.send.post(request_body=message.get())
        if response.status_code in range(200, 300):
            return True
    except Exception as err:
        print(err)
    return False
