from django import forms
from .models import *


class OrganizeWasteForm(forms.ModelForm):

    emission_source = forms.CharField(disabled=True, widget = forms.HiddenInput())

    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    quarter = forms.CharField(disabled=True, widget = forms.HiddenInput())

    all = forms.CharField(disabled=True, widget = forms.HiddenInput())
    G = forms.CharField(disabled=True, widget = forms.HiddenInput())


    class Meta:
        model = OrganizeWaste

        fields = '__all__'

        widgets = {
            'emission_source_number': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'number'}),
            'au_ptu_number': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'harmful_substance_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'first_month': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}), 
            'second_month': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}),
            'third_month': forms.TextInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step':'0.001', 'min': '0'}),
            'M': forms.TextInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step':'0.001', 'min': '0'})
        }

    def __init__(self, emission_source, year, quarter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['emission_source'].initial = emission_source
        self.fields['quarter'].initial = quarter
        self.fields['year'].initial = year
        self.fields['all'].initial = 0
        self.fields['G'].initial = 0

        if (quarter == 1):
            self.fields['first_month'].label = 'Январь'
            self.fields['second_month'].label = 'Февраль'
            self.fields['third_month'].label = 'Март'

        elif (quarter == 2):
            self.fields['first_month'].label = 'Апрель'
            self.fields['second_month'].label = 'Май'
            self.fields['third_month'].label = 'Июнь'

        elif (quarter == 3):
            self.fields['first_month'].label = 'Июль'
            self.fields['second_month'].label = 'Август'
            self.fields['third_month'].label = 'Сентябрь'

        elif (quarter == 4):
            self.fields['first_month'].label = 'Октябрь'
            self.fields['second_month'].label = 'Ноябрь'
            self.fields['third_month'].label = 'Декабрь'