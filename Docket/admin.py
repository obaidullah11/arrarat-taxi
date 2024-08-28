# from django.contrib import admin
# from .models import dockets
# from django.utils.translation import gettext_lazy as _
# from django.http import HttpResponse
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter, landscape
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
# from reportlab.lib.styles import ParagraphStyle
# from django.utils.html import format_html
# class MonthListFilter(admin.SimpleListFilter):
#     title = _('Month')  # Displayed filter title
#     parameter_name = 'month'  # URL parameter name for the filter

#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each tuple is the coded value
#         for the option that will appear in the URL query. The second element is the
#         human-readable name for the option that will appear in the right sidebar.
#         """
#         return (
#             ('1', _('January')),
#             ('2', _('February')),
#             ('3', _('March')),
#             ('4', _('April')),
#             ('5', _('May')),
#             ('6', _('June')),
#             ('7', _('July')),
#             ('8', _('August')),
#             ('9', _('September')),
#             ('10', _('October')),
#             ('11', _('November')),
#             ('12', _('December')),
#         )

#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value provided in the query string.
#         """
#         if self.value():
#             # Filter queryset based on selected month
#             return queryset.filter(created_at__month=self.value())
#         return queryset
# @admin.register(dockets)
# class SignatureReceiptAdmin(admin.ModelAdmin):
#     list_display = (
#         'date',
#         'docket_id',
#         'get_driver_name',
#         'account_name',
#         'start_time',
#         'finish_time',
#         'trip_explanation',
#         'start_point',
#         'drop_point',
#         'taxi_no',
#         'dc_no',
#         'passenger_name',

#         'total',
#         'signature',
#     )

#     search_fields = ('passenger', 'account_name', 'date')
#     list_filter = (MonthListFilter, 'passenger_name', 'Driver__name')

#     def get_driver_name(self, obj):
#         return obj.Driver.name
#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         # Check if 'passenger_name__name' filter has a selected value
#         passenger_filter_value = request.GET.get('passenger_name')

#         if not passenger_filter_value:
#             # If the filter is not active, remove the custom action
#             del actions['generate_pdf_for_selected_passenger']

#         return actions
#     def generate_pdf_for_selected_passenger(self, request, queryset):
#         if queryset:
#             passenger_name = queryset.first().passenger_name  # Assuming passenger name is the same for all selected records

#             # Create an HttpResponse object with PDF content
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="{passenger_name}_records.pdf"'

#             # Create a PDF document
#             doc = SimpleDocTemplate(response, pagesize=landscape(letter))
#             elements = []

#             # Define the table data
#             data = [
#                 ['Date', 'Docket\nID', 'Account\nName', 'Start\nTime', 'Finish\nTime', 'Start\nPoint', 'Drop\nPoint', 'Passenger\nName', 'Total', 'Signature'],
#             ]

#             # Define a custom paragraph style
#             custom_style = ParagraphStyle(
#                 name='CustomNormal',
#                 fontSize=8,
#                 alignment=1,
#             )

#             for record in queryset:
#                 # Add a column for the signature image
#                 signature_image = Image(record.signature.path, width=50, height=50)

#                 # Create paragraph objects with the custom style for text cells, handling None values
#                 date_paragraph = Paragraph(record.date.strftime('%Y-%m-%d') if record.date else '', custom_style)
#                 docket_id_paragraph = Paragraph(record.docket_id if record.docket_id else '', custom_style)
#                 account_name_paragraph = Paragraph(record.account_name if record.account_name else '', custom_style)
#                 start_time_paragraph = Paragraph(str(record.start_time) if record.start_time else '', custom_style)
#                 finish_time_paragraph = Paragraph(str(record.finish_time) if record.finish_time else '', custom_style)
#                 start_point_paragraph = Paragraph(record.start_point if record.start_point else '', custom_style)
#                 drop_point_paragraph = Paragraph(record.drop_point if record.drop_point else '', custom_style)
#                 passenger_name_paragraph = Paragraph(record.passenger_name if record.passenger_name else '', custom_style)
#                 total_paragraph = Paragraph(str(record.total) if record.total else '', custom_style)

