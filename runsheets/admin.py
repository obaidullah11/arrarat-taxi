from django.contrib import admin, messages
from .models import *
from django.http import HttpResponse
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from itertools import groupby
from import_export.admin import ExportActionMixin
from reportlab.platypus import KeepInFrame,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['name', 'Passenger_type', 'organization_name', 'invoice_number']
    list_filter = ['Passenger_type', 'organization_name']
    search_fields = ['name', 'invoice_number', 'organization_name']
class Runsheet1Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created']
    list_filter = ['date_created','driver__name','passenger_name__name']
    # list_filter = ['date_created','driver__name']
    # search_fields = ['passenger_name__name', 'driver__name']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_driver_name(self, obj):
        return obj.driver.name

    def get_actions(self, request):
        actions = super().get_actions(request)
        # print("actions ==+> ",actions)

        # Check if 'driver__name' filter has a selected value
        driver_filter_value = request.GET.get('driver__name')

        # Check if 'passenger__name' filter has a selected value
        passenger_filter_value = request.GET.get('passenger_name__name')

        if driver_filter_value and not passenger_filter_value:
            del actions['export_to_csv']
        elif passenger_filter_value and not driver_filter_value:
            del actions['export_driver_to_csv']
        elif not passenger_filter_value and not driver_filter_value:
            del actions['export_driver_to_csv']
            del actions['export_to_csv']

        # # If there's no 'driver__name' filter selected, restrict 'export_to_csv' action
        # if not driver_filter_value and 'export_to_csv' in actions:
        #     del actions['export_to_csv']

        # # If there's no 'passenger__name' filter selected, restrict 'export_passenger_csv' action
        # if not passenger_filter_value and 'export_passenger_csv' in actions:
        #     del actions['export_passenger_csv']

        return actions


    # def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        # Get a list of unique passengers from the queryset
        passengers = list(set(runsheet.passenger_name for runsheet in queryset))

        # Group queryset by date_created
        queryset = sorted(queryset, key=lambda x: x.date_created.date())
        grouped_data = groupby(queryset, key=lambda x: x.date_created.date())

        # Create a dictionary to hold the data in the desired format
        data_dict = {}
        for date, grouped_queryset in grouped_data:
            date_str = date.strftime('%d/%m/%Y')
            data_dict[date_str] = {
                'Morning': {passenger: 0 for passenger in passengers},
                'Afternoon': {passenger: 0 for passenger in passengers}
            }

            for runsheet in grouped_queryset:
                passenger_name = runsheet.passenger_name
                data_dict[date_str]['Morning'][passenger_name] = runsheet.Morning_price or 0
                data_dict[date_str]['Afternoon'][passenger_name] = runsheet.Evening_price or 0
            print("fdgdgfdddddddddddddf",data_dict)

        # Create a CSV writer
        csv_writer = csv.writer(response)

        # Write the header row
        header_row = ['Date']  + [passenger for passenger in passengers for _ in range(2)]
        csv_writer.writerow(header_row)

        # Write the subheader row
        subheader_row =  [''] + ['Morning', 'Afternoon'] * len(passengers)
        csv_writer.writerow(subheader_row)

        # Write the data rows
        for date_str, data in data_dict.items():
            data_row = [date_str]
            for time_slot in ['Morning', 'Afternoon']:

                for passenger in passengers:

                    data_row.extend([data[time_slot][passenger]])
                    print("fdgdgfdf",passenger)
            print("fdgdgfdf",data_row)
            csv_writer.writerow(data_row)
        # sum_row = ['<b>SUM</b>']


        csv_writer.writerow([])
        # Write the "SUM" row
        sum_row = ['SUM']
        for time_slot in ['Morning', 'Afternoon']:
            for passenger in passengers:
                total = sum(data[time_slot][passenger] for data in data_dict.values())
                sum_row.extend([total])
        csv_writer.writerow(sum_row)


        csv_writer.writerow([])
        # Write the "TOTAL" row
        total_row = ['TOTAL']
        for passenger in passengers:
            morning_total = sum(data['Morning'][passenger] for data in data_dict.values())
            evening_total = sum(data['Afternoon'][passenger] for data in data_dict.values())
            total_row.extend([ morning_total,  evening_total])
        csv_writer.writerow(total_row)

        return response




    # def export_driver_to_csv(self, request, queryset):
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="drivers.csv"'

    #     drivers = list(set(runsheet.driver.name for runsheet in queryset))

    #     queryset = sorted(queryset, key=lambda x: x.date_created.date())
    #     grouped_data = groupby(queryset, key=lambda x: x.date_created.date())

    #     data_dict = {}
    #     for date, grouped_queryset in grouped_data:
    #         date_str = date.strftime('%d/%m/%Y')
    #         data_dict[date_str] = {
    #             'Morning': {driver: 0 for driver in drivers},
    #             'Afternoon': {driver: 0 for driver in drivers}
    #         }

    #         for runsheet in grouped_queryset:
    #             driver_name = runsheet.driver.name
    #             data_dict[date_str]['Morning'][driver_name] = runsheet.Morning_price or 0
    #             data_dict[date_str]['Afternoon'][driver_name] = runsheet.Evening_price or 0

    #     print("Data Dictionary:", data_dict)

    #     csv_writer = csv.writer(response)

    #     header_row = ['Date']
    #     for driver in drivers:
    #         header_row.extend([driver, driver])
    #     print("Header Row:", header_row)
    #     csv_writer.writerow(header_row)

    #     subheader_row = [''] + ['Morning', 'Afternoon'] * len(drivers)
    #     print("Subheader Row:", subheader_row)
    #     csv_writer.writerow(subheader_row)

    #     for date_str, data in data_dict.items():
    #         data_row = [date_str]
    #         for time_slot in ['Morning', 'Afternoon']:
    #             for driver in drivers:
    #                 data_row.extend([data[time_slot][driver]])
    #         print("Data Row:", data_row)
    #         csv_writer.writerow(data_row)





    #     sum_row = ['SUM']
    #     for time_slot in ['Morning', 'Afternoon']:
    #         for driver in drivers:
    #             total = sum(data[time_slot][driver] for data in data_dict.values())
    #             sum_row.extend([total])
    #     print("Sum Row:", sum_row)
    #     csv_writer.writerow(sum_row)
    #     csv_writer.writerow([])

    # # Adding static text
    #     static_text_row = ['']
    #     static_text = "This is a static text line."
    #     static_text_row.append(static_text)
    #     csv_writer.writerow(static_text_row)
    #     total_row = ['TOTAL']
    #     for driver in drivers:
    #         morning_total = sum(data['Morning'][driver] for data in data_dict.values())
    #         evening_total = sum(data['Afternoon'][driver] for data in data_dict.values())
    #         total_row.extend([morning_total, evening_total])
    #     print("Total Row:", total_row)
    #     csv_writer.writerow(total_row)

    #     return response

    # export_driver_to_csv.short_description = "Export Driver CSV"

    # actions = [export_driver_to_csv]

    def export_driver_to_csv(self, request, queryset):
        name = ''
        if len(queryset)>0:
            name = queryset[0].driver.name
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{name}_runsheet1_driver.csv"'

        drivers = list(set(runsheet.passenger_name.name for runsheet in queryset))
    # Get unique passenger names

        queryset = sorted(queryset, key=lambda x: x.date_created.date())
        grouped_data = groupby(queryset, key=lambda x: x.date_created.date())

        data_dict = {}
        for date, grouped_queryset in grouped_data:
            date_str = date.strftime('%d/%m/%Y')
            day_name = date.strftime('%A')  # Get the full day name
            formatted_date =  f'{day_name}, {date_str}'

            # Combine day name and date
            # Initialize the Morning and Afternoon keys if not present
            if formatted_date not in data_dict:
                data_dict[formatted_date] = {
                    'Morning': {},
                    'Afternoon': {}
                }

            for runsheet in grouped_queryset:
                driver_name = runsheet.passenger_name.name

                # Initialize driver's entry for both Morning and Afternoon
                if driver_name not in data_dict[formatted_date]['Morning']:
                    data_dict[formatted_date]['Morning'][driver_name] = 0
                if driver_name not in data_dict[formatted_date]['Afternoon']:
                    data_dict[formatted_date]['Afternoon'][driver_name] = 0

                data_dict[formatted_date]['Morning'][driver_name] = runsheet.Morning_price or 0
                data_dict[formatted_date]['Afternoon'][driver_name] = runsheet.Evening_price or 0

        csv_writer = csv.writer(response)

        header_row = ['Date']
        for driver in drivers:
            header_row.extend([f"{driver} (Morning)", f"{driver} (Afternoon)"])
        csv_writer.writerow(header_row)

        for date_str, data in data_dict.items():
            data_row = [date_str]
            for driver in drivers:
                morning_data = data.get('Morning', {}).get(driver, 0)
                evening_data = data.get('Afternoon', {}).get(driver, 0)
                data_row.extend([morning_data, evening_data])
            csv_writer.writerow(data_row)

            # Calculate and write the sum of the week's records
            # week_sum_row = ['WEEK SUM']
            # for driver in drivers:
            #     week_sum = sum(data.get('Morning', {}).get(driver, 0) + data.get('Afternoon', {}).get(driver, 0) for week_date, week_data in data_dict.items() if driver in week_data.get('Morning', {}) and driver in week_data.get('Afternoon', {}))
            #     week_sum_row.extend([week_sum, ''])  # Add an empty string for space
            # csv_writer.writerow(week_sum_row)

            # Adding a blank line after each date's record
            csv_writer.writerow([])

        total_row = ['TOTAL']
        morning_total = sum(sum(data['Morning'].get(driver, 0) for data in data_dict.values()) for driver in drivers)
        evening_total = sum(sum(data['Afternoon'].get(driver, 0) for data in data_dict.values()) for driver in drivers)
        total_row.extend([morning_total, evening_total])
        csv_writer.writerow(total_row)
        total_row = ['TOTAL']
        # Rest of your code...

        return response

    def export_to_csv(self, request, queryset):
        name = ''
        if len(queryset)>0:
            name = queryset[0].passenger_name.name
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{name}_runsheet1_passenger.csv"'

        drivers = list(set(runsheet.driver.name for runsheet in queryset))
    # Get unique passenger names

        queryset = sorted(queryset, key=lambda x: x.date_created.date())
        grouped_data = groupby(queryset, key=lambda x: x.date_created.date())

        data_dict = {}
        for date, grouped_queryset in grouped_data:
            date_str = date.strftime('%d/%m/%Y')
            day_name = date.strftime('%A')  # Get the full day name
            formatted_date =  f'{day_name}, {date_str}'

            # Combine day name and date
            # Initialize the Morning and Afternoon keys if not present
            if formatted_date not in data_dict:
                data_dict[formatted_date] = {
                    'Morning': {},
                    'Afternoon': {}
                }

            for runsheet in grouped_queryset:
                driver_name = runsheet.driver.name

                # Initialize driver's entry for both Morning and Afternoon
                if driver_name not in data_dict[formatted_date]['Morning']:
                    data_dict[formatted_date]['Morning'][driver_name] = 0
                if driver_name not in data_dict[formatted_date]['Afternoon']:
                    data_dict[formatted_date]['Afternoon'][driver_name] = 0

                data_dict[formatted_date]['Morning'][driver_name] = runsheet.Morning_price or 0
                data_dict[formatted_date]['Afternoon'][driver_name] = runsheet.Evening_price or 0

        csv_writer = csv.writer(response)

        header_row = ['Date']
        for driver in drivers:
            header_row.extend([f"{driver} (Morning)", f"{driver} (Afternoon)"])
        csv_writer.writerow(header_row)

        for date_str, data in data_dict.items():
            data_row = [date_str]
            for driver in drivers:
                morning_data = data.get('Morning', {}).get(driver, 0)
                evening_data = data.get('Afternoon', {}).get(driver, 0)
                data_row.extend([morning_data, evening_data])
            csv_writer.writerow(data_row)

            # Calculate and write the sum of the week's records








        total_row = ['TOTAL']
        morning_total = sum(sum(data['Morning'].get(driver, 0) for data in data_dict.values()) for driver in drivers)
        evening_total = sum(sum(data['Afternoon'].get(driver, 0) for data in data_dict.values()) for driver in drivers)
        total_row.extend([morning_total, evening_total])
        csv_writer.writerow(total_row)
        total_row = ['TOTAL']
        # Rest of your code...

        return response

    actions = [export_to_csv,export_driver_to_csv]
    # def export_driver_to_csv(self, request, queryset):
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="drivers.csv"'

    #     drivers = list(set(runsheet.driver.name for runsheet in queryset))

    #     queryset = sorted(queryset, key=lambda x: x.date_created.date())
    #     grouped_data = groupby(queryset, key=lambda x: x.date_created.date())

    #     data_dict = {}
    #     for date, grouped_queryset in grouped_data:
    #         date_str = date.strftime('%d/%m/%Y')
    #         day_name = date.strftime('%A')  # Get the full day name
    #         formatted_date =  f'{day_name}, {date_str}'

    #          # Combine day name and date
    #           #   Combine day name and date
    #         print("formatted_date:", formatted_date)
    #         # Initialize the Morning and Afternoon keys if not present
    #         if formatted_date not in data_dict:
    #             data_dict[formatted_date] = {
    #                 'Morning': {},
    #                 'Afternoon': {}
    #             }

    #         for runsheet in grouped_queryset:
    #             driver_name = runsheet.driver.name

    #             # Initialize driver's entry for both Morning and Afternoon
    #             if driver_name not in data_dict[formatted_date]['Morning']:
    #                 data_dict[formatted_date]['Morning'][driver_name] = 0
    #             if driver_name not in data_dict[formatted_date]['Afternoon']:
    #                 data_dict[formatted_date]['Afternoon'][driver_name] = 0

    #             data_dict[formatted_date]['Morning'][driver_name] = runsheet.Morning_price or 0
    #             data_dict[formatted_date]['Afternoon'][driver_name] = runsheet.Evening_price or 0

    #     csv_writer = csv.writer(response)

    #     header_row = ['Date']
    #     for driver in drivers:
    #         header_row.extend([driver, driver])
    #     csv_writer.writerow(header_row)

    #     subheader_row = [''] + ['Morning', 'Afternoon'] * len(drivers)
    #     csv_writer.writerow(subheader_row)

    #     for date_str, data in data_dict.items():
    #         data_row = [date_str]
    #         for time_slot in ['Morning', 'Afternoon']:
    #             for driver in drivers:
    #                  morning_data = data.get(time_slot, {}).get(driver, 0)
    #                  data_row.extend([morning_data])
    #                 # data_row.extend([data[time_slot][driver]])
    #         csv_writer.writerow(data_row)
    #         print("data_dict:", data_dict)
    #         # Adding a blank line after each week's record
    #         csv_writer.writerow([])

    #         # Adding static text after each week's record
    #         static_text_row = ['']
    #         static_text = f" {date_str}"
    #         static_text_row.append(static_text)
    #         csv_writer.writerow(static_text_row)

    #         # Calculate and write the sum of the week's records
    #         week_sum_row = ['WEEK SUM']
    #         for driver in drivers:
    #             week_sum = sum(data['Morning'][driver] + data['Afternoon'][driver] for week_date, week_data in data_dict.items() if driver in week_data['Morning'] and driver in week_data['Afternoon'] and week_date == date_str)
    #             week_sum_row.extend([week_sum])
    #         csv_writer.writerow(week_sum_row)

    #         # Print each week's sum
    #         print(f"Week {date_str} Sum:", week_sum_row)

    #     # Adding a blank line before the "TOTAL" row
    #     csv_writer.writerow([])

    #     total_row = ['TOTAL']
    #     for driver in drivers:
    #         morning_total = sum(data['Morning'][driver] for data in data_dict.values())
    #         evening_total = sum(data['Afternoon'][driver] for data in data_dict.values())
    #         total_row.extend([morning_total, evening_total])
    #     csv_writer.writerow(total_row)

    #     return response

    export_driver_to_csv.short_description = "Export Driver CSV"
    export_to_csv.short_description = "Export to CSV"

    # actions = [export_driver_to_csv]





