from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='Users/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
    path('signup/admin/', views.signup, name='signup_admin'),
    path('signup/student/', views.signup_student, name='signup_student'),
    # ajax call pages
    path('ajax/change/student/data/', views.ajax_change_student_data, name='ajax_change_student_data'),


    # path('signup/student', views.student_signup, name='signup_student'),
]

