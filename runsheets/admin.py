from django.contrib import admin, messages
from .models import *
from django.utils.html import format_html
from django.utils.translation import gettext_lazy  as _
from datetime import date
from django.http import HttpResponse
import csv
from collections import defaultdict
from django.urls import path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.utils.text import slugify
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from itertools import groupby
from import_export.admin import ExportActionMixin
from reportlab.platypus import KeepInFrame,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
class MonthListFilter(admin.SimpleListFilter):
    title = _('Month')  # Displayed filter title
    parameter_name = 'month'  # URL parameter name for the filter

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value
        for the option that will appear in the URL query. The second element is the
        human-readable name for the option that will appear in the right sidebar.
        """
        return (
            ('1', _('January')),
            ('2', _('February')),
            ('3', _('March')),
            ('4', _('April')),
            ('5', _('May')),
            ('6', _('June')),
            ('7', _('July')),
            ('8', _('August')),
            ('9', _('September')),
            ('10', _('October')),
            ('11', _('November')),
            ('12', _('December')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query string.
        """
        if self.value():
            # Filter queryset based on selected month
            return queryset.filter(date_created__month=self.value())
        return queryset
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['name', 'Passenger_type', 'organization_name', 'invoice_number']
    list_filter = ['Passenger_type', 'organization_name']
    search_fields = ['name', 'invoice_number', 'organization_name']
class Runsheet1Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name','date_created']
    search_fields = ['passenger_name__name', 'driver__name']
    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    # def export_summary_csv(self, request, queryset):
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="summary_passenger_totals.csv"'

    #     # Group by passenger name and calculate totals
    #     passengers = list(set(runsheet.passenger_name for runsheet in queryset))
    #     passenger_totals = {passenger: {'Morning': 0, 'Afternoon': 0, 'Total': 0} for passenger in passengers}

    #     for runsheet in queryset:
    #         passenger_name = runsheet.passenger_name
    #         passenger_totals[passenger_name]['Morning'] += runsheet.Morning_price or 0
    #         passenger_totals[passenger_name]['Afternoon'] += runsheet.Evening_price or 0
    #         passenger_totals[passenger_name]['Total'] += (runsheet.Morning_price or 0) + (runsheet.Evening_price or 0)

    #     csv_writer = csv.writer(response)
    #     csv_writer.writerow(['Passenger', 'Morning Total', 'Afternoon Total', 'Total'])

    #     for passenger, totals in passenger_totals.items():
    #         csv_writer.writerow([
    #             passenger.name,
    #             totals['Morning'],
    #             totals['Afternoon'],
    #             totals['Total']
    #         ])

    #     return response
    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"

# admin.site.register(Runsheet1, RunsheetAdmin)

@admin.register(Runsheet2)
class Runsheet2Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name']
    search_fields = ['passenger_name__name', 'driver__name']

    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"
@admin.register(Runsheet3)
class Runsheet3Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name']
    search_fields = ['passenger_name__name', 'driver__name']

    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"
@admin.register(Runsheet4)
class Runsheet4Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name']
    search_fields = ['passenger_name__name', 'driver__name']

    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"
@admin.register(Runsheet5)
class Runsheet5Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name']
    search_fields = ['passenger_name__name', 'driver__name']

    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"
@admin.register(Runsheet6)
class Runsheet6Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name']
    search_fields = ['passenger_name__name', 'driver__name']

    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"
@admin.register(Runsheet7)
class Runsheet7Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name']
    search_fields = ['passenger_name__name', 'driver__name']

    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"
