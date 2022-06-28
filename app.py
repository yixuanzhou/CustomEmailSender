# !/usr/bin/env python
# @Date    : 2022-05-05
# @Author  : Yixuan Zhou (ethanzhou@alumni.usc.edu)
import os
import datetime
from flask import Flask, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
from utils.send_mail import send_mail
from utils.google_sheet_client import GoogleSheetClient

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = ('txt', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'eml')
gsc = GoogleSheetClient()
sheet_list = gsc.get_sheet_list()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    return render_template('index.html', sheets=sheet_list)


@app.route('/', methods=['POST'])
def submit():
    print("Request Data:", request.form)
    print("Request List:", request.form.getlist('header-name'), request.form.getlist('header-value'))
    print("Request File:", request.files)
    if request.form.get('clear') == "Clear All":
        return redirect("/")
    from_email = request.form.get('sender-addr')
    as_name = request.form.get('sender-name')
    to_email = request.form.get('receiver-addr')
    subject = request.form.get('email-subject')
    content = request.form.get('email-body')
    timestamp = request.form.get('email-timestamp')
    timestamp = " " + (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M") if timestamp == "on" else ""
    attachments = []
    headers = [request.form.getlist('header-name'), request.form.getlist('header-value')]
    cc = request.form.get('email-cc')
    bcc = request.form.get('email-bcc')
    files = request.files.getlist('email-attachment')
    for file in files:
        if file.filename == '':
            continue
        attachments.append((secure_filename(file.filename), file.content_type))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    if request.form.get('test-type') == 'predefined':
        mail_bodies = gsc.read_sheet(request.form['sheet-name'])
        for idx, mail_body in enumerate(mail_bodies):
            res = send_mail(from_email, to_email, subject + " " + str(idx) + timestamp, mail_body[0], as_name,
                            attachments, headers, cc, bcc)
            if not res:
                flash('Sorry, something went wrong', 'danger')
                break
        flash('Sent Message successfully!', 'success')
    else:
        res = send_mail(from_email, to_email, subject + timestamp, content, as_name, attachments, headers, cc, bcc)
        flash('Sent Message successfully!', 'success') if res else flash('Sorry, something went wrong', 'danger')

    return render_template('index.html', sheets=sheet_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
