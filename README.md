# Tortoise <img src="https://cdn-icons-png.flaticon.com/512/882/882869.png" width="35">

> Custom Email Sender Web App
> 
Flask App to send custom email messages using SendGrid.

<img src="https://github.com/yixuanzhou/Tortoise/blob/main/static/uploads/Tortoise.png" alt="demo" />

## Getting Started
### Prerequisites
- Python
- [SendGrid](https://sendgrid.com/)

#### Install Requirements
```bash
pip install -r requirements.txt
```
#### Set SendGrid API key as environment variable
```bash
export API_KEY=<sendgrid_api_key>
```
#### Start Flask server
```bash
flask run
nohup flask run --host=0.0.0.0 > flask.log 2>&1 & # Or run in background
```

## Features
- Generate random fake sender - Using [Faker](https://github.com/joke2k/faker)
- Add custom email headers
- Add Cc/Bcc recipients
- Preview mail body in HTML
- Send one or multiple mail attachments
- Configurable mail server - utils/send_mail.py
- Bulk email sending - Read data from Google Sheets