# admin.site.register(Runsheet1, RunsheetAdmin)

@admin.register(Runsheet2)
class Runsheet2Admin(admin.ModelAdmin):
    list_display = ('passenger_name', 'Morning_price', 'Evening_price', 'driver', 'date_created')

@admin.register(Runsheet3)
class Runsheet3Admin(admin.ModelAdmin):
    list_display = ('passenger_name', 'Morning_price', 'Evening_price', 'driver', 'date_created')

@admin.register(Runsheet4)
class Runsheet4Admin(admin.ModelAdmin):
    list_display = ('passenger_name', 'Morning_price', 'Evening_price', 'driver', 'date_created')

@admin.register(Runsheet5)
class Runsheet5Admin(admin.ModelAdmin):
    list_display = ('passenger_name', 'Morning_price', 'Evening_price', 'driver', 'date_created')
@admin.register(Runsheet8)
class Runsheet8Admin(admin.ModelAdmin):
    list_display = ('passenger_name', 'Morning_price', 'Evening_price', 'driver', 'date_created')

# Register the model admin








# get_driver_name.short_description = 'Driver Name'


# @admin.register(Passenger)
# class PassengerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'age', 'description', 'user']
#     list_filter = ['user']
# @admin.register(ShiftTime)
# class ShiftTimeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)
# @admin.register(Runsheet1)
# class Runsheet1Admin(admin.ModelAdmin):
#     list_display = ['id', 'passenger_name', 'shift_name', 'price', 'driver']
#     list_filter = ['shift_name', 'driver']
#     search_fields = ['passenger_name', 'shift_name']