#                 data.append([
#                     date_paragraph,
#                     docket_id_paragraph,
#                     account_name_paragraph,
#                     start_time_paragraph,
#                     finish_time_paragraph,
#                     start_point_paragraph,
#                     drop_point_paragraph,
#                     passenger_name_paragraph,
#                     total_paragraph,
#                     signature_image,  # Add the signature image to the table
#                 ])

#             # Define column widths and row heights for responsiveness
#             col_widths = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 40, 40, 100]
#             row_heights = [80] * len(data)

#             # Create a table
#             table = Table(data, colWidths=col_widths, rowHeights=row_heights)
#             table.setStyle(TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ]))

#             elements.append(table)
#             doc.build(elements)

#             return response


#     generate_pdf_for_selected_passenger.short_description = "Generate PDF for Selected Passenger"


#       # Only superusers can access the action

#     actions = [generate_pdf_for_selected_passenger]
from django.contrib import admin
from .models import dockets
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import ParagraphStyle

class MonthListFilter(admin.SimpleListFilter):
    title = _('Month')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
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
        if self.value():
            return queryset.filter(created_at__month=self.value())
        return queryset

@admin.register(dockets)
class SignatureReceiptAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'docket_id',
        'get_driver_name',
        'account_name',
        'start_time',
        'finish_time',
        'trip_explanation',
        'start_point',
        'drop_point',
        'taxi_no',
        'dc_no',
        'passenger_name',
        'total',
        'signature',
    )

    search_fields = ('passenger', 'account_name', 'date')
    list_filter = (MonthListFilter, 'passenger_name', 'Driver__name')

    def get_driver_name(self, obj):
        return obj.Driver.name

    def generate_pdf_for_selected_passenger(self, request, queryset):
        return self.generate_pdf(queryset, "selected_passenger_records")

    def generate_pdf_for_all_records(self, request, queryset=None):
        queryset = dockets.objects.all()  # Get all records if queryset is not provided
        return self.generate_pdf(queryset, "all_passenger_records")

    def generate_pdf(self, queryset, filename_prefix):
        if queryset.exists():
            # Create an HttpResponse object with PDF content
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename_prefix}.pdf"'

            # Create a PDF document
            doc = SimpleDocTemplate(response, pagesize=landscape(letter))
            elements = []

            # Define the table data
            data = [
                ['Date', 'Docket\nID', 'Account\nName', 'Start\nTime', 'Finish\nTime', 'Start\nPoint', 'Drop\nPoint', 'Passenger\nName', 'Total', 'Signature'],
            ]

            # Define a custom paragraph style
            custom_style = ParagraphStyle(
                name='CustomNormal',
                fontSize=8,
                alignment=1,
            )

            for record in queryset:
                signature_image = Image(record.signature.path, width=50, height=50)

                date_paragraph = Paragraph(record.date.strftime('%Y-%m-%d') if record.date else '', custom_style)
                docket_id_paragraph = Paragraph(record.docket_id if record.docket_id else '', custom_style)
                account_name_paragraph = Paragraph(record.account_name if record.account_name else '', custom_style)
                start_time_paragraph = Paragraph(str(record.start_time) if record.start_time else '', custom_style)
                finish_time_paragraph = Paragraph(str(record.finish_time) if record.finish_time else '', custom_style)
                start_point_paragraph = Paragraph(record.start_point if record.start_point else '', custom_style)
                drop_point_paragraph = Paragraph(record.drop_point if record.drop_point else '', custom_style)
                passenger_name_paragraph = Paragraph(record.passenger_name if record.passenger_name else '', custom_style)
                total_paragraph = Paragraph(str(record.total) if record.total else '', custom_style)

                data.append([
                    date_paragraph,
                    docket_id_paragraph,
                    account_name_paragraph,
                    start_time_paragraph,
                    finish_time_paragraph,
                    start_point_paragraph,
                    drop_point_paragraph,
                    passenger_name_paragraph,
                    total_paragraph,
                    signature_image,
                ])

            col_widths = [60] * 9 + [100]
            row_heights = [80] * len(data)

            table = Table(data, colWidths=col_widths, rowHeights=row_heights)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)
            doc.build(elements)

            return response

    generate_pdf_for_selected_passenger.short_description = "Generate PDF for Selected Record"
    generate_pdf_for_all_records.short_description = "Generate PDF for All Records"

    actions = [generate_pdf_for_selected_passenger, generate_pdf_for_all_records]
