import smtplib
from pathlib import Path
import os
from dotenv import load_dotenv\

class Util:
    '''Utility class'''
    
    @staticmethod
    def send_email(data):
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
        load_dotenv(os.path.join(BASE_DIR, ".env"))
        
        EMAIL_HOST_USER = os.getenv('MY_EMAIL')
        EMAIL_HOST_PASSWORD = os.getenv('PASSWORD')
        
        with smtplib.SMTP('smtp.gmail.com', 587) as conn:
            conn.starttls()
            conn.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)
            
            conn.sendmail(
                from_addr=EMAIL_HOST_USER, 
                to_addrs=data['email'],
                msg=f"Subject:{data['subject']}\n\n{data['body']}"
            )
            