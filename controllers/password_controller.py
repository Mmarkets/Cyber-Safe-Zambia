from zxcvbn import zxcvbn
import secrets
import string

def generate_password(length, include_symbols):
    characters = string.ascii_letters + string.digits
    if include_symbols:
        characters += string.punctuation
    try:
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return {'password': password, 'status': 'Password generated successfully', 'category': 'success'}
    except Exception as e:
        return {'password': None, 'status': f'Error: {str(e)}', 'category': 'danger'}

def check_password_strength(password):
    try:
        result = zxcvbn(password)
        score = result['score']
        feedback = result['feedback']['suggestions']
        if score <= 1:
            return {
                'status': 'Weak Password',
                'feedback': ', '.join(feedback) or 'Use a longer, more complex password.',
                'category': 'danger'
            }
        elif score <= 3:
            return {
                'status': 'Medium Password',
                'feedback': ', '.join(feedback) or 'Consider adding more unique characters.',
                'category': 'warning'
            }
        else:
            return {
                'status': 'Strong Password',
                'feedback': 'Great job! Your password is secure.',
                'category': 'success'
            }
    except Exception as e:
        return {
            'status': f'Error: {str(e)}',
            'feedback': 'Unable to process password.',
            'category': 'danger'
        }