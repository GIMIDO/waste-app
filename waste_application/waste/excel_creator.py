
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import redirect

import xlwt

from .utils import *
from .models import *


def get_columns(quarter):

    months = get_months(str(quarter))

    return ['№ ист.', '№ АУ или ПТУ', 'Вредное вещество', months['1'], months['2'], months['3'], 'Всего', 'М, г/с', 'G, т/год']

def quarter_rim(quarter):
    match str(quarter):
        case '1':
            return 'I'
        case 2:
            return 'II'
        case 3:
            return 'III'
        case 4:
            return 'IV'


class OrganizeDownloadExcel(View):

    def get(self, request, **kwargs):

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

        NAMES = {'Элеватор': 'Elevator', 'Мельница': 'Mill', 'Крупозавод': 'Groats_factory', 'Фасовка': 'Packed'}

        response = HttpResponse(content_type='application/ms-excel')
        response.headers['Content-Disposition'] = f'attachment; filename="{NAMES[emission_source]}_{year}_{quarter}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')

        ws = wb.add_sheet("sheet1")

        row_num = 0

        font_style = xlwt.XFStyle()

        font_style.font.bold = True

        ws.write(row_num, 0, emission_source, font_style)
        row_num += 1

        columns = get_columns(quarter)

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        h_s_types = ['Пыль зерновая', 'Твердые суммарно']

        for i in h_s_types:
            sum = 0
            for my_row in data:
                if my_row.harmful_substance_name == i:
                    row_num += 1
                    sum += my_row.G
                    ws.write(row_num, 0, my_row.emission_source_number, font_style)
                    ws.write(row_num, 1, my_row.au_ptu_number, font_style)
                    ws.write(row_num, 2, my_row.harmful_substance_name, font_style)

                    ws.write(row_num, 3, my_row.first_month, font_style)
                    ws.write(row_num, 4, my_row.second_month, font_style)
                    ws.write(row_num, 5, my_row.third_month, font_style)

                    ws.write(row_num, 6, my_row.all, font_style)
                    ws.write(row_num, 7, my_row.M, font_style)
                    ws.write(row_num, 8, round(my_row.G, 4), font_style)

            row_num += 1
            ws.write(row_num, 6, 'Итого:', font_style)
            ws.write(row_num, 7, i, font_style)
            ws.write(row_num, 8, round(sum, 4), font_style)

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


class BoilerDownloadExcel(View):

    def get(self, request, **kwargs):

        year = kwargs.get('year')
        quarter = kwargs.get('quarter')

        dataBT = BoilerWaste.objects.all()

        if not dataBT.exists():
            return redirect(f'/boiler/waste/main/?year={year}&quarter={quarter}')

        response = HttpResponse(content_type='application/ms-excel')
        response.headers['Content-Disposition'] = f'attachment; filename="Boiler_{year}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")

        row_num = 0

        for item in dataBT:

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['', item.name, 'Время']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            row_num += 1

            font_style = xlwt.XFStyle()

            columns = ['', 'тыс м3', 'час.', 'CO', 'Азот(1У)N2O', 'Азот(11)', 'SО2', 'углер.черный']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            y_B, y_Mco, y_T, y_Mno2, y_Mno, y_Mc, y_Mso2 = 0,0,0,0,0,0,0
            quarter = 1
            while(quarter < 5):
                q_B, q_Mco, q_T, q_Mno2, q_Mno, q_Mc, q_Mso2 = 0,0,0,0,0,0,0
                
                font_style = xlwt.XFStyle()

                carbon = BoilerCarbonOxWaste.objects.filter(quarter=quarter, name=item, year=year)
                nitrogen = BoilerNitrogenWaste.objects.filter(quarter=quarter, name=item, year=year)
                carb_sulf = BoilerSulfCarbWaste.objects.filter(quarter=quarter, name=item, year=year)

                months = get_boiler_months(str(quarter))
                for elem in months:
                    row_num += 1
                    ws.write(row_num, 0, elem, font_style)

                    if carbon.exists():
                        for dataElem in carbon:
                            if dataElem.month == elem:
                                ws.write(row_num, 1, dataElem.B, font_style)
                                ws.write(row_num, 3, dataElem.Mco, font_style)
                                q_B += dataElem.B
                                q_Mco += dataElem.Mco
                    if nitrogen.exists():
                        for dataElem in nitrogen:
                            if dataElem.month == elem:
                                ws.write(row_num, 2, dataElem.T, font_style)
                                ws.write(row_num, 4, round(dataElem.Mno2, 4), font_style)
                                ws.write(row_num, 5, dataElem.Mno, font_style)
                                q_T += dataElem.T
                                q_Mno2 += dataElem.Mno2
                                q_Mno += dataElem.Mno
                    if carb_sulf.exists():
                        for dataElem in carb_sulf:
                            if dataElem.name == item and dataElem.month == elem:
                                ws.write(row_num, 6, dataElem.Mc, font_style)
                                ws.write(row_num, 7, dataElem.Mso2, font_style)
                                q_Mc += dataElem.Mc
                                q_Mso2 += dataElem.Mso2

                row_num += 1

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                ws.write(row_num, 0, f'Итого {quarter}кв', font_style)
                ws.write(row_num, 1, q_B, font_style)
                ws.write(row_num, 2, q_T, font_style)
                ws.write(row_num, 3, q_Mco, font_style)
                ws.write(row_num, 4, round(q_Mno2, 4), font_style)
                ws.write(row_num, 5, q_Mno, font_style)
                ws.write(row_num, 6, q_Mc, font_style)
                ws.write(row_num, 7, q_Mso2, font_style)

                y_B += q_B
                y_Mco += q_Mco
                y_T += q_T
                y_Mno2 += q_Mno2
                y_Mno += q_Mno
                y_Mc += q_Mc
                y_Mso2 += q_Mso2

                quarter += 1

            row_num += 1

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            ws.write(row_num, 0, 'Всего за год', font_style)
            ws.write(row_num, 1, y_B, font_style)
            ws.write(row_num, 2, y_T, font_style)
            ws.write(row_num, 3, y_Mco, font_style)
            ws.write(row_num, 4, round(y_Mno2, 4), font_style)
            ws.write(row_num, 5, y_Mno, font_style)
            ws.write(row_num, 6, y_Mc, font_style)
            ws.write(row_num, 7, y_Mso2, font_style)

            row_num += 2

        wb.save(response)

        return response


