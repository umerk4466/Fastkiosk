from django import forms
from django.contrib.auth.models import User
from .models import Event, Service,Category



# create event form
# Event_Form
class Event_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Event_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['title'].label = "Title of the event"
        self.fields['description'].label = "Add event Description"
        self.fields['image_url'].label = "Image url for the event banner"
        self.fields['event_date'].label = "Event will be on? "
        self.fields['event_start_time'].label = "What time event will start"
        self.fields['event_finish_time'].label = "What time event will finish"
        self.fields['event_address'].label = "Event's exact address"
        self.fields['event_city'].label = "City of this event"

        self.fields['event_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['event_start_time'].widget = forms.DateInput(attrs={'type': 'time'})
        self.fields['event_finish_time'].widget = forms.DateInput(attrs={'type': 'time'})

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date','event_start_time','event_finish_time', 'image_url', 'event_address','event_city', ]


# Service_Form
class Service_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Service_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['category'].label = "Select category of the service or add new"
        self.fields['name'].label = "Title or Name of service"
        self.fields['description'].label = "Service's desciption"
        self.fields['service_city'].label = "Service's Place/City"
        self.fields['image_url'].label = "Image url for the service"

    class Meta:
        model = Service
        fields = ['category' ,'name', 'description', 'service_city','image_url',]

# Category_Form
class Category_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Category_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['name'].label = "Category's name"
        self.fields['description'].label = "Category's desciption"

    class Meta:
        model = Category
        fields = ['name' ,'description',]
