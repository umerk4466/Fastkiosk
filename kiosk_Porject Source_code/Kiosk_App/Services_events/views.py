from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Users.models import Profile,Student_data
from Users.forms import Student_Form, Profile_Form, User_Form
from .models import Event,Category,Service,Event_booking,Booking_status,Service_booking
# import forms
from Services_events.forms import Event_Form, Service_Form,Category_Form
# for ajax functions
from django.http import JsonResponse

# Create your views here.
@login_required
def home(request):
    u = Profile.objects.get(user=request.user)
    role = u.role.permission.name
    context = {'role': role,}
    return render(request,'Services_events/comman_pages/home.html' ,context,)

# guest functions
def guest(request):
    return render(request,'Services_events/guest_pages/guest_home.html',)


# comman pages functions
# event related
def all_events(request):
    # check if user is login and then send role to the page
    if request.user.is_authenticated:
        u = Profile.objects.get(user=request.user)
        role = u.role.permission.name
    else: 
        role = ''
    # get and send all events
    events = Event.objects.all()

    context = {'role': role, 'events':events}
    return render(request,'Services_events/comman_pages/all_events.html',context,)

def specific_event(request, id):
    # check if user is login and then send role to the page
    if request.user.is_authenticated:
        u = Profile.objects.get(user=request.user)
        role = u.role.permission.name
        is_owner = Event.objects.filter(id=id, user=request.user).exists()
        is_already_booked = Event_booking.objects.filter(event_id=id,user=request.user).exists()


    else: 
        role = ''
        is_owner = False
        is_already_booked = False
    # get and send pecific event details
    event_details = Event.objects.filter(id=id)
    context = {'role': role, 'event_details': event_details, 'is_owner' : is_owner, 'is_already_booked' : is_already_booked}
    return render(request,'Services_events/comman_pages/specific_event.html',context,)


# services related
def all_services_categories(request):
    # check if user is login and then send role to the page
    if request.user.is_authenticated:
        u = Profile.objects.get(user=request.user)
        role = u.role.permission.name
    else: 
        role = ''
    categories = Category.objects.all()
    context = {'role': role, 'categories' : categories}
    return render(request,'Services_events/comman_pages/all_services_categories.html',context)

def specific_service(request,id):
    # check if user is login and then send role to the page
    if request.user.is_authenticated:
        u = Profile.objects.get(user=request.user)
        role = u.role.permission.name
        is_owner = Service.objects.filter(id=id, user=request.user).exists()
        is_already_booked = Service_booking.objects.filter(service_id=id,user=request.user).exists()

    else: 
        role = ''
        is_owner = False
        is_already_booked = False

    # get and send pecific event details
    service_details = Service.objects.filter(id=id)
    context = {'role': role, 'service_details': service_details, 'is_owner' : is_owner, 'is_already_booked':is_already_booked,}
    return render(request,'Services_events/comman_pages/specific_service.html',context,)

@login_required
def my_bookings(request):
    u = Profile.objects.get(user=request.user)
    role = u.role.permission.name
    context = {'role': role,}

    # send user event and service booking which he made
    service_bookings = Service_booking.objects.filter(user=request.user)
    event_bookings = Event_booking.objects.filter(user=request.user)

    context = {'role': role,'service_bookings': service_bookings,'event_bookings': event_bookings,}
    return render(request,'Services_events/comman_pages/my_bookings.html',context,)


# @login_required
def profile(request,id):
    # check if received user id is valid user id
    if User.objects.filter(pk=id).exists():
        # check if profile viewer is the current user or someone else
        is_owner = False
        if request.user.is_authenticated and request.user.id == id:
            is_owner = True
        # send user data according to the received id
        user_details = User.objects.filter(pk=id)
        user = User.objects.get(pk=id)
        role = user.profile.role.name
        if role == "Student":
            student_details = Student_data.objects.filter(profile=user.profile)
            student_data = Student_data.objects.get(profile_id=user.profile.id)
            student_form = Student_Form(request.POST or None, instance=student_data)
        else:
            student_details = None
            student_form = None

        # send forms in the templates
        user_form = User_Form(request.POST or None, instance=user)
        profile_form = Profile_Form(request.POST or None, instance=user.profile)
        # validate received form and save the data
        if request.POST and user_form.is_valid() or  profile_form.is_valid():
            if role == "Student":
                if student_form.is_valid():
                    student_form.save()
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile Updated Successfully!!!')

        context = {'is_owner': is_owner,'user_details': user_details, 'student_details': student_details, 'user_form' : user_form, 'profile_form': profile_form, 'student_form':student_form, }
        return render(request,'Services_events/comman_pages/profile.html',context,)
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User not found!!!</h1><h2 style='color:white'>Go back and try to see valid user profile</h2</center></body")



