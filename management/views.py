from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from authentication.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from mail.models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from mail.factory import MailIDFactory
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from django.core.paginator import Paginator
from packages.decorators import *
from django.contrib import messages


class LogEntryListView(LoginRequiredMixin, ListView):
    model = LogEntry
    template_name = 'logs/log_entries_list.html'
    context_object_name = 'log_entries'

    def get_queryset(self):
        return LogEntry.objects.all().order_by('-action_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'System Log Entries'
        return context
    
# Function to log actions
def log_action(user, instance, action_flag, change_message):
    """Log actions performed on models."""
    LogEntry.objects.log_action(
        user_id=user,
        content_type_id=ContentType.objects.get_for_model(instance).pk,
        object_id=instance.id,
        object_repr=str(instance),
        action_flag=action_flag,
        change_message=change_message
    )

# User CRUD
@method_decorator([login_required, admin_required], name='dispatch')
class CreateUser(CreateView):
    model = User
    template_name = 'authentication/create_user.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        return context

    def form_valid(self, form):
        user = form.save()
        log_action(self.request.user.pk, user, ADDITION, f"{self.request.user.full_name} added {form.instance.full_name} to the system")
        messages.success(self.request, 'User added successfully')
        return super().form_valid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'authentication/user_list.html'
    context_object_name = 'users'

@method_decorator([login_required, admin_required], name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'authentication/user_detail.html'
    context_object_name = 'user'

@method_decorator([login_required, admin_required], name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'authentication/delete_user.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        log_action(request.user, user, DELETION, f"{self.request.user.full_name} deleted {user.full_name} from the system")
        return super().delete(request, *args, **kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'authentication/update_user.html'
    context_object_name = 'user'
    fields = ['username', 'is_admin', 'is_registry', 'email', 'full_name']
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        user = form.save()
        log_action(self.request.user.pk, user, CHANGE, f"{self.request.user.full_name} updated {form.instance.full_name} in the system")
        messages.success(self.request, 'User Updated successfully')
        return super().form_valid(form)

# Location CRUD
@method_decorator([login_required, admin_required], name='dispatch')
class LocationCreateView(CreateView):
    model = Location
    template_name = 'location/create_location.html'
    form_class = LocationForm
    success_url = reverse_lazy('locations')

    def form_valid(self, form):
        location = form.save()
        log_action(self.request.user.pk, location, ADDITION, f"{self.request.user.full_name} added {form.instance.name} location to the system")
        messages.success(self.request, 'Location added successfully')
        return super().form_valid(form)

@method_decorator([login_required, admin_required], name='dispatch')
class LocationListView(ListView):
    model = Location
    template_name = 'location/location_list.html'
    context_object_name = 'locations'

@method_decorator([login_required, admin_required], name='dispatch')
class LocationDeleteView(DeleteView):
    model = Location
    template_name = 'location/delete_user.html'
    context_object_name = 'location'
    success_url = reverse_lazy('locations')

    def delete(self, request, *args, **kwargs):
        location = self.get_object()
        log_action(request.user, location, DELETION, f"{self.request.user.full_name} deleted {location.name} location from the system")
        return super().delete(request, *args, **kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class LocationUpdateView(UpdateView):
    model = Location
    template_name = 'location/update_location.html'
    context_object_name = 'location'
    fields = ['name']
    success_url = reverse_lazy('locations')

    def form_valid(self, form):
        location = form.save()
        log_action(self.request.user.pk, location, CHANGE, f"{self.request.user.full_name} updated {form.instance.name} location in the system")
        messages.success(self.request, 'Location Updated successfully')
        return super().form_valid(form)

# Driver CRUD
@method_decorator([login_required, registry_required], name='dispatch')
class DriverCreateView(CreateView):
    model = AssignedTo
    template_name = 'driver/create_driver.html'
    form_class = DriverForm
    success_url = reverse_lazy('drivers')

    def form_valid(self, form):
        driver = form.save()
        log_action(self.request.user.pk, driver, ADDITION, f"{self.request.user.full_name} added {form.instance.name} driver to the system")
        messages.success(self.request, 'Driver Created successfully')
        return super().form_valid(form)

@method_decorator([login_required, registry_required], name='dispatch')
class DriverListView(ListView):
    model = AssignedTo
    template_name = 'driver/driver_list.html'
    context_object_name = 'drivers'

@method_decorator([login_required, registry_required], name='dispatch')
class DriverDeleteView(DeleteView):
    model = AssignedTo
    template_name = 'driver/delete_driver.html'
    context_object_name = 'driver'
    success_url = reverse_lazy('drivers')

    def delete(self, request, *args, **kwargs):
        driver = self.get_object()
        log_action(request.user, driver, DELETION, f"{self.request.user.full_name} deleted {driver.name} driver from the system")
        messages.success(self.request, 'Driver Deleted successfully')
        return super().delete(request, *args, **kwargs)

@method_decorator([login_required, registry_required], name='dispatch')
class DriverUpdateView(UpdateView):
    model = AssignedTo
    template_name = 'driver/update_driver.html'
    context_object_name = 'driver'
    fields = ['name', 'phone_number']
    success_url = reverse_lazy('drivers')

    def form_valid(self, form):
        driver = form.save()
        log_action(self.request.user.pk, driver, CHANGE, f"{self.request.user.full_name} updated {driver.name} driver in the system")
        messages.success(self.request, 'Driver Updated successfully')
        return super().form_valid(form)

# Mail
@method_decorator([login_required, registry_required], name='dispatch')
class AddNewMailBoxView(LoginRequiredMixin, CreateView):
    model = MailBox
    form_class = MailBoxForm
    template_name = 'mail/new_mailbox.html'

    def get_initial(self):
        initial = super().get_initial()
        default_location = self.request.user.location

        if default_location:
            initial['mail_id'] = MailIDFactory.generate_mail_id(default_location.name)

        return initial

    def form_valid(self, form):
        mailbox = form.save(commit=False)
        mailbox.mail_id = form.cleaned_data['mail_id']
        mailbox.created_by = self.request.user
        mailbox.from_location = self.request.user.location
        mailbox.save()
        log_action(self.request.user.pk, mailbox, ADDITION, f"{self.request.user.full_name} added {form.instance.mail_id} to the system")  # Log the action
        messages.success(self.request, 'Mailbox Added successfully')
        return redirect('add_individual_mail', mail_id=mailbox.id)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_location = self.request.user.location
        form.fields['to_location'].queryset = Location.objects.exclude(id=user_location.id)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['assigned_to_list'] = AssignedTo.objects.all()
        return context

@method_decorator([login_required, registry_required], name='dispatch')
class MailBoxUpdateView(UpdateView):
    model = MailBox
    template_name = 'mail/update_mailbox.html'
    context_object_name = 'mailbox'
    fields = ['handling_officer', 'to_location', 'remarks']
    success_url = reverse_lazy('mail_boxes')

    def form_valid(self, form):
        mailbox = form.save()
        log_action(self.request.user.pk, mailbox, CHANGE, f"{self.request.user.full_name} updated {mailbox.mail_id} in the system")  # Log the action
        messages.success(self.request, 'Mailbox Updated successfully')
        return super().form_valid(form)

@method_decorator([login_required, registry_required], name='dispatch')
class AddIndividualMailView(LoginRequiredMixin, CreateView):
    model = Mail
    form_class = MailsForm
    template_name = 'mail/add_individual_mail.html'

    def get_mailbox(self):
        return get_object_or_404(MailBox, id=self.kwargs['mail_id'])

    def get_initial(self):
        initial = super().get_initial()
        mailbox = self.get_mailbox()
        current_count = mailbox.individual_mails.count()
        individual_mail_number = str(current_count + 1)
        initial['individual_mail_id'] = f"{mailbox.mail_id}_{individual_mail_number}"
        return initial

    def form_valid(self, form):
        individual_mail = form.save(commit=False)
        mailbox = self.get_mailbox()
        individual_mail.mail_box = mailbox
        individual_mail.individual_mail_id = form.cleaned_data['individual_mail_id']
        individual_mail.created_by = self.request.user
        individual_mail.save()
        log_action(self.request.user.pk, individual_mail, ADDITION, f"{self.request.user.full_name} added {form.instance.individual_mail_id} to the system")  # Log the action
        messages.success(self.request, 'Mail added successfully')
        return redirect('add_individual_mail', mail_id=mailbox.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailbox = self.get_mailbox()
        context['mailbox'] = mailbox
        individual_mails = mailbox.individual_mails.all().order_by('-created_at')
        paginator = Paginator(individual_mails, 8)  
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

@method_decorator([login_required, registry_required], name='dispatch')
class MailBoxListView(ListView):
    model = MailBox
    template_name = 'mail/mail_box_list.html'
    context_object_name = 'mailboxes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['mailboxes'] = MailBox.objects.filter(dispatch_date=today, from_location=self.request.user.location)
        drafted_past_mailboxes = MailBox.objects.filter(dispatch_date__lt=today, from_location=self.request.user.location, mail_status="Drafted")
        context['has_past_drafted_mailboxes'] = drafted_past_mailboxes.exists()
        context['drafted_past_mailboxes'] = drafted_past_mailboxes
        return context

@method_decorator([login_required, registry_required], name='dispatch')
class FinalMailSubmit(View):
    template_name = 'mail/final_submittion.html'

    def get(self, request, *args, **kwargs):
        mailbox_id = self.kwargs.get('mail_id')
        mailbox = MailBox.objects.get(pk=mailbox_id)
        mailbox_mails = Mail.objects.filter(mail_box=mailbox)
        drivers = AssignedTo.objects.all()
        form = FinalSubmissionForm
        context = {
            'mailbox': mailbox,
            'mailbox_mails': mailbox_mails,
            'form': form,
            'drivers': drivers,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        mailbox_id = self.kwargs.get('mail_id')
        mailbox = MailBox.objects.get(pk=mailbox_id)
        form = FinalSubmissionForm(request.POST, instance=mailbox)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.mail_status = "In Transit"
            submission.save()
            log_action(request.user.pk, submission, CHANGE, f"{self.request.user.full_name} submitted {submission.mail_id} to {submission.to_location.name}")  # Log the action
            messages.success(self.request, 'Mailbox submitted successfully')
            return redirect('mail_boxes')

@method_decorator([login_required, registry_required], name='dispatch')
class ReceiveMailView(View):
    template_name = 'mail/receive_mail.html'

    def get(self, request, *args, **kwargs):
        mailbox_id = request.GET.get('mailbox_id', None)
        mailbox = None
        form = None
        mails = []
        if mailbox_id:
            mailbox = get_object_or_404(MailBox, mail_id=mailbox_id)
            form = MailReceiveForm(mail_box=mailbox)
            mails = Mail.objects.filter(mail_box=mailbox)

        return render(request, self.template_name, {
            'mailbox': mailbox,
            'form': form,
            'mails': mails
        })

    def post(self, request, *args, **kwargs):
        mailbox_id = request.GET.get('mailbox_id', None)
        mailbox = get_object_or_404(MailBox, mail_id=mailbox_id)
        form = MailReceiveForm(request.POST, mail_box=mailbox)

        if form.is_valid():
            selected_mails = form.cleaned_data['mails']
            selected_mails.update(is_received=True)
            mailbox.mail_status = "Received"
            mailbox.save()
            log_action(request.user.pk, mailbox, CHANGE, f"{self.request.user.full_name} received {mailbox.mail_id} from {mailbox.from_location}")  # Log the action
            messages.success(self.request, 'Mailbox marked as received successfully')
            
            return redirect('mail_boxes')

        return render(request, self.template_name, {
            'mailbox': mailbox,
            'form': form,
        })

@method_decorator([login_required, registry_required], name='dispatch')
class ManageLocationMails(View):
    template_name = 'mail/manage_mails.html'

    def get(self, request, *args, **kwargs):
        location_id = self.kwargs.get('location_id')
        location = get_object_or_404(Location, pk=location_id)
        mailboxes = MailBox.objects.filter(from_location=location, mail_status="Received")

        context = {
            'mailboxes': mailboxes,
            'location': location,
        }
        return render(request, self.template_name, context)

@method_decorator([login_required, registry_required], name='dispatch')
class ReceivedMailboxMails(DetailView):
    model = MailBox
    template_name = 'mail/mail_box_mails.html'
    context_object_name = 'mailbox'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mails = Mail.objects.filter(mail_box=self.get_object())
        context['mails'] = mails
        return context

@method_decorator([login_required, registry_required], name='dispatch')
class ManageMailSummary(View):
    template_name = 'mail/mails_summary.html'

    def get(self, request, *args, **kwargs):
        location_id = self.kwargs.get('location_id')
        location = get_object_or_404(Location, pk=location_id)

        mailboxes = MailBox.objects.filter(mail_status="Received")
        sent_mailboxes = mailboxes.filter(from_location=location)
        received_mailboxes = mailboxes.filter(to_location=location)

        mailboxes_sent = {}
        for mailbox in sent_mailboxes:
            to_location = mailbox.to_location
            if to_location not in mailboxes_sent:
                mailboxes_sent[to_location] = []
            mailboxes_sent[to_location].append(mailbox)

        mailboxes_received = {}
        for mailbox in received_mailboxes:
            from_location = mailbox.from_location
            if from_location not in mailboxes_received:
                mailboxes_received[from_location] = []
            mailboxes_received[from_location].append(mailbox)

        context = {
            'mailboxes_received': mailboxes_received,
            'mailboxes_sent': mailboxes_sent,
            'location': location,
        }

        return render(request, self.template_name, context)