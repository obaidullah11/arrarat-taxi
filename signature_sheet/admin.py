from django.contrib import admin,messages
from django.utils.html import format_html
from .models import *

# Register your models here.
# class AssignPassengerTosignatureAdmin(admin.ModelAdmin):
#     list_display = ['get_driver_name', 'passenger', 'date_created']
#     list_filter = ['date_created']
#     search_fields = ['get_driver_name', 'passenger__name']

#     def get_driver_name(self, obj):
#         return obj.user.name

#     get_driver_name.short_description = 'Driver'

#     def save_model(self, request, obj, form, change):
#         # Check if there's an existing assignment for the same passenger and a different driver
#         existing_assignment = AssignPassengerTosignature_sheet1.objects.filter(
#             passenger=obj.passenger,
#             user__is_deleted=False,
#             user__is_registered=True
#         ).exclude(user=obj.user).first()

#         if existing_assignment:
#             message = "This passenger is already assigned to a different driver."
#             self.message_user(request, message, level=messages.WARNING)
#             return

#         super().save_model(request, obj, form, change)
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'user':
#             # Filter the list of passengers based on your criteria
#             kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
# class SignatureSheetAdmin(admin.ModelAdmin):
#     list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','display_image']
#     list_filter = ['date_created', 'driver__name', 'passenger_name__name']

#     def export_to_csv(self, request, queryset):
#         # Your export to CSV code for passengers here
#         pass

#     export_to_csv.short_description = "Export to CSV"

#     def export_driver_to_csv(self, request, queryset):
#         # Your export to CSV code for drivers here
#         pass

#     export_driver_to_csv.short_description = "Export Driver CSV"

#     actions = [export_to_csv, export_driver_to_csv]
#     def display_image(self, obj):
#         if obj.signature:
#             return format_html('<img src="{}" width="100" height="100" />', obj.signature.url)
#         else:
#             return ''

#     display_image.short_description = 'Signature Image'



#     def get_driver_name(self, obj):
#         return obj.driver.name

# admin.site.register(signature_sheet1, SignatureSheetAdmin)


@admin.register(SignatureReceipt)
class SignatureReceiptAdmin(admin.ModelAdmin):
    list_display = (
        'get_driver_name',
        # 'created_at'
        'date',
        'account_name',
        'start_time',
        'finish_time',
        'trip_explanation',
        'start_point',
        'drop_point',
        'taxi_no',
        'dc_no',
        'passenger_name',
        'fare_meter',
        'extras',
        'total',
        'display_image',
    )

    search_fields = ('passenger_name', 'account_name', 'date')

    list_filter = ('date', 'account_name')
    def get_driver_name(self, obj):
        return obj.Driver.name

    def display_image(self, obj):
        if obj.signature:
            return format_html('<img src="{}" width="100" height="100" />', obj.signature.url)
        else:
            return ''

    display_image.short_description = 'Signature'



# admin.site.register(AssignPassengerTosignature_sheet1, AssignPassengerTosignatureAdmin)