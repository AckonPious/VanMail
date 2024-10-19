from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from packages.decorators import *
from django.contrib.auth.decorators import login_required
from mail.models import *
from django.contrib.admin.models import LogEntry 

from django.utils import timezone
@method_decorator([login_required, registry_required], name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'
    
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()  
        
        if request.user.is_superadmin:
            # Do not filter
            total_mailbox = MailBox.objects.all().count()
            mailbox = MailBox.objects.filter(mail_status="Received")
            mailbox_count = mailbox.count()
            
            mails = Mail.objects.filter(is_received=True)
            mails_count = mails.count()
            drafted_count = MailBox.objects.filter(mail_status='Drafted').count()
            in_transit_count = MailBox.objects.filter(mail_status='In Transit').count()
            received_count = MailBox.objects.filter(mail_status='Received').count()
            drafted_per = round((drafted_count / total_mailbox) * 100, 2)
            in_transit_per = round((in_transit_count / total_mailbox) * 100, 2)
            received_per = round((received_count / total_mailbox) * 100, 2)

            log_entries = LogEntry.objects.filter(action_time__date=today)

        elif request.user.is_admin:
            total_mailbox = MailBox.objects.filter(from_location=request.user.location).count()
            mailbox = MailBox.objects.filter(mail_status="Received", from_location=request.user.location)
            mailbox_count = mailbox.count()
            
            mails = Mail.objects.filter(is_received=True)
            mails_count = mails.count()
            drafted_count = MailBox.objects.filter(mail_status='Drafted', from_location=request.user.location).count()
            in_transit_count = MailBox.objects.filter(mail_status='In Transit', from_location=request.user.location).count()
            received_count = MailBox.objects.filter(mail_status='Received', from_location=request.user.location).count()
            drafted_per = round((drafted_count / total_mailbox) * 100, 2)
            in_transit_per = round((in_transit_count / total_mailbox) * 100, 2)
            received_per = round((received_count / total_mailbox) * 100, 2)

            log_entries = LogEntry.objects.filter(action_time__date=today)

        else:
            total_mailbox = MailBox.objects.filter(created_by=request.user).count()
            mailbox = MailBox.objects.filter(mail_status="Received", created_by=request.user)
            mailbox_count = mailbox.count()
            
            mails = Mail.objects.filter(is_received=True, created_by=request.user)
            mails_count = mails.count()
            drafted_count = MailBox.objects.filter(mail_status='Drafted', created_by=request.user).count()
            in_transit_count = MailBox.objects.filter(mail_status='In Transit', created_by=request.user).count()
            received_count = MailBox.objects.filter(mail_status='Received', created_by=request.user).count()
            drafted_per = round((drafted_count / total_mailbox) * 100, 2)
            in_transit_per = round((in_transit_count / total_mailbox) * 100, 2)
            received_per = round((received_count / total_mailbox) * 100, 2)

            log_entries = LogEntry.objects.filter(action_time__date=today, user=request.user)

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