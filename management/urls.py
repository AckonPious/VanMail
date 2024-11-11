from django.urls import path
from .views import *


urlpatterns = [
    
    # Users
    path('create-user', CreateUser.as_view(), name='create_user' ),
    path('users', UserListView.as_view(), name='users' ),
    path('user/<str:pk>', UserDetailView.as_view(), name='user_detail' ),
    path('user/update/<str:pk>', UserUpdateView.as_view(), name='user_update' ),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    
    # Locations
    path('create-location', LocationCreateView.as_view(), name='create_location'),
    path('locations', LocationListView.as_view(), name='locations'),
    path('location/update/<str:pk>', LocationUpdateView.as_view(), name='location_update'),
    path('location/delete/<str:pk>', LocationDeleteView.as_view(), name='location_delete'),

    # Drivers (AssignedTo)
    path('create-driver', DriverCreateView.as_view(), name='create_driver'),
    path('drivers', DriverListView.as_view(), name='drivers'),
    path('driver/update/<str:pk>', DriverUpdateView.as_view(), name='driver_update'),
    path('driver/delete/<str:pk>', DriverDeleteView.as_view(), name='driver_delete'),

    # MailBox and Individual Mail
    path('create-mailbox', AddNewMailBoxView.as_view(), name='add_new_mailbox'),
    path('mailboxes', MailBoxListView.as_view(), name='mail_boxes'),
    path('mailbox/add-individual-mail/<int:mail_id>', AddIndividualMailView.as_view(), name='add_individual_mail'),
    path('mailbox/update-individual-mail/<int:pk>', UpdateIndividualMailView.as_view(), name='update_individual_mail'),
    path('mailbox/final-submission/<int:mail_id>', FinalMailSubmit.as_view(), name='final_submittion'),
    
    path('mailbox/update/<str:pk>', MailBoxUpdateView.as_view(), name='update_mailbox'),
    path('mailbox/manage/<str:location_id>', ManageLocationMails.as_view(), name='manage_mails'), 
    path('mailbox/summary/<str:location_id>', ManageMailSummary.as_view(), name='mail_summary'),
    path('mailbox/submitted/<str:pk>', ReceivedMailboxMails.as_view(), name='view_submitted_mailbox'),
    
    # received mails
    path('receive-mail/', ReceiveMailView.as_view(), name='receive_mail'),
    path('logs/', LogEntryListView.as_view(), name='log_entries_list'),
    path('mark-as-read/<int:notification_id>/', MarkAsReadView.as_view(), name='mark_as_read'),
    
]
