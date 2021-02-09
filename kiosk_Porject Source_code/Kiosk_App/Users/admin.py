from django.contrib import admin
from .models import Profile, Role, Permission, Student_data


# user tables
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Student_data)