@login_required
def specific_event_bookings(request, id):
    u = Profile.objects.get(user=request.user)
    role = u.role.permission.name

    event_booking_details = Event_booking.objects.filter(event_id=id, user=request.user) 
    
    context = {'role': role, 'event_booking_details':event_booking_details, }
    return render(request,'Services_events/comman_pages/specific_event_booking.html',context,)


@login_required
def specific_service_bookings(request, id):
    u = Profile.objects.get(user=request.user)
    role = u.role.permission.name

    service_booking_details = Service_booking.objects.filter(service_id=id, user=request.user) 

    context = {'role': role, 'service_booking_details': service_booking_details,}
    return render(request,'Services_events/comman_pages/specific_service_booking.html',context,)


@login_required
def book_event(request, id):
    u = Profile.objects.get(user=request.user)
    role = u.role.permission.name
    if u.role.name == "Student":
        # student form
        student_data = Student_data.objects.get(profile_id=u.id)
        student_form = Student_Form(instance=student_data)
    else:
        student_form = None
    # send event to the template
    event_details = Event.objects.filter(id=id)
    
    context = {'role': role, 'event_details' : event_details, 'student_form':student_form,}
    return render(request,'Services_events/comman_pages/book_event.html',context,)

@login_required
def confirm_event_booking(request,id):
    if Event_booking.objects.filter(user=request.user,event_id=id).exists():
        messages.warning(request, 'You already booked this Event check your bookings')
        return redirect('specific_event', id=id)
    else:
        if Booking_status.objects.filter(status="Pending").exists():
            pending_status = Booking_status.objects.get(status="Pending")
        else:
            pending_status = Booking_status.objects.create(status="Pending")
            pending_status.save()

        event_booking = Event_booking.objects.create(user=request.user,event_id=id, status=pending_status)
        event_booking.save()
        if Event_booking.objects.filter(user=request.user,event_id=id).exists():
            messages.success(request, 'Your event booking request has been made successfully')
            return redirect('my_bookings')
        else:
            messages.error(request, 'Error!!! Something is wrong please check you connection')


@login_required
def book_service(request, id):
    u = Profile.objects.get(user=request.user)
    role = u.role.permission.name
    if u.role.name == "Student":
        # student form
        student_data = Student_data.objects.get(profile_id=u.id)
        student_form = Student_Form(instance=student_data)
    else:
        student_form = None
    # send service to the template
    service_details = Service.objects.filter(id=id)
    
    context = {'role': role, 'service_details' : service_details, 'student_form':student_form,}
    return render(request,'Services_events/comman_pages/book_service.html',context,)



@login_required
def confirm_service_booking(request,id):
    if Service_booking.objects.filter(user=request.user,service_id=id).exists():
        messages.warning(request, 'You already booked this Service check your bookings')
        return redirect('specific_service', id=id)
    else:
        if Booking_status.objects.filter(status="Pending").exists():
            pending_status = Booking_status.objects.get(status="Pending")
        else:
            pending_status = Booking_status.objects.create(status="Pending")
            pending_status.save()

        service_booking = Service_booking.objects.create(user=request.user,service_id=id, status=pending_status)
        service_booking.save()
        if Service_booking.objects.filter(user=request.user,service_id=id).exists():
            messages.success(request, 'Your service booking request has been made successfully')
            return redirect('my_bookings')
        else:
            messages.error(request, 'Error!!! Something is wrong please check you connection')

# add event and service function
@login_required
def add_event(request):
    if request.method == 'POST':
        add_event_form = Event_Form(request.POST)

        if add_event_form.is_valid():
            event = add_event_form.save(commit=False)
            if request.user.profile.role.name == "Admin":
                event.user = request.user
                event.save()
                messages.success(request, 'Event created successfully')
                return redirect('login')
            else:
                messages.error(request, 'Error!!! You do not have permission to add event')
    else:
        add_event_form = Event_Form()

    context = {'add_event_form': add_event_form}
    return render(request,'Services_events/admin_pages/add_event.html',context,)


@login_required
def add_service(request):
    if request.method == 'POST':
        add_service_form = Service_Form()
        add_category_form = Category_Form()
        # check which form is submited and then save data accordingly
        if 'add_service_form' in request.POST :
            add_service_form = Service_Form(request.POST)
            if add_service_form.is_valid():
                service = add_service_form.save(commit=False)
                if request.user.profile.role.name == "Admin":
                    service.user = request.user
                    service.save()
                    messages.success(request, 'Service created successfully')
                    return redirect('login')
                else:
                    messages.error(request, 'Error!!! You do not have permission to add service')
        elif 'add_category_form' in request.POST :
            add_category_form = Category_Form(request.POST)
            if add_category_form.is_valid():
                add_category_form.save()
                messages.success(request, 'Category created successfully')
    else:
        add_service_form = Service_Form()
        add_category_form = Category_Form()
    
    context = {'add_service_form':add_service_form,'add_category_form':add_category_form,}
    return render(request,'Services_events/admin_pages/add_service.html',context,)
    
