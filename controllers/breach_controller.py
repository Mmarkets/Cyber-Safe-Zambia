import requests
import hashlib
import time

def check_breach(email):
    if not email or not '@' in email:
        return {'status': 'Invalid email address', 'category': 'danger'}
    try:
        email_hash = hashlib.sha1(email.lower().encode()).hexdigest().upper()
        prefix = email_hash[:5]
        suffix = email_hash[5:]
        headers = {'User-Agent': 'CyberSafeZambia'}
        response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}', headers=headers)
        response.raise_for_status()
        hashes = response.text.splitlines()
        for h in hashes:
            if h.split(':')[0] == suffix:
                return {'status': 'Email Found in Breaches', 'category': 'danger'}
        return {'status': 'No Breaches Found', 'category': 'success'}
    except Exception as e:
        return {'status': f'Error: {str(e)}', 'category': 'danger'}
    finally:
        time.sleep(1.5)  # Respect HIBP rate limit