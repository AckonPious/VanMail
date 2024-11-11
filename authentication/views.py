from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from packages.decorators import *
from django.contrib.auth.decorators import login_required
from mail.models import *
from django.contrib.admin.models import LogEntry 
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils import timezone

@method_decorator([login_required, registry_required], name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'
    
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()  
        user_location = None 
        
        if request.user.is_authenticated:
            user_location = request.user.location 
            
        if request.user.is_superadmin:
            mailboxes = MailBox.objects.filter(mail_status="Received")
            received_mailboxes = mailboxes

            mails_per_location = {}
            for mailbox in received_mailboxes:
                labels = mailbox.from_location
                if labels not in mails_per_location:
                    mails_per_location[labels] = 0
                mails_per_location[labels] += mailbox.number_of_mails()
           
            total_mailbox = MailBox.objects.all.count()
            mailbox = MailBox.objects.filter(mail_status="Received")
            mailbox_count = mailbox.count()            
            
            mails = Mail.objects.filter(is_received=True)
            mails_count = mails.count()
            
            drafted= MailBox.objects.filter(mail_status='Drafted')
            drafted_count = drafted.count()
            
            in_transit = MailBox.objects.filter(mail_status='In Transit')
            in_transit_count = in_transit.count()
            
            received = MailBox.objects.filter(mail_status='Received')
            received_count=received.count()
            
            
            drafted_mails = 0
            for mail in drafted:
                drafted_mails+=mail.number_of_mails()
                
            in_transit_mails = 0
            for mail in in_transit:
                in_transit_mails+=mail.number_of_mails()
                
            received_mails = 0
            for mail in received:
                received_mails+=mail.number_of_mails()
                
            total_sum = drafted_mails + in_transit_mails + received_mails
            
            if total_sum > 0:
                    drafted_per = round((drafted_mails / total_sum) * 100, 2)
                    in_transit_per = round((in_transit_mails / total_sum) * 100, 2)
                    received_per = round((received_mails / total_sum) * 100, 2)
            else:
                drafted_per = 0
                in_transit_per = 0
                received_per = 0 
                
            log_entries = LogEntry.objects.filter(action_time__date=today)
            
            current_date = timezone.now().date()
            start_of_today = timezone.make_aware(datetime.combine(current_date, datetime.min.time()))
            end_of_today = timezone.make_aware(datetime.combine(current_date, datetime.max.time()))

            notifications = Notification.objects.filter(
                location=user_location,
                timestamp__gte=start_of_today,
                timestamp__lt=end_of_today
            ).order_by('-timestamp')
            
            
        elif request.user.is_admin:
            mailboxes = MailBox.objects.filter(mail_status="Received")
            received_mailboxes = mailboxes.filter(to_location=user_location)

            mails_per_location = {}
            for mailbox in received_mailboxes:
                labels = mailbox.from_location
                if labels not in mails_per_location:
                    mails_per_location[labels] = 0
                mails_per_location[labels] += mailbox.number_of_mails()
           
            total_mailbox = MailBox.objects.filter(from_location=user_location).count()
            mailbox = MailBox.objects.filter(mail_status="Received", to_location=user_location)
            mailbox_count = mailbox.count()            
            
            mails = Mail.objects.filter(is_received=True, mail_box__to_location=user_location)
            mails_count = mails.count()
            
            drafted= MailBox.objects.filter(mail_status='Drafted',from_location=user_location)
            drafted_count = drafted.count()
            
            in_transit = MailBox.objects.filter(mail_status='In Transit',  from_location=user_location)
            in_transit_count = in_transit.count()
            
            received = MailBox.objects.filter(mail_status='Received',  to_location=user_location)
            received_count=received.count()
            
            
            drafted_mails = 0
            for mail in drafted:
                drafted_mails+=mail.number_of_mails()
                
            in_transit_mails = 0
            for mail in in_transit:
                in_transit_mails+=mail.number_of_mails()
                
            received_mails = 0
            for mail in received:
                received_mails+=mail.number_of_mails()
                
            total_sum = drafted_mails + in_transit_mails + received_mails
            
            if total_sum > 0:
                drafted_per = round((drafted_mails / total_sum) * 100, 2)
                in_transit_per = round((in_transit_mails / total_sum) * 100, 2)
                received_per = round((received_mails / total_sum) * 100, 2)
            else:
                drafted_per = 0
                in_transit_per = 0
                received_per = 0 
            log_entries = LogEntry.objects.filter(action_time__date=today)
            
            current_date = timezone.now().date()
            start_of_today = timezone.make_aware(datetime.combine(current_date, datetime.min.time()))
            end_of_today = timezone.make_aware(datetime.combine(current_date, datetime.max.time()))

            notifications = Notification.objects.filter(
                location=user_location,
                timestamp__gte=start_of_today,
                timestamp__lt=end_of_today
            ).order_by('-timestamp')
            

        elif request.user.is_registry:
            mailboxes = MailBox.objects.filter(mail_status="Received")
            received_mailboxes = mailboxes.filter(to_location=user_location)

            mails_per_location = {}
            for mailbox in received_mailboxes:
                labels = mailbox.from_location
                if labels not in mails_per_location:
                    mails_per_location[labels] = 0
                mails_per_location[labels] += mailbox.number_of_mails()

           
            total_mailbox = MailBox.objects.filter(from_location=user_location).count()
            mailbox = MailBox.objects.filter(mail_status="Received", to_location=user_location)
            mailbox_count = mailbox.count()            
            
            mails = Mail.objects.filter(is_received=True, mail_box__to_location=user_location)
            mails_count = mails.count()
            
            drafted= MailBox.objects.filter(mail_status='Drafted',from_location=user_location)
            drafted_count = drafted.count()
            
            in_transit = MailBox.objects.filter(mail_status='In Transit',  from_location=user_location)
            in_transit_count = in_transit.count()
            
            received = MailBox.objects.filter(mail_status='Received',  to_location=user_location)
            received_count=received.count()
            
            
            drafted_mails = 0
            for mail in drafted:
                drafted_mails+=mail.number_of_mails()
                
            in_transit_mails = 0
            for mail in in_transit:
                in_transit_mails+=mail.number_of_mails()
                
            received_mails = 0
            for mail in received:
                received_mails+=mail.number_of_mails()
                
            total_sum = drafted_mails + in_transit_mails + received_mails
            
            if total_sum > 0:
                    drafted_per = round((drafted_mails / total_sum) * 100, 2)
                    in_transit_per = round((in_transit_mails / total_sum) * 100, 2)
                    received_per = round((received_mails / total_sum) * 100, 2)
            else:
                drafted_per = 0
                in_transit_per = 0
                received_per = 0  

            log_entries = LogEntry.objects.filter(action_time__date=today, user=request.user)
            
            current_date = timezone.now().date()
            start_of_today = timezone.make_aware(datetime.combine(current_date, datetime.min.time()))
            end_of_today = timezone.make_aware(datetime.combine(current_date, datetime.max.time()))

            notifications = Notification.objects.filter(
                location=user_location,
                timestamp__gte=start_of_today,
                timestamp__lt=end_of_today
            ).order_by('-timestamp')

        monthly_received_mails = (
            Mail.objects.filter(is_received=True, mail_box__to_location=user_location)
            .annotate(month=TruncMonth('updated_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
            )
        
            
        months = [mail['month'].strftime('%b') for mail in monthly_received_mails]
        received_counts = [mail['count'] for mail in monthly_received_mails]
        
        context = {
            "mailbox_count": mailbox_count,
            "mails_count": mails_count,
            'drafted_count': drafted_count,
            'in_transit_count': in_transit_count,
            'received_count': received_count,
            'drafted_per': drafted_per,
            'in_transit_per': in_transit_per,
            'received_per': received_per,
            'log_entries': log_entries,  
            "months": months,
            "received_counts": received_counts,
            'notifications': notifications, 
            'mails_per_location': mails_per_location,
        }
        
        
        return render(request, self.template_name, context)


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')  
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Signin.html')

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.') 
    return redirect("login")