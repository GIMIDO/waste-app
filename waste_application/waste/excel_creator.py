
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import redirect

import xlwt

from .utils import *
from .models import *


def get_columns(quarter, toc):

    months = get_months(str(quarter))

    return ['№ ист.', '№ АУ или ПТУ', 'Вредное вещество', months['1'], months['2'], months['3'], 'Всего', 'М, г/с', 'G, т/год']


class OrganizeDownloadExcel(View):

    def get(self, request, **kwargs):

        toc = kwargs.get('toc')
        emission_source = kwargs.get('e_s')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        data = OrganizeWaste.objects.filter(
            emission_source=emission_source,
            year=year,
            quarter=quarter
        )

        if data.exists():
            pass
        else:
            return redirect(f'/organize/waste/main/?type={emission_source}&year={year}&quarter={quarter}')

        h_s_types = get_hs_o(emission_source)
        calc_data = organize_waste_calc_all_G(data, emission_source)
        print(calc_data)

        NAMES = {
            'Элеватор': 'Elevator',
            'Мельница': 'Mill',
            'Крупозавод': 'Groats_factory',
            'Фасовка': 'Packed',
        }

        response = HttpResponse(content_type='application/ms-excel')
        response.headers['Content-Disposition'] = f'attachment; filename="{NAMES[emission_source]}_{year}_{quarter}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')

        ws = wb.add_sheet("sheet1")

        row_num = 0

        font_style = xlwt.XFStyle()

        font_style.font.bold = True

        columns = get_columns(quarter, toc)

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        for i in range(len(h_s_types)):
            for my_row in data:
                if my_row.harmful_substance_name == h_s_types[i]:
                    row_num += 1
                    ws.write(row_num, 0, my_row.emission_source_number, font_style)
                    ws.write(row_num, 1, my_row.au_ptu_number, font_style)
                    ws.write(row_num, 2, my_row.harmful_substance_name, font_style)

                    ws.write(row_num, 3, my_row.first_month, font_style)
                    ws.write(row_num, 4, my_row.second_month, font_style)
                    ws.write(row_num, 5, my_row.third_month, font_style)

                    ws.write(row_num, 6, my_row.all, font_style)
                    ws.write(row_num, 7, my_row.M, font_style)
                    ws.write(row_num, 8, my_row.G, font_style)

            row_num += 1
            ws.write(row_num, 7, 'Итого:', font_style)
            ws.write(row_num, 8, calc_data[i], font_style)
            i += 1

        wb.save(response)

        return response


class WeldingDownloadExcel(View):

    def get(self, request, **kwargs):

        year = kwargs.get('year')

        data = WeldingWaste.objects.filter(
            year=year,
        )

        if data.exists():
            pass
        else:
            return redirect(f'/welding/waste/main/?year={year}')

        response = HttpResponse(content_type='application/ms-excel')
        response.headers['Content-Disposition'] = f'attachment; filename="Weldings_{year}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')

        ws = wb.add_sheet("sheet1")

        row_num = 0

        font_style = xlwt.XFStyle()

        font_style.font.bold = True

        columns = ['Квартал', 'Марка электр.', 'Удельн. выдел.', 'Оксид железа', '', 'Марганец', '', 'Фтористый водород', '']
        columns2 = ['', '', '', 'кг', 'т/год', 'г/г', 'т/год', 'г/кг', 'т/год']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        row_num += 1
        for col_num in range(len(columns2)):
            ws.write(row_num, col_num, columns2[col_num], font_style)

        font_style = xlwt.XFStyle()

        quarters = get_quarters(data)
        sum_calc = welding_waste_sum_calc(data)

        for q in quarters:
            for my_row in data:
                if (my_row.quarter == q):
                    row_num += 1
                    ws.write(row_num, 0, my_row.quarter, font_style)
                    ws.write(row_num, 1, my_row.mark, font_style)
                    ws.write(row_num, 2, my_row.emission, font_style)

                    ws.write(row_num, 3, my_row.iron_ox_kg, font_style)
                    ws.write(row_num, 4, my_row.iron_ox_ton, font_style)

                    ws.write(row_num, 5, my_row.mg_gg, font_style)
                    ws.write(row_num, 6, my_row.mg_ton, font_style)

                    ws.write(row_num, 7, my_row.hyd_flu_gkg, font_style)
                    ws.write(row_num, 8, my_row.hyd_flu_ton, font_style)

            row_num += 1
            ws.write(row_num, 0, "Итого:", font_style)
            ws.write(row_num, 3, sum_calc[str(q)]['s_i_kg'], font_style)
            ws.write(row_num, 4, sum_calc[str(q)]['s_i_t'], font_style)

            ws.write(row_num, 5, sum_calc[str(q)]['s_m_g'], font_style)
            ws.write(row_num, 6, sum_calc[str(q)]['s_m_t'], font_style)

            ws.write(row_num, 7, sum_calc[str(q)]['s_hf_g'], font_style)
            ws.write(row_num, 8, sum_calc[str(q)]['s_hf_t'], font_style)
            row_num += 1
            q += 1

        row_num += 1
        ws.write(row_num, 0, "Итого за год:", font_style)
        ws.write(row_num, 3, sum_calc["year"]['y_i_kg'], font_style)
        ws.write(row_num, 4, sum_calc["year"]['y_i_t'], font_style)

        ws.write(row_num, 5, sum_calc["year"]['y_m_g'], font_style)
        ws.write(row_num, 6, sum_calc["year"]['y_m_t'], font_style)

        ws.write(row_num, 7, sum_calc["year"]['y_hf_g'], font_style)
        ws.write(row_num, 8, sum_calc["year"]['y_hf_t'], font_style)
        wb.save(response)

        return response


