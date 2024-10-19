from datetime import datetime
from .models import MailBox 

class MailIDFactory:
    @staticmethod
    def generate_mail_id(location_name):
        now = datetime.now()
        current_year = now.year
        day_of_year = now.timetuple().tm_yday
        location_name = location_name.lower()
        prefix = f"{location_name}_{current_year}_{day_of_year}_"
        latest_mail = MailBox.objects.filter(mail_id__startswith=prefix).order_by('-mail_id').first()
        
        if latest_mail:
            last_id_number = int(latest_mail.mail_id.split('_')[-1])
            new_id_number = last_id_number + 1
        else:
            new_id_number = 1
        return f"{prefix}{new_id_number}"

