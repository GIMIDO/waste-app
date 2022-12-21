from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from .utils import *
from .models import *
from .forms import *
from .mixins import *


class HomeView(AuthUserMixin, View):

    def get(self, request):

        return render(request, "base/base.html")


class LoginView(View):

    def get(self, request):

        form = LoginForm(request.POST or None)

        context = {
            'form': form
        }

        return render(request, 'base/login.html', context)

    def post(self, request):

        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                return redirect('home')

        context = {
            'form': form
        }

        return render(request, 'base/login.html', context)

class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('login')


# --- #


class OrganizeWasteView(AuthUserMixin,View):

    def get(self, request, **kwargs):

        if (self.request.GET.get('type')):
            emission_source = self.request.GET.get('type')
            year = self.request.GET.get('year')
            quarter = self.request.GET.get('quarter')
        else:
            emission_source = 'Элеватор'
            year = '2022'
            quarter = '1'


        data = OrganizeWaste.objects.filter(
            emission_source=emission_source,
            year=year,
            quarter=quarter
        )

        organize_waste_calc_all(data)

        context = {
            'table_data': {
                'data': data,
                'h_s_types': get_hs_o(emission_source),
                "calc_data": organize_waste_calc_all_G(data, emission_source),
            },

            "page_data": {
                "e_s": emission_source,
                "year": year,
                "quarter": quarter,
                "months": get_months(quarter)
            }
        }

        return render(request, "OrganizeWaste/waste.html", context)


class CreateOrganizeWasteView(AuthUserMixin,View):

    def get(self, request, **kwargs):

        emission_source = kwargs.get('e_s')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = OrganizeWasteForm(emission_source, year, quarter, request.POST or None)

        context = {
            'form': form,
            "e_s": emission_source,
            "year": year,
            "quarter": quarter,
            "months": get_months(str(quarter))
        }

        return render(request, 'OrganizeWaste/create.html', context)

    def post(self, request, **kwargs):

        emission_source = kwargs.get('e_s')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = OrganizeWasteForm(emission_source, year, quarter, request.POST or None)

        if form.is_valid():
            orgObj = OrganizeWaste.objects.create(
                emission_source = form.cleaned_data['emission_source'],
                emission_source_number = form.cleaned_data['emission_source_number'],
                au_ptu_number = form.cleaned_data['au_ptu_number'],
                harmful_substance_name = form.cleaned_data['harmful_substance_name'],
                year = form.cleaned_data['year'],
                quarter = form.cleaned_data['quarter'],
                first_month = form.cleaned_data['first_month'],
                second_month = form.cleaned_data['second_month'],
                third_month = form.cleaned_data['third_month'],
                all = form.cleaned_data['all'],
                M = form.cleaned_data['M'],
                G = form.cleaned_data['G']
            )
            orgObj.save()

            return redirect(f'/organize/waste/main/?type={emission_source}&year={year}&quarter={quarter}')

        context = {
            'form': form,
            "e_s": emission_source,
            "year": year,
            "quarter": quarter,
            "months": get_months(str(quarter))
        }

        return render(request, 'OrganizeWaste/create.html', context)


class UpdateOrganizeWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        emission_source = kwargs.get('e_s')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = OrganizeWaste.objects.get(
            pk=pk
        )

        form = OrganizeWasteForm(emission_source, year, quarter, request.POST or None, instance=obj)

        context = {
            'form': form,
            "e_s": emission_source,
            "year": year,
            "quarter": quarter,
            "months": get_months(str(quarter))
        }

        return render(request, 'OrganizeWaste/update.html', context)

    def post(self, request, **kwargs):

        pk = kwargs.get('pk')
        emission_source = kwargs.get('e_s')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = OrganizeWaste.objects.get(
            pk=pk
        )

        form = OrganizeWasteForm(emission_source, year, quarter, request.POST or None, instance=obj)

        if form.is_valid():
            form.save()

            return redirect(f'/organize/waste/main/?type={emission_source}&year={year}&quarter={quarter}')

        context = {
            'form': form,
            "e_s": emission_source,
            "year": year,
            "quarter": quarter,
            "months": get_months(str(quarter))
        }

        return render(request, 'OrganizeWaste/update.html', context)


class DeleteOrganizeWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):
        
        obj = OrganizeWaste.objects.get(pk=(kwargs.get('pk')))

        context = {
            "obj": obj
        }

        return render(request, 'OrganizeWaste/delete.html', context)

    def post(self, request, **kwargs):

        obj = OrganizeWaste.objects.get(pk=(kwargs.get('pk')))
        obj.delete()

        return redirect(f'/organize/waste/main/?type={obj.emission_source}&year={obj.year}&quarter={obj.quarter}')


# --- #


class WeldingWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        if (self.request.GET.get('year')):
            year = self.request.GET.get('year')
        else:
            year = '2022'


        data = WeldingWaste.objects.filter(
            year=year
        )

        welding_waste_calc(data)

        context = {
            'table_data': {
                'data': data,
            },

            "page_data": {
                "year": year,
            },
            "q_counter": get_quarters(data),
            "sum_calc": welding_waste_sum_calc(data)
        }

        return render(request, "WeldingWaste/waste.html", context)


class CreateWeldingWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        year = kwargs.get('year')

        form = WeldingWasteForm(year, request.POST or None)

        context = {
            'form': form,
            "year": year,
        }

        return render(request, 'WeldingWaste/create.html', context)

    def post(self, request, **kwargs):

        year = kwargs.get('year')

        form = WeldingWasteForm(year, request.POST or None)

        if form.is_valid():
            orgObj = WeldingWaste.objects.create(
                year = form.cleaned_data['year'],
                quarter = form.cleaned_data['quarter'],
                mark = form.cleaned_data['mark'],
                emission = form.cleaned_data['emission'],
                iron_ox_kg = form.cleaned_data['iron_ox_kg'],
                iron_ox_ton = form.cleaned_data['iron_ox_ton'],
                mg_gg = form.cleaned_data['mg_gg'],
                mg_ton = form.cleaned_data['mg_ton'],
                hyd_flu_gkg = form.cleaned_data['hyd_flu_gkg'],
                hyd_flu_ton = form.cleaned_data['hyd_flu_ton'],
            )
            orgObj.save()

            return redirect(f'/welding/waste/main/?year={year}')

        context = {
            'form': form,
            "year": year,
        }

        return render(request, 'WeldingWaste/create.html', context)


class UpdateWeldingWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')

        obj = WeldingWaste.objects.get(
            pk=pk
        )

        form = WeldingWasteForm(year, request.POST or None, instance=obj)

        context = {
            'form': form,
            "year": year,
        }

        return render(request, 'WeldingWaste/update.html', context)

    def post(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')

        obj = WeldingWaste.objects.get(
            pk=pk
        )

        form = WeldingWasteForm(year, request.POST or None, instance=obj)

        if form.is_valid():
            form.save()

            return redirect(f'/welding/waste/main/?year={year}')

        context = {
            'form': form,
            "year": year,
        }

        return render(request, 'WeldingWaste/update.html', context)


class DeleteWeldingWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):
        
        obj = WeldingWaste.objects.get(pk=(kwargs.get('pk')))

        context = {
            "obj": obj
        }

        return render(request, 'WeldingWaste/delete.html', context)

    def post(self, request, **kwargs):

        obj = WeldingWaste.objects.get(pk=(kwargs.get('pk')))
        obj.delete()

        return redirect(f'/welding/waste/main/?year={obj.year}')


# --- #


class UnOrganizeWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        if (self.request.GET.get('year')):
            year = self.request.GET.get('year')
            quarter = self.request.GET.get('quarter')
            obj_type = self.request.GET.get('obj_type')
        else:
            year = '2022'
            quarter = '1'
            obj_type = 'Мельзавод'


        data = UnOrganizeWaste.objects.filter(
            year=year,
            quarter=quarter,
            obj_type=obj_type
        )

        unorganize_waste_calculate(data)

        context = {
            'table_data': {
                'data': data,
                'h_s_types': get_hs(obj_type),
                'calc_data': unorganize_calc_data(data, obj_type)
            },

            "page_data": {
                "year": year,
                "quarter": quarter,
                "months": get_months(quarter),
                "obj_type": obj_type
            }
        }

        return render(request, "UnOrganizeWaste/waste.html", context)


class CreateUnOrganizeWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        obj_type = kwargs.get('obj_type')

        form = UnOrganizeWasteForm(obj_type, year, quarter, request.POST or None)

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
            "obj_type": obj_type
        }

        return render(request, 'UnOrganizeWaste/create.html', context)

    def post(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        obj_type = kwargs.get('obj_type')

        form = UnOrganizeWasteForm(obj_type, year, quarter, request.POST or None)

        if form.is_valid():
            orgObj = UnOrganizeWaste.objects.create(
                obj_type = form.cleaned_data['obj_type'],
                e_s_number = form.cleaned_data['e_s_number'],
                e_s_name = form.cleaned_data['e_s_name'],
                harmful_substance_name = form.cleaned_data['harmful_substance_name'],
                M = form.cleaned_data['M'],
                T = form.cleaned_data['T'],
                year = form.cleaned_data['year'],
                quarter = form.cleaned_data['quarter'],
                first_month = form.cleaned_data['first_month'],
                second_month = form.cleaned_data['second_month'],
                third_month = form.cleaned_data['third_month'],
                all = form.cleaned_data['all'],
                Tw = form.cleaned_data['Tw'],
                G = form.cleaned_data['G'],
                loaded = form.cleaned_data['loaded'],
                weight = form.cleaned_data['weight'],
            )
            orgObj.save()

            return redirect(f'/unorganize/waste/main/?obj_type={obj_type}&year={year}&quarter={quarter}')

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
            "obj_type": obj_type
        }

        return render(request, 'UnOrganizeWaste/create.html', context)


class UpdateUnOrganizeWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        obj_type = kwargs.get('obj_type')

        obj = UnOrganizeWaste.objects.get(
            pk=pk
        )

        form = UnOrganizeWasteForm(obj_type, year, quarter, request.POST or None, instance=obj)

        context = {
            'form': form,
            "obj_type": obj_type,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'UnOrganizeWaste/update.html', context)

    def post(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')
        obj_type = kwargs.get('obj_type')

        obj = UnOrganizeWaste.objects.get(
            pk=pk
        )

        form = UnOrganizeWasteForm(obj_type, year, quarter, request.POST or None, instance=obj)

        if form.is_valid():
            form.save()

            return redirect(f'/unorganize/waste/main/?obj_type={obj_type}&year={year}&quarter={quarter}')

        context = {
            'form': form,
            "obj_type": obj_type,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'UnOrganizeWaste/update.html', context)


class DeleteUnOrganizeWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):
        
        obj = UnOrganizeWaste.objects.get(pk=(kwargs.get('pk')))

        context = {
            "obj": obj
        }

        return render(request, 'UnOrganizeWaste/delete.html', context)

    def post(self, request, **kwargs):

        obj = UnOrganizeWaste.objects.get(pk=(kwargs.get('pk')))
        obj.delete()

        return redirect(f'/unorganize/waste/main/?obj_type={obj.obj_type}&year={obj.year}&quarter={obj.quarter}')


# --- #


class BoilerWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        if (self.request.GET.get('year')):
            year = self.request.GET.get('year')
            quarter = self.request.GET.get('quarter')
        else:
            year = '2022'
            quarter = '1'


        data1 = BoilerCarbonOxWaste.objects.filter(
            year=year,
            quarter=quarter
        )
        data2 = BoilerNitrogenWaste.objects.filter(
            year=year,
            quarter=quarter
        )
        data3 = BoilerSulfCarbWaste.objects.filter(
            year=year,
            quarter=quarter
        )

        months = get_boiler_months(quarter)

        boiler_carbon_waste_calc(data1)
        boiler_nitrogen_waste_calc(data2)

        boiler_CB_SD_calc(data3)

        context = {
            'table_data': {
                'data1': data1,
                'data2': data2,
                'data3': data3,
                
                'sum_carbon': boiler_carbon_waste_month(data1, months),
                'sum_nitrogen': boiler_nitrogen_waste_month(data2, months),
                'sum_CB_SD': boiler_CB_SD_q(data3)
            },

            "page_data": {
                "year": year,
                "quarter": quarter,
                "months": months,
            }
        }

        return render(request, "BoilerWaste/waste.html", context)


class CreateBoilerNitrogenWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = BoilerNitrogenWasteForm(year, quarter, request.POST or None)

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
            'description': 'выброс азота диоксида и азота оксида',
        }

        return render(request, 'BoilerWaste/create.html', context)

    def post(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = BoilerNitrogenWasteForm(year, quarter, request.POST or None)

        if form.is_valid():
            orgObj = BoilerNitrogenWaste.objects.create(
                name = form.cleaned_data['name'],
                quarter = form.cleaned_data['quarter'],
                month = form.cleaned_data['month'],
                year = form.cleaned_data['year'],
                B = form.cleaned_data['B'],
                Qh = form.cleaned_data['Qh'],
                T = form.cleaned_data['T'],
                Q = form.cleaned_data['Q'],
                Bs = form.cleaned_data['Bs'],
                Knox = form.cleaned_data['Knox'],
                Mnox = form.cleaned_data['Mnox'],
                Mno2 = form.cleaned_data['Mno2'],
                Mno = form.cleaned_data['Mno'],
            )
            orgObj.save()

            return redirect(f'/boiler/waste/main/?year={year}&quarter={quarter}')

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/create.html', context)

class CreateBoilerCarbonOxWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = BoilerCarbonOxWasteForm(year, quarter, request.POST or None)

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
            'description': 'выброс углерода оксида',
        }

        return render(request, 'BoilerWaste/create.html', context)

    def post(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = BoilerCarbonOxWasteForm(year, quarter, request.POST or None)

        if form.is_valid():
            orgObj = BoilerCarbonOxWaste.objects.create(
                name = form.cleaned_data['name'],
                quarter = form.cleaned_data['quarter'],
                month = form.cleaned_data['month'],
                year = form.cleaned_data['year'],
                B = form.cleaned_data['B'],
                Qh = form.cleaned_data['Qh'],
                Qh_calc = form.cleaned_data['Qh_calc'],
                Cco = form.cleaned_data['Cco'],
                Mco = form.cleaned_data['Mco'],
            )
            orgObj.save()

            return redirect(f'/boiler/waste/main/?year={year}&quarter={quarter}')

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/create.html', context)

class CreateBoilerSulfCarbWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = BoilerSulfCarbWasteForm(year, quarter, request.POST or None)

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
            'description': 'расчет дизельного топлива и сажи',
        }

        return render(request, 'BoilerWaste/create.html', context)

    def post(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('q')

        form = BoilerSulfCarbWasteForm(year, quarter, request.POST or None)

        if form.is_valid():
            orgObj = BoilerSulfCarbWaste.objects.create(
                name = form.cleaned_data['name'],
                quarter = form.cleaned_data['quarter'],
                month = form.cleaned_data['month'],
                year = form.cleaned_data['year'],
                B = form.cleaned_data['B'],
                Mc = form.cleaned_data['Mc'],
                Mso2 = form.cleaned_data['Mso2'],
            )
            orgObj.save()

            return redirect(f'/boiler/waste/main/?year={year}&quarter={quarter}')

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/create.html', context)


class UpdateBoilerNitrogenWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = BoilerNitrogenWaste.objects.get(
            pk=pk
        )

        form = BoilerNitrogenWasteForm(year, quarter, request.POST or None, instance=obj)

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/update.html', context)

    def post(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = BoilerNitrogenWaste.objects.get(
            pk=pk
        )

        form = BoilerNitrogenWasteForm(year, quarter, request.POST or None, instance=obj)

        if form.is_valid():
            form.save()

            return redirect(f'/boiler/waste/main/?year={year}&quarter={quarter}')

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/update.html', context)

class UpdateBoilerCarbonOxWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = BoilerCarbonOxWaste.objects.get(
            pk=pk
        )

        form = BoilerCarbonOxWasteForm(year, quarter, request.POST or None, instance=obj)

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/update.html', context)

    def post(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = BoilerCarbonOxWaste.objects.get(
            pk=pk
        )

        form = BoilerCarbonOxWasteForm(year, quarter, request.POST or None, instance=obj)

        if form.is_valid():
            form.save()

            return redirect(f'/boiler/waste/main/?year={year}&quarter={quarter}')

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/update.html', context)

class UpdateBoilerSulfCarbWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = BoilerSulfCarbWaste.objects.get(
            pk=pk
        )

        form = BoilerSulfCarbWasteForm(year, quarter, request.POST or None, instance=obj)

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/update.html', context)

    def post(self, request, **kwargs):

        pk = kwargs.get('pk')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        obj = BoilerSulfCarbWaste.objects.get(
            pk=pk
        )

        form = BoilerSulfCarbWasteForm(year, quarter, request.POST or None, instance=obj)

        if form.is_valid():
            form.save()

            return redirect(f'/boiler/waste/main/?year={year}&quarter={quarter}')

        context = {
            'form': form,
            "year": year,
            "quarter": quarter,
        }

        return render(request, 'BoilerWaste/update.html', context)


class DeleteBoilerNitrogenWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):
        
        obj = BoilerNitrogenWaste.objects.get(pk=(kwargs.get('pk')))

        context = {
            "obj": obj,
            "description": 'выброс азота диоксида и азота оксида',
        }

        return render(request, 'BoilerWaste/delete.html', context)

    def post(self, request, **kwargs):

        obj = BoilerNitrogenWaste.objects.get(pk=(kwargs.get('pk')))
        obj.delete()

        return redirect(f'/boiler/waste/main/?year={obj.year}&quarter={obj.quarter}')

class DeleteBoilerCarbonOxWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):
        
        obj = BoilerCarbonOxWaste.objects.get(pk=(kwargs.get('pk')))

        context = {
            "obj": obj,
            'description' : 'выбросов углерода оксида'
        }

        return render(request, 'BoilerWaste/delete.html', context)

    def post(self, request, **kwargs):

        obj = BoilerCarbonOxWaste.objects.get(pk=(kwargs.get('pk')))
        obj.delete()

        return redirect(f'/boiler/waste/main/?year={obj.year}&quarter={obj.quarter}')

class DeleteBoilerSulfCarbWasteView(AuthUserMixin, View):

    def get(self, request, **kwargs):
        
        obj = BoilerSulfCarbWaste.objects.get(pk=(kwargs.get('pk')))

        context = {
            "obj": obj,
            'description' : 'расчета дизельного топлива и сажи'
        }

        return render(request, 'BoilerWaste/delete.html', context)

    def post(self, request, **kwargs):

        obj = BoilerSulfCarbWaste.objects.get(pk=(kwargs.get('pk')))
        obj.delete()

        return redirect(f'/boiler/waste/main/?year={obj.year}&quarter={obj.quarter}')


