from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    # common pages
    path('home/', views.home, name='home'),
    path('my/bookings/', views.my_bookings, name='my_bookings'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('event/booked/<int:id>/', views.specific_event_bookings, name='specific_event_booking'),
    path('service/booked/<int:id>/', views.specific_service_bookings, name='specific_service_booking'),

    # guest urls
    path('guest/', views.guest, name='guest'),
    # events related
    path('events/', views.all_events, name='events'),
    path('event/<int:id>/', views.specific_event, name='specific_event'),
    path('book/event/<int:id>/', views.book_event, name='book_event'),
    path('add/event/', views.add_event, name='add_event'),
    path('confirm/event/booking/<int:id>/', views.confirm_event_booking, name='confirm_event_booking'),
    path('my/events/', views.my_events, name='my_events'),
    path('delete/my/event/<int:id>/', views.delete_my_event, name='delete_my_event'),
    path('edit/my/event/<int:id>/', views.edit_my_event, name='edit_my_event'),


    # ajax functions
    path('ajax/event/booking/delete/<int:id>', views.ajax_delete_event_booking, name='ajax_delete_event_booking'),
    path('ajax/confirm/booking/event/<int:event_id>/<int:requester_id>/', views.ajax_confirm_event_booking, name='ajax_confirm_event_booking'),
    path('ajax/cancel/booking/event/<int:event_id>/<int:requester_id>/', views.ajax_cancel_event_booking, name='ajax_cancel_event_booking'),

    # services related
    path('services/', views.all_services_categories, name='services'),
    path('service/<int:id>/', views.specific_service, name='specific_service'),
    path('book/service/<int:id>/', views.book_service, name='book_service'),
    path('add/service/', views.add_service, name='add_service'),
    path('confirm/service/booking/<int:id>/', views.confirm_service_booking, name='confirm_service_booking'),
    path('my/services/', views.my_services, name='my_services'),
    path('delete/my/service/<int:id>/', views.delete_my_service, name='delete_my_service'),
    path('edit/my/service/<int:id>/', views.edit_my_service, name='edit_my_service'),


    # ajax functions
    path('ajax/service/booking/delete/<int:id>/', views.ajax_delete_service_booking, name='ajax_delete_service_booking'),
    path('ajax/confirm/booking/<int:service_id>/<int:requester_id>/', views.ajax_confirm_service_booking, name='ajax_confirm_service_booking'),
    path('ajax/cancel/booking/<int:service_id>/<int:requester_id>/', views.ajax_cancel_service_booking, name='ajax_cancel_service_booking'),


    # Admin
    path('booking/requests/', views.booking_requests, name='booking_requests'),

    





]

