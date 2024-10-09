from datetime import datetime
from .models import MailBox

class MailIDFactory:
    @staticmethod
    def generate_mail_id(location_name):
        current_year = datetime.now().year
        location_name = location_name.lower()  # Normalize location name to lowercase
        
        # New prefix format: location_year_
        prefix = f"{location_name}_{current_year}_"

        # Query the latest mail_id that starts with the location and year
        latest_mail = MailBox.objects.filter(mail_id__startswith=prefix).order_by('-mail_id').first()

        if latest_mail:
            # Get the last number of the mail_id and increment it
            last_id_number = int(latest_mail.mail_id.split('_')[-1])
            new_id_number = last_id_number + 1
        else:
            # If no mail found, start with 1
            new_id_number = 1

        # Return the new mail_id formatted as location_year_1, 2, 3, etc.
        return f"{prefix}{new_id_number}"
