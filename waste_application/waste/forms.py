from django import forms
from .models import *


# форма Логина
class LoginForm(forms.Form):

    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control me-5 w-25'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control mb-3 w-25'}))

    class Meta:
        model = User

        fields = '__all__'

    # проверка введенных данных
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь {username} не найден!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль!')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'


# форма Организованные
class OrganizeWasteForm(forms.ModelForm):

    emission_source = forms.CharField(disabled=True, widget = forms.HiddenInput())

    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    quarter = forms.CharField(disabled=True, widget = forms.HiddenInput())

    all = forms.CharField(disabled=True, widget = forms.HiddenInput())
    G = forms.CharField(disabled=True, widget = forms.HiddenInput())

    class Meta:
        model = OrganizeWaste

        fields = '__all__'

        # атрибуты HTML-элемента
        widgets = {
            'emission_source_number': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'number'}),
            'au_ptu_number': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'harmful_substance_name': forms.Select(attrs={'class': 'form-control mb-3'}),

            'first_month': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}), 
            'second_month': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}),
            'third_month': forms.TextInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step':'0.001', 'min': '0'}),

            'M': forms.TextInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step':'0.001', 'min': '0'}),

            'operating_mode': forms.Select(attrs={'class': 'form-control mb-1'}),
            'code_ZV': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number'}),
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


# форма Сварка
class WeldingWasteForm(forms.ModelForm):

    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    iron_ox_ton = forms.CharField(disabled=True, widget = forms.HiddenInput())
    mg_ton = forms.CharField(disabled=True, widget = forms.HiddenInput())
    hyd_flu_ton = forms.CharField(disabled=True, widget = forms.HiddenInput())

    class Meta:
        model = WeldingWaste

        fields = '__all__'

        # атрибуты HTML-элемента
        widgets = {
            'quarter': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number', 'step': '1', 'max': '4', 'min':'1'}),

            'mark': forms.TextInput(attrs={'class': 'form-control mb-1', 'type':'text'}),
            'emission': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number'}),

            'iron_ox_kg': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.001', 'min': '0'}), 

            'mg_gg': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.0001', 'min': '0'}), 

            'hyd_flu_gkg': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'step':'0.0001', 'min': '0'}), 

        }

    def __init__(self, year, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].initial = year
        self.fields['iron_ox_ton'].initial = 0
        self.fields['mg_ton'].initial = 0
        self.fields['hyd_flu_ton'].initial = 0


# форма Неорганизованные
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

        # атрибуты HTML-элемента
        widgets = {
            'e_s_number': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number'}),
            'e_s_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'type':'text'}),
            'harmful_substance_name': forms.Select(attrs={'class': 'form-control mb-3', 'type':'text'}),
            
            'code_ZV': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number'}),

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


# форма Котельные углерод оксид
class BoilerCarbonOxWasteForm(forms.ModelForm):

    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    quarter = forms.CharField(disabled=True, widget = forms.HiddenInput())

    Qh_calc = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Cco = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Mco = forms.CharField(disabled=True, widget = forms.HiddenInput())

    class Meta:

        model = BoilerCarbonOxWaste
        
        fields = '__all__'

        # атрибуты HTML-элемента
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control mb-1', 'type':'text'}),
            'month': forms.Select(attrs={'class': 'form-control mb-3', 'type':'text'}),
            'B': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'min': '0', 'step': '0.0001'}),
            'Qh': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number', 'min': '0', 'step': '1'}),

        }

    def __init__(self, year, quarter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].initial = year
        self.fields['quarter'].initial = quarter
        self.fields['Qh_calc'].initial = 0
        self.fields['Cco'].initial = 0
        self.fields['Mco'].initial = 0

# форма Котелные азот диоксид и азот оксид
class BoilerSulfCarbWasteForm(forms.ModelForm):

    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    quarter = forms.CharField(disabled=True, widget = forms.HiddenInput())

    Mc = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Mso2 = forms.CharField(disabled=True, widget = forms.HiddenInput())

    class Meta:

        model = BoilerSulfCarbWaste
        
        fields = '__all__'

        # атрибуты HTML-элемента
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control mb-1', 'type':'text'}),
            'month': forms.Select(attrs={'class': 'form-control mb-3', 'type':'text'}),
            'B': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'min': '0', 'step': '0.00001'}),

        }

    def __init__(self, year, quarter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].initial = year
        self.fields['quarter'].initial = quarter
        self.fields['Mc'].initial = 0
        self.fields['Mso2'].initial = 0

# форма Котельные дизельное топливо и сажа
class BoilerNitrogenWasteForm(forms.ModelForm):

    year = forms.CharField(disabled=True, widget = forms.HiddenInput())
    quarter = forms.CharField(disabled=True, widget = forms.HiddenInput())

    Q = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Bs = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Knox = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Mnox = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Mno2 = forms.CharField(disabled=True, widget = forms.HiddenInput())
    Mno = forms.CharField(disabled=True, widget = forms.HiddenInput())

    class Meta:

        model = BoilerNitrogenWaste
        
        fields = '__all__'

        # атрибуты HTML-элемента
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control mb-1', 'type':'text'}),
            'month': forms.Select(attrs={'class': 'form-control mb-3', 'type':'text'}),
            'B': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'min': '0', 'step': '0.0001'}),
            'Qh': forms.NumberInput(attrs={'class': 'form-control mb-1', 'type':'number', 'min': '0', 'step': '1'}),
            'T': forms.NumberInput(attrs={'class': 'form-control mb-3', 'type':'number', 'min': '0', 'step': '1'}),

        }

    def __init__(self, year, quarter, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].initial = year
        self.fields['quarter'].initial = quarter
        self.fields['Q'].initial = 0
        self.fields['Bs'].initial = 0
        self.fields['Knox'].initial = 0
        self.fields['Mnox'].initial = 0
        self.fields['Mno2'].initial = 0
        self.fields['Mno'].initial = 0
