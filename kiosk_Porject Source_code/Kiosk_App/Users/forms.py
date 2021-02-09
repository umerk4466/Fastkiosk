from django import forms
from django.contrib.auth.models import User
from .models import Student_data, Profile
from django.contrib.auth.forms import UserCreationForm

# form for admin signup
class Signup_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(Signup_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Email"

    # SIGNUP_USERS_TYPES = (
    #     ('Student', 'Student',),
    #     ('Admin', 'Admin',),
    # )
    # user_type = forms.ChoiceField(choices = SIGNUP_USERS_TYPES, required=True, label="Sign-up as :",)
        
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'username', 'password1', 'password2' ]



# # form for student signup
class Signup_Student_Form(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(Signup_Student_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"

    student_roll_no = forms.IntegerField(label="Student Roll Nummber :",)
    course_name = forms.CharField(max_length=255,  label="Student Course Name :")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'student_roll_no', 'course_name', 'username', 'password1', 'password2' ]


# form for profile
class User_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(User_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['email'].label = "Your Email"

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]


# form for profile
class Profile_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Profile_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['about_me'].label = "About you"
        # self.fields['student_roll_no'].required = True
        self.fields['country'].label = "My Country"
        self.fields['city'].label = "My City"
        self.fields['website'].label = "My Website"
        self.fields['image'].label = "Profile Image Link"
        self.fields['date_of_birth'].label = "Date Of Birth"
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'type': 'date'})

        # self.fields['cource_finish'].widget = forms.DateInput(attrs={'type': 'date'})
    
    class Meta:
        model = Profile
        fields = ['image', 'country', 'city', 'website', 'date_of_birth', 'about_me']


# form for student
class Student_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Student_Form, self).__init__(*args, **kwargs)
        # below changing on the fields of this form.
        self.fields['student_roll_no'].label = "Your Roll Number"
        self.fields['student_roll_no'].required = True
        self.fields['course_name'].label = "Course Name"
        self.fields['cource_finish'].label = "Course finish"
        self.fields['cource_finish'].widget = forms.DateInput(attrs={'type': 'date'})

    class Meta:
        model = Student_data
        fields = ['student_roll_no', 'course_name', 'cource_finish']












# class Student_Signup_Form(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(Student_Signup_Form, self).__init__(*args, **kwargs)
#         # below changing on the fields of this form.
#         self.fields['first_name'].label = "First Name"
#         self.fields['last_name'].label = "Last Name"
#         self.fields['student_no'].label = "Roll Number"

#     student_no = forms.IntegerField(required=True)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'student_no', 'username', 'password1', 'password2']
