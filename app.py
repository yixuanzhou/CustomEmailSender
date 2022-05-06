from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils.send_mail import *
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = ('txt', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png')
DEBUG = True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit():
    print("Request Form Data:", request.form)
    From = request.form.get('sender-addr')
    As = request.form.get('sender-name')
    To = request.form.get('receiver-addr')
    Subject = request.form.get('email-subject')
    Body = request.form.get('email-body')
    Attachments = ""
    Headers = [request.form.getlist('header-name'), request.form.getlist('header-value')]
    Cc = request.form.get('email-cc')
    Bcc = request.form.get('email-bcc')
    print(Headers)
    if 'email-attachment' in request.files:
        if request.files.get('email-attachment').filename:
            file = request.files['email-attachment']
            Attachments = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], Attachments))
    send_mail(From, To, Subject, Body, As, Attachments, Headers, Cc, Bcc)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
