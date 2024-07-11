from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UsermodelAdmin(BaseUserAdmin):
    
   

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'name','contact', 'is_admin','role','is_registered','is_deleted')
    list_filter = ('is_admin','role')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','contact',"image")}),
        ('Permissions', {'fields': ('is_admin','is_registered','is_deleted')}),
        ('Role', {'fields': ('role',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','contact', 'password1', 'password2','role'),
        }),
    )
    search_fields = ('email','contact')
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UsermodelAdmin)