from django.db import models
from authentication.models import User
from authentication.models import Location 

class ModelInherit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class AssignedTo(ModelInherit):
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=False)
    def __str__(self):
        return f"{self.name}" 

MAIL_STATUS = [
        ('Drafted', 'Drafted'),
        ('In Transit', 'In Transit'),
        ('Received', 'Received'),
    ]  
class MailBox(ModelInherit):
    mail_id = models.CharField(max_length=200, unique=True)
    handling_officer = models.CharField(max_length=100)
    dispatch_date = models.DateField(auto_now_add=True)
    mail_status = models.CharField(max_length=50, default='Drafted', choices=MAIL_STATUS)
    remarks = models.TextField(blank=True, null=True)
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='to_location')
    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='from_location')
    assigned_to = models.ForeignKey(AssignedTo, on_delete=models.SET_NULL, null=True, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)  

    def __str__(self):
        return f"{self.mail_id}" 
    
    def number_of_mails(self):
        return self.individual_mails.count()
        


class Mail(ModelInherit):
    mail_box = models.ForeignKey(MailBox, on_delete=models.PROTECT, related_name='individual_mails')
    individual_mail_id = models.CharField(max_length=100, unique=True)  
    mail_description = models.TextField(blank=False, null=True)
    priority_level = models.CharField(max_length=15, choices=[('Standard', 'Standard'), ('High Priority', 'High Priority')])
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by', blank=False) 
    is_received = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.individual_mail_id}" 
