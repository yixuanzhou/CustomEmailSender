from flask import Flask, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
from utils.send_mail import *
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = ('txt', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit():
    print("Request Data:", request.form)
    print("Request List:", request.form.getlist('header-name'), request.form.getlist('header-value'))
    print("Request File:", request.files)
    if request.form.get('clear') == "Clear All":
        return redirect("/")
    From = request.form.get('sender-addr')
    As = request.form.get('sender-name')
    To = request.form.get('receiver-addr')
    Subject = request.form.get('email-subject')
    Body = request.form.get('email-body')
    Timestamp = request.form.get('email-timestamp')
    Timestamp = " " + (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M") if Timestamp == "on" else ""
    Attachments = ""
    Headers = [request.form.getlist('header-name'), request.form.getlist('header-value')]
    Cc = request.form.get('email-cc')
    Bcc = request.form.get('email-bcc')
    if 'email-attachment' in request.files:
        if request.files.get('email-attachment').filename:
            file = request.files['email-attachment']
            Attachments = (secure_filename(file.filename), file.content_type)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], Attachments[0]))

    # res = send_mail(From, To, Subject + Timestamp, Body, As, Attachments, Headers, Cc, Bcc)
    # flash('Sent Message successfully!', 'success') if res else flash('Sorry, something went wrong', 'danger')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
