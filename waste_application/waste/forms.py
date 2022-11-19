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


class WeldingWasteForm(forms.ModelForm):

    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    iron_ox_ton = forms.CharField(disabled=True, widget = forms.HiddenInput())
    mg_ton = forms.CharField(disabled=True, widget = forms.HiddenInput())
    hyd_flu_ton = forms.CharField(disabled=True, widget = forms.HiddenInput())

    class Meta:
        model = WeldingWaste

        fields = '__all__'

        widgets = {
            'quarter': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step': '1', 'max': '4', 'min':'1'}),

            'mark': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'text'}),
            'emission': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number'}),

            'iron_ox_kg': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'1', 'min': '0'}), 

            'mg_gg': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}), 

            'hyd_flu_gkg': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}), 

        }

    def __init__(self, year, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].initial = year
        self.fields['iron_ox_ton'].initial = 0
        self.fields['mg_ton'].initial = 0
        self.fields['hyd_flu_ton'].initial = 0


class UnOrganizeWasteForm(forms.ModelForm):

    obj_type = forms.CharField(disabled=True, widget = forms.HiddenInput())
    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    quarter = forms.CharField(disabled=True, widget = forms.HiddenInput())
    all = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Tw = forms.CharField(disabled=True, widget = forms.HiddenInput())
    G = forms.CharField(disabled=True, widget = forms.HiddenInput())

    class Meta:

        model = UnOrganizeWaste
        
        fields = '__all__'

        widgets = {
            'e_s_number': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number'}),
            'e_s_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'type':'text'}),
            'harmful_substance_name': forms.Select(attrs={'class': 'form-control mb-3', 'type':'text'}),

            'M': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}), 
            'T': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'1', 'min': '0'}), 

            'first_month': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}), 
            'second_month': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}),
            'third_month': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step':'0.001', 'min': '0'}),

            'loaded': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'1', 'min': '0'}), 
            'weight': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step':'1', 'min': '0'}), 
        }

    def __init__(self, obj_type, year, quarter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['obj_type'].initial = obj_type
        self.fields['year'].initial = year
        self.fields['quarter'].initial = quarter
        self.fields['all'].initial = 0
        self.fields['Tw'].initial = 0
        self.fields['G'].initial = 0