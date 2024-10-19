from django import template
from authentication.models import Location, User
from mail.models import MailBox, Mail, AssignedTo

register = template.Library()

@register.simple_tag
def get_recent_logs():
    locations = Location.objects.order_by('-updated_at')[:50]
    users = User.objects.order_by('-updated_at')[:50]  
    drivers = AssignedTo.objects.all().order_by('-updated_at')
    mailboxes = MailBox.objects.order_by('-updated_at')[:50]
    mails = Mail.objects.order_by('-updated_at')[:50]
    
    all_logs = list(locations) + list(users) + list(mailboxes) + list(mails) + list(drivers)
    sorted_logs = sorted(all_logs, key=lambda obj: getattr(obj, 'updated_at', None) or getattr(obj, 'date_joined', None), reverse=True)
    
    for log in sorted_logs:
        if isinstance(log, MailBox):
            if log.created_at < log.updated_at:
                log.action = log.mail_status
            else:
                log.action = log.mail_status
        else:
            log.action = "Updated" if log.created_at < log.updated_at else "Added"

    return sorted_logs[:40]