class IRSOrganizeDownloadExcel(View):

    def get(self, request, **kwargs):

        year = self.request.GET.get('year')
        quarter = self.request.GET.get('quarter')

        data = OrganizeWaste.objects.filter(year=year, quarter=quarter)

        if data.exists():
            pass
        else:
            return redirect('report')

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")

        # fonts
        f_s = xlwt.easyxf('font: height 240, name Times New Roman;') # стандартный
        f_s_b_i = xlwt.easyxf('font: height 240, name Times New Roman, bold 1, italic 1;') # жирный италик
        f_s_bold_sum = xlwt.easyxf('font: height 240, name Times New Roman, bold 1; align: horiz right;') # для вывода суммы по категории
        h_s = xlwt.easyxf('align: wrap yes,vert centre, horiz centre; font: height 240, name Times New Roman;') # для хэдэров

        row_num = 0

        def header(row_num, header_count):
            ws.write(row_num, 0, f'Год {year}', f_s)
            ws.merge(row_num,row_num,0,1)
            ws.write(row_num, 2, 'квартал', f_s)
            ws.write(row_num, 3, quarter_rim(quarter), f_s)
            ws.write(row_num, 14, f'лист {header_count}', f_s)

            row_num += 2

            ws.write(row_num, 0, 'Источник выбросов', h_s)
            ws.merge(row_num, row_num, 0, 1)
            ws.write(row_num+1, 0, '№', h_s)
            ws.merge(row_num+1, row_num+3, 0, 0)
            ws.write(row_num+1, 1, 'Номера вентиляционных систем стационарных источнков', h_s)
            ws.merge(row_num+1, row_num+3, 1, 1)

            ws.write(row_num, 2, 'Режим работы технологического оборудования', h_s)
            ws.merge(row_num, row_num+3, 2, 2)

            ws.write(row_num, 3, 'Выброс загрязняющего вещества в атмосферный воздух', h_s)
            ws.merge(row_num, row_num+2, 3, 4)
            ws.write(row_num+3, 3, 'Наименование или хим.формула ЗВ', h_s)
            ws.merge(row_num+3, row_num+3, 3, 3)
            ws.write(row_num+3, 4, 'Код ЗВ', h_s)
            ws.merge(row_num+3, row_num+3, 4, 4)

            ws.write(row_num, 5, 'Параметры выбросов загрязняющих веществ в атмосферный воздух', h_s)
            ws.merge(row_num, row_num+1, 5, 14)
            ws.write(row_num+2, 5, '1 месяц', h_s)
            ws.merge(row_num+2, row_num+2, 5, 7)
            ws.write(row_num+2, 8, '2 месяц', h_s)
            ws.merge(row_num+2, row_num+2, 8, 10)
            ws.write(row_num+2, 11, '3 месяц', h_s)
            ws.merge(row_num+2, row_num+2, 11, 13)
            ws.write(row_num+2, 14, 'квартал', h_s)

            ws.write(row_num+3, 5, 'Значение выброса Вк, г/с', h_s)
            ws.merge(row_num+3, row_num+3, 5, 5)
            ws.write(row_num+3, 8, 'Значение выброса Вк, г/с', h_s)
            ws.merge(row_num+3, row_num+3, 8, 8)
            ws.write(row_num+3, 11, 'Значение выброса Вк, г/с', h_s)
            ws.merge(row_num+3, row_num+3, 11, 11)

            ws.write(row_num+3, 6, 'Время работы источников, ч/мес', h_s)
            ws.merge(row_num+3, row_num+3, 6, 6)
            ws.write(row_num+3, 9, 'Время работы источников, ч/мес', h_s)
            ws.merge(row_num+3, row_num+3, 9, 9)
            ws.write(row_num+3, 12, 'Время работы источников, ч/мес', h_s)
            ws.merge(row_num+3, row_num+3, 12, 12)

            ws.write(row_num+3, 7, 'Масса выброса  ЗВ, т/мес.', h_s)
            ws.merge(row_num+3, row_num+3, 7, 7)
            ws.write(row_num+3, 10, 'Масса выброса  ЗВ, т/мес.', h_s)
            ws.merge(row_num+3, row_num+3, 10, 10)
            ws.write(row_num+3, 13, 'Масса выброса  ЗВ, т/мес.', h_s)
            ws.merge(row_num+3, row_num+3, 13, 13)
            ws.write(row_num+3, 14, 'Масса выброса  ЗВ, т/мес.', h_s)
            ws.merge(row_num+3, row_num+3, 14, 14)

            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 34*20
            ws.row(row_num+1).height_mismatch = True
            ws.row(row_num+1).height = 29*20
            ws.row(row_num+3).height_mismatch = True
            ws.row(row_num+3).height = 88*20

            return row_num

        zerno, solid, header_count = 0,0,1
        harmf_name = ['Пыль зерновая','Твердые суммарно']
        names = ['Элеватор','Мельница','Крупозавод','Фасовка']

        for eType in names:
            t_data = data.filter(emission_source=eType)
            sum = 0

            if header_count < 4:
                header(row_num, header_count)
                row_num += 6
                header_count += 1

            for h in harmf_name:
                f_data = t_data.filter(harmful_substance_name=h)

                if f_data.exists():

                    for item in f_data:
                        item_sum = 0
                        row_num += 1

                        ws.write(row_num, 0, item.emission_source_number, f_s)
                        ws.write(row_num, 1, item.au_ptu_number, f_s)
                        ws.write(row_num, 2, item.operating_mode[0:8], f_s)
                        ws.write(row_num, 3, item.harmful_substance_name, f_s)
                        ws.write(row_num, 4, item.code_ZV, f_s)
                        
                        ws.write(row_num, 5, item.M, f_s)
                        ws.write(row_num, 6, item.first_month, f_s_b_i)
                        calc = item.M * item.first_month * 3600 * decimal.Decimal(0.000001)
                        item_sum += calc
                        ws.write(row_num, 7, round(calc, 4), f_s)

                        ws.write(row_num, 8, item.M, f_s)
                        ws.write(row_num, 9, item.second_month, f_s_b_i)
                        calc = item.M * item.second_month * 3600 * decimal.Decimal(0.000001)
                        item_sum += calc
                        ws.write(row_num, 10, round(calc, 4), f_s)

                        ws.write(row_num, 11, item.M, f_s)
                        ws.write(row_num, 12, item.third_month, f_s_b_i)
                        calc = item.M * item.third_month * 3600 * decimal.Decimal(0.000001)
                        item_sum += calc
                        ws.write(row_num, 13, round(calc, 4), f_s)

                        ws.write(row_num, 14, round(item_sum, 4), f_s)
                        sum += item_sum

                        if item.harmful_substance_name == 'Твердые суммарно':
                            solid += sum
                        else:
                            zerno += sum

                    if h == 'Твердые суммарно':
                        eType = 'Твердые суммарно'
                    row_num += 1
                    ws.write(row_num, 10, f'Итого по {eType}', f_s_bold_sum)
                    ws.merge(row_num, row_num, 10, 13)
                    ws.write(row_num, 14, round(sum, 4), f_s_bold_sum)
            if header_count < 4:
                row_num += 3        

        row_num += 1
        ws.write(row_num, 1, 'Сумма:', f_s)
        ws.write(row_num, 2, 'пыль зерновая', f_s)
        ws.write(row_num, 14, round(zerno, 4), f_s)

        row_num += 1
        ws.write(row_num, 2, 'твердые суммарно', f_s)
        ws.write(row_num, 14, round(solid, 4), f_s)

        row_num += 1
        ws.write(row_num, 2, 'Итого по загрязняющим веществам:', f_s)
        row_num += 1
        ws.write(row_num, 2, '3 класса опасности', f_s)
        ws.write(row_num, 14, round(solid+zerno, 4), f_s)

        row_num += 1
        ws.write(row_num, 2, 'Проверил', f_s)
        ws.write(row_num, 4, 'Главный инженер', f_s)
        ws.write(row_num, 6, '_______________', f_s)
        ws.write(row_num, 11, 'С. И. Лызо', f_s)

        ws.col(0).width = 6*256
        ws.col(1).width = 11*256
        ws.col(2).width = 10*256
        ws.col(3).width = 15*256

        response = HttpResponse(content_type='application/ms-excel')
        response.headers['Content-Disposition'] = f'attachment; filename="POD-1_{year}_{quarter}.xls"'

        wb.save(response)

        return response