# admin.site.register(Runsheet1, Runsheet1Admin)
# class AssignPassengerToRunsheet1Admin(admin.ModelAdmin):
#     list_display = ['get_driver_name', 'passenger', 'date_created']
#     list_filter = ['date_created']
#     search_fields = ['user__username', 'passenger__name']

#     def get_driver_name(self, obj):
#         return obj.user.name

#     get_driver_name.short_description = 'Driver'

#     def save_model(self, request, obj, form, change):
#         existing_assignment = AssignPassengerToRunsheet1.objects.filter(user=obj.user, passenger=obj.passenger).first()

#         if existing_assignment and (not change or obj.id != existing_assignment.id):
#             message = "A passenger assignment for the same user already exists."
#             self.message_user(request, message, level=messages.WARNING)
#             return

#         super().save_model(request, obj, form, change)

class AssignPassengerToRunsheet1Admin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['get_driver_name', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet1.objects.filter(
    #         passenger=obj.passenger,
    #         user__is_deleted=False,
    #         user__is_registered=True
    #     ).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

    #     super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class AssignPassengerToRunsheet2Admin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user__username', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet2.objects.filter(passenger=obj.passenger).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

    #     super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)




class AssignPassengerToRunsheet3Admin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user__username', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet3.objects.filter(passenger=obj.passenger).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

    #     super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class AssignPassengerToRunsheet4Admin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user__username', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet4.objects.filter(passenger=obj.passenger).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

    #     super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class AssignPassengerToRunsheet5Admin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user__username', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet5.objects.filter(passenger=obj.passenger).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

    #     super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AssignPassengerToRunsheet6Admin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user__username', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet6.objects.filter(passenger=obj.passenger).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

    #     super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class AssignPassengerToRunsheet7Admin(admin.ModelAdmin):
    list_display = ['get_driver_name', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user__username', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet7.objects.filter(passenger=obj.passenger).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

        # super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class AssignPassengerToRunsheet8Admin(admin.ModelAdmin):
    list_display = ['user', 'passenger', 'date_created']
    list_filter = ['date_created']
    search_fields = ['user', 'passenger__name']

    def get_driver_name(self, obj):
        return obj.user.name

    get_driver_name.short_description = 'Driver'

    # def save_model(self, request, obj, form, change):
    #     # Check if there's an existing assignment for the same passenger and a different driver
    #     existing_assignment = AssignPassengerToRunsheet8.objects.filter(passenger=obj.passenger).exclude(user=obj.user).first()

    #     if existing_assignment:
    #         message = "This passenger is already assigned to a different driver."
    #         self.message_user(request, message, level=messages.WARNING)
    #         return

    #     super().save_model(request, obj, form, change)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Filter the list of passengers based on your criteria
            kwargs['queryset'] = User.objects.filter(is_deleted=False,is_registered=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
class HelpAndDisputeAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'get_driver_name', 'created_at')

    def get_driver_name(self, obj):
        return obj.driver.name  # Assuming your Driver model has a 'name' field
    get_driver_name.short_description = 'Driver Name'

admin.site.register(HelpAndDispute, HelpAndDisputeAdmin)

admin.site.register(AssignPassengerToRunsheet1, AssignPassengerToRunsheet1Admin)
admin.site.register(AssignPassengerToRunsheet2, AssignPassengerToRunsheet2Admin)
admin.site.register(AssignPassengerToRunsheet3, AssignPassengerToRunsheet3Admin)
admin.site.register(AssignPassengerToRunsheet4, AssignPassengerToRunsheet4Admin)
admin.site.register(AssignPassengerToRunsheet5, AssignPassengerToRunsheet5Admin)
admin.site.register(AssignPassengerToRunsheet6, AssignPassengerToRunsheet6Admin)
admin.site.register(AssignPassengerToRunsheet7, AssignPassengerToRunsheet7Admin)
admin.site.register(AssignPassengerToRunsheet8, AssignPassengerToRunsheet8Admin)
admin.site.register(Runsheet1,Runsheet1Admin)
# admin.site.register(Runsheet1Proxy,Runsheet1ProxyAdmin)

admin.site.register(Passenger, PassengerAdmin)