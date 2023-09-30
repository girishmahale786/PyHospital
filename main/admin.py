from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from main.models import Appointment, Employee, Post
from django.contrib import admin

# Register your models here.


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Post)
admin.site.register(Appointment)
