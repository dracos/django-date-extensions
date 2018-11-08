from django import forms
from approximate_date.django.forms import VagueDateNumbersField, VagueDateTextField


class DatesForm(forms.Form):
    text_input = VagueDateTextField()
    numbers_input = VagueDateNumbersField(required=False)

    # REMOVE
    def clean(self):
        self.safe_cleaned_data = self.cleaned_data
        return self.cleaned_data
