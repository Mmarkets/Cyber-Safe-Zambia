import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('860cb606c2f1d541e4eaa2fbd9740ad82adcd90b77dc5338a27314a184c2f438')
    # PHISHTANK_API_KEY = os.getenv('PHISHTANK_API_KEY')  # Deprecated
    GOOGLE_SAFE_BROWSING_API_KEY = os.getenv('AIzaSyCYJiucXgbX-dc2n5wnXMyQCLZrrLZTgN8')
    VIRUSTOTAL_API_KEY = os.getenv('74c56dec6196b1ffc9570a24e7bbcbae8bc91458929f3071a7d7049794147928')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    API_KEY = os.getenv('a299dc435f7cd6c61c01fdc26978bc2d6b240bee5c14989220b247f05008e9ac')