@admin.register(Runsheet8)
class Runsheet8Admin(admin.ModelAdmin):
    list_display = ['passenger_name', 'Morning_price', 'Evening_price', 'get_driver_name', 'date_created','type']
    list_filter = ['driver__name', 'passenger_name__name']
    search_fields = ['passenger_name__name', 'driver__name']

    def get_list_filter(self, request):
        """
        Returns updated list filter including custom date filter.
        """
        return [MonthListFilter] + list(self.list_filter)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'driver':
            kwargs['queryset'] = User.objects.filter(is_deleted=False, is_registered=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_driver_name(self, obj):
        return obj.driver.name

    def export_summary_csv(self, request, queryset):
    # Check if the queryset is empty
        if not queryset.exists():
            driver_name = "unknown_driver"
        else:
            driver_name = queryset[0].driver.name if queryset[0].driver else "unknown_driver"

        driver_name_slug = slugify(driver_name)  # Create a slug to ensure the filename is URL-safe

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="summary_passenger_totals_{driver_name_slug}.csv"'

        # Initialize dictionaries to store data
        passenger_days = defaultdict(lambda: defaultdict(float))
        monthly_totals = defaultdict(float)

        # Process each runsheet entry
        for runsheet in queryset:
            passenger = runsheet.passenger_name  # This is a Passenger object
            passenger_name = str(passenger)
            print(f"Processing passenger: {passenger_name}")

            # Get the string representation of the Passenger object (e.g., passenger name)
            date = runsheet.date_created.strftime("%d/%m/%Y")

            morning_total = float(runsheet.Morning_price or 0)
            afternoon_total = float(runsheet.Evening_price or 0)
            daily_total = morning_total + afternoon_total

            passenger_days[passenger_name][date] += daily_total
            monthly_totals[passenger_name] += daily_total

        # Write CSV header
        csv_writer = csv.writer(response)
        # Add driver's name at the top of the CSV file
        csv_writer.writerow(['Driver:', driver_name])
        csv_writer.writerow([])  # Add an empty row for separation

        # Use a list of sorted passenger names for the header
        sorted_passenger_names = sorted(passenger_days.keys())
        header = ['Date'] + sorted_passenger_names
        csv_writer.writerow(header)

        # Write daily totals
        for date in sorted({date for dates in passenger_days.values() for date in dates}):
            row = [date]
            for passenger_name in sorted_passenger_names:
                row.append(f"{passenger_days[passenger_name][date]:.2f}")
            csv_writer.writerow(row)

        # Write monthly totals
        total_row = ['TOTAL']
        for passenger_name in sorted_passenger_names:
            total_row.append(f"{monthly_totals[passenger_name]:.2f}")
        csv_writer.writerow(total_row)

        return response

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="runsheets.csv"'

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Passenger Name', 'Morning Price', 'Evening Price', 'Driver Name', 'Date Created'])

        for runsheet in queryset:
            csv_writer.writerow([
                runsheet.passenger_name.name,
                runsheet.Morning_price,
                runsheet.Evening_price,
                runsheet.driver.name,
                runsheet.date_created
            ])

        return response

    def export_driver_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="driver_summary.csv"'

        drivers = list(set(runsheet.driver for runsheet in queryset))
        driver_totals = {driver: {'Morning': 0, 'Afternoon': 0} for driver in drivers}

        for runsheet in queryset:
            driver = runsheet.driver
            driver_totals[driver]['Morning'] += runsheet.Morning_price or 0
            driver_totals[driver]['Afternoon'] += runsheet.Evening_price or 0

        csv_writer = csv.writer(response)
        csv_writer.writerow(['Driver', 'Morning Total', 'Afternoon Total'])

        for driver, totals in driver_totals.items():
            csv_writer.writerow([driver.name, totals['Morning'], totals['Afternoon']])

        return response

    actions = [export_summary_csv, export_to_csv, export_driver_to_csv]
    export_summary_csv.short_description = "Export Summary CSV"
    export_to_csv.short_description = "Export to CSV"
    export_driver_to_csv.short_description = "Export Driver to CSV"
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
# admin.site.register(Runsheet1, Runsheet1Admin)
# admin.site.register(Runsheet1Proxy,Runsheet1ProxyAdmin)

admin.site.register(Passenger, PassengerAdmin)