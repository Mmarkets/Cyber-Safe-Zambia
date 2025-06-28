## Features
- Phishing Detector: Checks URLs using Google Safe Browsing API.
- Password Strength Checker: Evaluates passwords with zxcvbn, with live feedback.
- Secure Password Generator: Creates strong passwords using Python’s secrets module.
- Data Breach Checker: Verifies email breaches with Have I Been Pwned API, with email alerts.
- Malware Scanner: Scans files using VirusTotal API, with email alerts.
- Feedback Form: Collects user suggestions.
- Privacy Policy: Ensures transparency.
- Email Notifications: Alerts for critical findings.
- Multi-Language Support: English, Bemba, Nyanja.

## Setup
1. Install Python 3.8+.
2. Create virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables in `.env`: