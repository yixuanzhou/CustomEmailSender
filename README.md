# Tortoise <img src="https://cdn-icons-png.flaticon.com/512/882/882869.png" width="35">

> Custom Email Sender Web App
> 
Flask App to send custom email messages using SendGrid.

<img src="https://github.com/yixuanzhou/Tortoise/blob/main/static/uploads/Tortoise.gif" alt="demo" width="400"/>

## Getting Started
### Prerequisites
- Python

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
- Add CC/BCC
- Plain/HTML mail body
- Mail attachments
- Configure your own mail sending server - Modify utils/send_mail.py
- Bulk emails sending - Available for Google Sheets