# for admin my events page
@login_required
def my_events(request):
    # check if the user is admin
    if Profile.objects.filter(user_id=request.user.id, role__name="Admin").exists():
        # get list of the all events rquested user id 
        user_events = Event.objects.filter(user_id=request.user.id)
        # send user events to the template
        context = {'user_events':user_events}
        return render(request,'Services_events/admin_pages/my_events.html',context,)
    # if user not found or not a admin send not found reponse
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User is not admin or not exists!!!</h1><h2 style='color:white'>Go back and try to to get valid admin</h2</center></body")


# for admin my services page
@login_required
def my_services(request):
    # check if the user is admin
    if Profile.objects.filter(user_id=request.user.id, role__name="Admin").exists():
        # get list of the all services rquested user id 
        user_services = Service.objects.filter(user_id=request.user.id)
        # send user services to the template
        context = {'user_services':user_services}
        return render(request,'Services_events/admin_pages/my_services.html',context,)
    # if user not found or not a admin send not found reponse
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User is not admin or not exists!!!</h1><h2 style='color:white'>Go back and try to to get valid admin</h2</center></body")

# add function to see booking_requests for admin
@login_required
def booking_requests(request):
    # check user is admin
    if request.user.profile.role.name == "Admin":
        # get objects of the user's services booking requests
        services_requests = Service_booking.objects.filter(service__user=request.user.id)
        # get objects of the user's events booking requests
        events_requests = Event_booking.objects.filter(event__user=request.user.id)

        # pass to the context for manupulating in template
        context = {'services_requests':services_requests, 'events_requests' : events_requests}
        return render(request,'Services_events/admin_pages/booking_requests.html',context,)

    # if user not found or not a admin send not found reponse
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User is not admin or not exists!!!</h1><h2 style='color:white'>Go back and try to to get valid admin</h2</center></body")


# add function to delete the admin's event
@login_required
def delete_my_event(request,id):
    # check user is admin
    if request.user.profile.role.name == "Admin":
        # check if the the admin is the owner of the received event id
        if Event.objects.filter(pk=id, user=request.user).exists():
            # find the event and delete it
            admin_event = Event.objects.get(pk=id, user=request.user)
            admin_event.delete()
            messages.success(request, 'Event Deleted successfully')
            return redirect('my_events')
        else:
            messages.error(request, 'Error!!! You could not delete the event. Make sure you are the owner of this event')
            return redirect('my_events')
            
    # if user not found or not a admin send not found reponse
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User is not admin or not exists!!!</h1><h2 style='color:white'>Go back and try to to get valid admin</h2</center></body")



# add function to edit the admin's event
@login_required
def edit_my_event(request,id):
    # check user is admin
    if request.user.profile.role.name == "Admin":
        # check if the the admin is the owner of the received event id
        if Event.objects.filter(pk=id, user=request.user).exists():
            # get the event instance
            event = Event.objects.get(pk=id)
            # get event form and pass to the context
            event_form = Event_Form(request.POST or None, instance=event)
            # on post request validate the event and save
            if request.POST and event_form.is_valid():
                event_form.save()
                messages.success(request, 'Event edited successfully')
                return redirect('specific_event', id=id)
            
            context = {'event_form':event_form}
            return render(request,'Services_events/admin_pages/edit_my_event.html',context,)
        else:
            messages.error(request, 'Error!!! You could not edit the event. Make sure you are the owner of this event')
            return redirect('my_events')
            
    # if user not found or not a admin send not found reponse
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User is not admin or not exists!!!</h1><h2 style='color:white'>Go back and try to to get valid admin</h2</center></body")


# add function to delete the admin's service
@login_required
def delete_my_service(request,id):
    # check user is admin
    if request.user.profile.role.name == "Admin":
        # check if the the admin is the owner of the received service id
        if Service.objects.filter(pk=id, user=request.user).exists():
            # find the service and delete it
            admin_service = Service.objects.get(pk=id, user=request.user)
            admin_service.delete()
            messages.success(request, 'Service Deleted successfully')
            return redirect('my_services')
        else:
            messages.error(request, 'Error!!! You could not delete the service. Make sure you are the owner of this service')
            return redirect('my_services')
            
    # if user not found or not a admin send not found reponse
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User is not admin or not exists!!!</h1><h2 style='color:white'>Go back and try to to get valid admin</h2</center></body")

