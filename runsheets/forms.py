from django import forms

class MonthYearForm(forms.Form):
    month = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 13)],
        label='Month',
        required=True
    )
    year = forms.ChoiceField(
        choices=[(i, i) for i in range(2000, 2101)],
        label='Year',
        required=True
    )