from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.
admin.site.register(Profile)

##########################################################################################################
#Mix profile info and user info
class ProfileInLine(admin.StackedInline):
    model = Profile

#Extend the user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'email', 'first_name', 'last_name', 'email']
    inlines = [ProfileInLine]
# Unregister the Old way
admin.site.unregister(User)
#Re-register the New Way
admin.site.register(User, UserAdmin)

##########################################################################################################