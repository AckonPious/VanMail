from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from packages.decorators import *
from django.contrib.auth.decorators import login_required
from mail.models import *

@method_decorator([login_required, registry_required], name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'
    
    def get(self, request, *args, **kwargs):
        mailbox = MailBox.objects.filter(mail_status = "Received")
        mailbox_count = mailbox.count()
        
        mails = Mail.objects.filter(is_received=True)
        mails_count = mails.count()
        context = {
            "mailbox_count": mailbox_count,
            "mails_count": mails_count,
            
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