# add function to edit the admin's service
@login_required
def edit_my_service(request,id):
    # check user is admin
    if request.user.profile.role.name == "Admin":
        # check if the the admin is the owner of the received service id
        if Service.objects.filter(pk=id, user=request.user).exists():
            # get the service instance
            service = Service.objects.get(pk=id)
            # get service form and pass to the context
            service_form = Service_Form(request.POST or None, instance=service)
            # on post request validate the service and save
            if request.POST and service_form.is_valid():
                service_form.save()
                messages.success(request, 'Service edited successfully')
                return redirect('specific_service', id=id)
            
            context = {'service_form':service_form}
            return render(request,'Services_events/admin_pages/edit_my_service.html',context,)
        else:
            messages.error(request, 'Error!!! You could not edit the service. Make sure you are the owner of this service')
            return redirect('my_services')
            
    # if user not found or not a admin send not found reponse
    else:
        return HttpResponseNotFound("<body style='background-color:red;'><center><h1 style='color:white;'>Error User is not admin or not exists!!!</h1><h2 style='color:white'>Go back and try to to get valid admin</h2</center></body")


# ajax functions
# ajax function for deleting specific event booking.
@login_required
def ajax_delete_event_booking(request,id):
    if request.is_ajax():
        try:
            # get event booking object by received id
            booked_event = Event_booking.objects.filter(pk=id, user=request.user)
            # delete the instance
            booked_event.delete()
            # send back url to redirect from frontend
            redirect_url = "/user/my/bookings/"
            return JsonResponse({"success": True, 'redirect_url': redirect_url})
        except Exception as e:
            return JsonResponse({"success": False})
        return JsonResponse(data)


# ajax function for deleting specific service booking.
@login_required
def ajax_delete_service_booking(request,id):
    if request.is_ajax():
        try:
            # get service booking object by received id
            booked_service = Service_booking.objects.filter(pk=id, user=request.user)
            # delete the instance
            booked_service.delete()
            # send back url to redirect from frontend
            redirect_url = "/user/my/bookings/"
            return JsonResponse({"success": True, 'redirect_url': redirect_url})
        except Exception as e:
            return JsonResponse({"success": False})
        return JsonResponse(data)

# -----service
# ajax function for accepting or confirming service.
@login_required
def ajax_confirm_service_booking(request,service_id,requester_id):
    if request.is_ajax():
        try:
            # check if user is admin and owner of the service
            if Service.objects.filter(pk=service_id, user=request.user).exists():
                # get and set status
                if Booking_status.objects.filter(status="Confirmed").exists():
                    confirm_status = Booking_status.objects.get(status="Confirmed")
                else:
                    confirm_status = Booking_status.objects.create(status="Confirmed")
                    confirm_status.save()

                # get service booking object and set status
                booking = Service_booking.objects.get(service_id=service_id, user_id=requester_id)
                booking.status = confirm_status
                booking.service_approver = request.user
                booking.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False})
            
        except Exception as e:
            return JsonResponse({"success": False})
        return JsonResponse(data)


# ajax function for canceling service.
@login_required
def ajax_cancel_service_booking(request,service_id,requester_id):
    if request.is_ajax():
        try:
            # check if user is admin and owner of the service
            if Service.objects.filter(pk=service_id, user=request.user).exists():
                # get service booking object and delete object
                booking = Service_booking.objects.get(service_id=service_id, user_id=requester_id)
                booking.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False})
            
        except Exception as e:
            return JsonResponse({"success": False})
        return JsonResponse(data)


# -----events
# ajax function for accepting or confirming event.
@login_required
def ajax_confirm_event_booking(request,event_id,requester_id):
    if request.is_ajax():
        try:
            # check if user is admin and owner of the event
            if Event.objects.filter(pk=event_id, user=request.user).exists():
                # get and set status
                if Booking_status.objects.filter(status="Confirmed").exists():
                    confirm_status = Booking_status.objects.get(status="Confirmed")
                else:
                    confirm_status = Booking_status.objects.create(status="Confirmed")
                    confirm_status.save()

                # get event booking object and set status
                booking = Event_booking.objects.get(event_id=event_id, user_id=requester_id)
                booking.status = confirm_status
                booking.event_approver = request.user
                booking.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False})
            
        except Exception as e:
            return JsonResponse({"success": False})
        return JsonResponse(data)


# ajax function for canceling event.
@login_required
def ajax_cancel_event_booking(request,event_id,requester_id):
    if request.is_ajax():
        try:
            # check if user is admin and owner of the event
            if Event.objects.filter(pk=event_id, user=request.user).exists():
                # get event booking object and delete object
                booking = Event_booking.objects.get(event_id=event_id, user_id=requester_id)
                booking.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False})
            
        except Exception as e:
            return JsonResponse({"success": False})
        return JsonResponse(data)