class UnOrganizeDownloadExcel(View):

    def get(self, request, **kwargs):

        obj_type = kwargs.get('obj_type')
        year = kwargs.get('year')
        quarter = kwargs.get('quarter')

        data = UnOrganizeWaste.objects.filter(
            obj_type=obj_type,
            year=year,
            quarter=quarter
        )
        h_s_types = get_hs(obj_type)
        calc_data = unorganize_calc_data(data, obj_type)

        if data.exists():
            pass
        else:
            return redirect(f'/unorganize/waste/main/?obj_type={obj_type}&year={year}&quarter={quarter}')

        NAMES = {
            'Мельзавод': 'Mill',
            'Крупозавод': 'Groats_factory',
            'РБ': 'R/B',
        }

        response = HttpResponse(content_type='application/ms-excel')
        response.headers['Content-Disposition'] = f'attachment; filename="{NAMES[obj_type]}_{year}_{quarter}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')

        ws = wb.add_sheet("sheet1")

        row_num = 0

        font_style = xlwt.XFStyle()

        font_style.font.bold = True

        months = get_months(str(quarter))
        columns = [
            'Объект',
            '№ источника выброса',
            'Наименование источника выброса',
            'Вредное вещество',
            'Максимальное выделение веществ [М, г/с]',
            'Время операции [T, с]',
            'Количество транспортных единиц, [шт]',
            '',
            '',
            '',
            'Кол-во часов работы [T, час/год]',
            'Валовый выброс [T, т/год]',
            'Загружено',
            'Вес одной ед. [кг]',
        ]
        columns2 = ['', '', '', '', '', '', '',
            months['1'],
            months['2'],
            months['3'],
            'Всего',
            '', '', '', '', '',
        ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        row_num += 1
        for col_num in range(len(columns2)):
            ws.write(row_num, col_num, columns2[col_num], font_style)

        font_style = xlwt.XFStyle()

        for i in range(len(h_s_types)):
            # i = 0
            for my_row in data:
                if my_row.harmful_substance_name == h_s_types[i]:
                    row_num += 1
                    ws.write(row_num, 0, my_row.obj_type, font_style)
                    ws.write(row_num, 1, my_row.e_s_number, font_style)
                    ws.write(row_num, 2, my_row.e_s_name, font_style)

                    ws.write(row_num, 3, my_row.harmful_substance_name, font_style)
                    ws.write(row_num, 4, my_row.M, font_style)
                    ws.write(row_num, 5, my_row.T, font_style)

                    ws.write(row_num, 6, my_row.first_month, font_style)
                    ws.write(row_num, 7, my_row.second_month, font_style)
                    ws.write(row_num, 8, my_row.third_month, font_style)

                    ws.write(row_num, 9, my_row.all, font_style)
                    ws.write(row_num, 10, my_row.Tw, font_style)
                    ws.write(row_num, 11, my_row.G, font_style)
                    ws.write(row_num, 12, my_row.loaded, font_style)
                    ws.write(row_num, 13, my_row.weight, font_style)
            
            row_num += 1
            ws.write(row_num, 10, 'Итого:', font_style)
            ws.write(row_num, 11, calc_data[i], font_style)
            i += 1

        wb.save(response)

        return response