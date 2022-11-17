from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect

from .utils import *
from .models import *
from .forms import *


class HomeView(View):

    def get(self, request):

        return render(request, "base/base.html")



class OrganizeWasteView(View):

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
                "all_G": organize_waste_calc_all_G(data),
            },

            "page_data": {
                "e_s": emission_source,
                "year": year,
                "quarter": quarter,
                "months": get_months(quarter)
            }
        }

        return render(request, "OrganizeWaste/waste.html", context)


class CreateOrganizeWasteView(View):

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


class UpdateOrganizeWasteView(View):

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


class DeleteOrganizeWasteView(View):

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


class WeldingWasteView(View):

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


class CreateWeldingWasteView(View):

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


class UpdateWeldingWasteView(View):

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


class DeleteWeldingWasteView(View):

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
