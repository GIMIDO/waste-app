
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
        case "1":
            return 'I'
        case "2":
            return 'II'
        case "3":
            return 'III'
        case "4":
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
            'Фосфин': 'Fosfin',
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


# ПОД-2
class IRS2OrganizeDownloadExcel(View):

    def get(self, request, **kwargs):

        # получение года и квартала
        year = self.request.GET.get('year')
        quarter = self.request.GET.get('quarter')

        # создание таблицы
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")

        # шрифты
        f_s = xlwt.easyxf('font: height 240, name Times New Roman;') # стандартный
        f_s_b_i = xlwt.easyxf('font: height 240, name Times New Roman, bold 1, italic 1;') # жирный италик
        f_s_bold_sum = xlwt.easyxf('font: height 240, name Times New Roman, bold 1; align: horiz right;') # для вывода суммы по категории
        h_s = xlwt.easyxf('align: wrap yes,vert centre, horiz centre; font: height 240, name Times New Roman;') # для хэдэров

        # установка счетчика строк и счетчика листов
        row_num = 0

        # формирование хэдэра для таблицы
        def header(row_num):
            ws.write(row_num, 0, f'Год {year}', f_s)
            ws.merge(row_num,row_num,0,1)
            ws.write(row_num, 2, 'квартал', f_s)
            ws.write(row_num, 3, quarter_rim(quarter), f_s)

            row_num += 1

            ws.write(row_num, 0, 'Источник выбросов', h_s)
            ws.merge(row_num, row_num, 0, 1)
            ws.write(row_num, 2, 'Наименование топлива, сырья, материалов', h_s)
            ws.merge(row_num, row_num+3, 2, 2)
            ws.write(row_num+1, 0, '№', h_s)
            ws.merge(row_num+1, row_num+3, 0, 0)
            ws.write(row_num+1, 1, 'Номера вентиляционных систем стационарных источнков', h_s)
            ws.merge(row_num+1, row_num+3, 1, 1)

            ws.write(row_num, 3, 'Выброс загрязняющего вещества в атмосферный воздух', h_s)
            ws.merge(row_num, row_num+1, 3, 6)

            ws.write(row_num, 7, 'Параметры выбросов загрязняющих веществ в атмосферный воздух', h_s)
            ws.merge(row_num, row_num, 7, 13)
            ws.write(row_num+1, 7, '1 месяц', h_s)
            ws.merge(row_num+1, row_num+1, 7, 8)
            ws.write(row_num+1, 9, '2 месяц', h_s)
            ws.merge(row_num+1, row_num+1, 9, 10)
            ws.write(row_num+1, 11, '3 месяц', h_s)
            ws.merge(row_num+1, row_num+1, 11, 12)
            ws.write(row_num+1, 13, 'Квартал', h_s)

            ws.write(row_num+2, 3, 'Hаименование или хим.формула ЗВ', h_s)
            ws.merge(row_num+2, row_num+3, 3, 3)
            ws.write(row_num+2, 4, 'Код ЗВ', h_s)
            ws.merge(row_num+2, row_num+3, 4, 4)
            ws.write(row_num+2, 5, 'Технологический удельный норматив', h_s)
            ws.merge(row_num+2, row_num+2, 5, 6)
            ws.write(row_num+3, 5, 'Значение', h_s)
            ws.write(row_num+3, 6, 'ед. изм.', h_s)

            ws.write(row_num+2, 7, 'Кол-во израсх. ед. топлива, выпущ. прод. произвед. энергии / мес.', h_s)
            ws.merge(row_num+2, row_num+3, 7, 7)
            ws.write(row_num+2, 9, 'Кол-во израсх. ед. топлива, выпущ. прод. произвед. энергии / мес.', h_s)
            ws.merge(row_num+2, row_num+3, 9, 9)
            ws.write(row_num+2, 11, 'Кол-во израсх. ед. топлива, выпущ. прод. произвед. энергии / мес.', h_s)
            ws.merge(row_num+2, row_num+3, 11, 11)

            ws.write(row_num+2, 8, 'Масса выброса ЗВ, т/мес.', h_s)
            ws.merge(row_num+2, row_num+3, 8, 8)
            ws.write(row_num+2, 10, 'Масса выброса ЗВ, т/мес.', h_s)
            ws.merge(row_num+2, row_num+3, 10, 10)
            ws.write(row_num+2, 12, 'Масса выброса ЗВ, т/мес.', h_s)
            ws.merge(row_num+2, row_num+3, 12, 12)
            ws.write(row_num+2, 13, 'Масса выброса ЗВ, т/мес.', h_s)
            ws.merge(row_num+2, row_num+3, 13, 13)

            for i in range(14):
                ws.write(row_num+4, i, i+1, h_s)

            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 42*20
            ws.row(row_num+1).height_mismatch = True
            ws.row(row_num+1).height = 16*20
            ws.row(row_num+2).height_mismatch = True
            ws.row(row_num+2).height = 47*20
            ws.row(row_num+3).height_mismatch = True
            ws.row(row_num+3).height = 65*20

        # вставка хэдера
        header(row_num)
        # пропуск строк с учетом хэдера
        row_num += 5

    # КОТЕЛЬНЫЕ ---------------------------------------------------------------
        # получение НАЗВАНИЙ МЕСЯЦЕВ из квартала
        months = get_boiler_months(str(quarter))
        # получение ТИПОВ в котельных
        dataBT = BoilerWaste.objects.all()
        # Общая сумма значений из котельных
        q_Mno_X, q_Mno2_X, q_Mco_X, q_Mc_X, q_Mso2_X = 0,0,0,0,0

        for item in dataBT:
            # получение записей по ТИПУ из котельных
            carbon = BoilerCarbonOxWaste.objects.filter(quarter=quarter, name=item, year=year)
            nitrogen = BoilerNitrogenWaste.objects.filter(quarter=quarter, name=item, year=year)
            carb_sulf = BoilerSulfCarbWaste.objects.filter(quarter=quarter, name=item, year=year)

            # если есть Азот (1У) оксид и Азот (11) оксид
            if nitrogen.exists():
                row_num += 1
                # сумма за три месяца
                q_Mno2, q_Mno, = 0,0
                # счетчик пропуска колонок
                col_plus = 0

                ws.write(row_num, 0, item.number, f_s)
                ws.write(row_num, 2, item.fuel, f_s)

                ws.write(row_num, 3, 'Азот (1У) оксид', f_s)
                ws.write(row_num, 4, 301, f_s)
                ws.write(row_num+1, 3, 'Азот (11) оксид', f_s)
                ws.write(row_num+1, 4, 304, f_s)

                # запись в три месяца
                for elem in months:
                    for dataElem in nitrogen:
                        if dataElem.month == elem:
                            ws.write(row_num, 7+col_plus, round(dataElem.B, 4), f_s)
                            ws.write(row_num, 8+col_plus, round(dataElem.Mno2, 4), f_s)
                            ws.write(row_num+1, 8+col_plus, round(dataElem.Mno, 4), f_s)
                            # сумма за три месяца
                            q_Mno += dataElem.Mno
                            q_Mno2 += dataElem.Mno2
                    # пропуск колонок
                    col_plus += 2   

                ws.write(row_num, 13, round(q_Mno2, 4), f_s)
                ws.write(row_num+1, 13, round(q_Mno, 4), f_s)
                # сумма за загрязняющее вещество
                q_Mno2_X += q_Mno2
                q_Mno_X += q_Mno
                row_num += 1

            # если есть Углерод оксид
            if carbon.exists():
                row_num += 1
                # сумма за три месяца
                q_Mco = 0
                # счетчик пропуска колонок
                col_plus = 0

                ws.write(row_num, 3, 'Углерод оксид', f_s)
                ws.write(row_num, 4, 337, f_s)

                # запись в три месяца
                for elem in months:
                    for dataElem in carbon:
                        if dataElem.month == elem:
                            ws.write(row_num, 8+col_plus, round(dataElem.Mco, 4), f_s)
                            # сумма за три месяца
                            q_Mco += dataElem.Mco
                    # пропуск колонок
                    col_plus += 2

                ws.write(row_num, 13, round(q_Mco, 4), f_s)
                # сумма за загрязняющее вещество
                q_Mco_X += q_Mco

            # если есть Серы диоксид и Углерод черный
            if carb_sulf.exists():
                row_num += 1
                # сумма за три месяца
                q_Mc, q_Mso2 = 0,0
                # счетчик пропуска колонок
                col_plus = 0

                ws.write(row_num, 3, 'Серы диоксид', f_s)
                ws.write(row_num, 4, 330, f_s)
                ws.write(row_num+1, 3, 'Углерод черный', f_s)
                ws.write(row_num+1, 4, 328, f_s)

                # запись в три месяца
                for elem in months:
                    for dataElem in carb_sulf:
                        if dataElem.name == item and dataElem.month == elem:
                            ws.write(row_num, 8+col_plus, round(dataElem.Mso2, 4), f_s)
                            ws.write(row_num+1, 8+col_plus, round(dataElem.Mc, 4), f_s)
                            # сумма за три месяца
                            q_Mc += dataElem.Mc
                            q_Mso2 += dataElem.Mso2
                    # пропуск колонок
                    col_plus += 2

                ws.write(row_num, 13, round(q_Mso2, 4), f_s)
                ws.write(row_num+1, 13, round(q_Mc, 4), f_s)
                # сумма за загрязняющее вещество
                q_Mso2_X += q_Mso2
                q_Mc_X += q_Mc
                row_num += 1
                
    # СВАРКА ------------------------------------------------------------------
        # получение записей из СВАРКИ
        welding = WeldingWaste.objects.filter(quarter=quarter, year=year)
        # суммы за три месяца
        q_iron, q_mg = 0,0 
        # суммы за три месяца, так же будут записаны в общую сумму по загрязняющему веществу
        q_iron_t, q_mg_t = 0,0 

        # если СВАРКА есть
        if welding.exists():
            row_num += 1
            ws.write(row_num, 0, 7, f_s)
            ws.write(row_num, 2, 'Электроды', f_s)

            # создание строки
            t_iron, t_mg = '',''

            # суммы из всех найденных сварок
            for item in welding:
                q_iron += item.iron_ox_kg
                q_mg += item.mg_gg

                q_iron_t += item.iron_ox_ton
                q_mg_t += item.mg_ton

                t_iron += str(round(item.emission, 2)) + ' '
                t_mg += str(round(item.mg_gg, 2)) + ' '
            
            ws.write(row_num, 3, 'Железа оксид', f_s)
            ws.write(row_num, 4, 123, f_s)
            ws.write(row_num, 5, t_iron, f_s)
            ws.write(row_num, 11, q_iron, f_s)
            ws.write(row_num, 12, round(q_iron_t, 5), f_s)
            ws.write(row_num, 13, round(q_iron_t, 5), f_s)

            row_num += 1
            ws.write(row_num, 3, 'Марганец и его соед.', f_s)
            ws.write(row_num, 4, 143, f_s)
            ws.write(row_num, 5, t_mg, f_s)
            ws.write(row_num, 11, q_mg, f_s)
            ws.write(row_num, 12, round(q_mg_t, 5), f_s)
            ws.write(row_num, 13, round(q_mg_t, 5), f_s)

    # НЕОГРАНИЗОВАННЫЕ --------------------------------------------------------
        # получение зщаписей из НЕОРГАНИЗОВАННЫХ
        data = UnOrganizeWaste.objects.filter(year=year, quarter=quarter)
        # глобальная сумма по ПЫЛИ
        grain_dust_X = 0

        for item in data:
            # если запись не 6028
            if not item.e_s_number == '6028':
                row_num += 1

                ws.write(row_num, 0, item.e_s_number, f_s)
                ws.write(row_num, 1, item.e_s_name, f_s)
                ws.write(row_num, 3, item.harmful_substance_name, f_s)
                ws.write(row_num, 4, item.code_ZV, f_s)
                ws.write(row_num, 5, item.M, f_s)
                ws.write(row_num, 11, round(item.Tw, 1), f_s)
                ws.write(row_num, 12, item.G, f_s)
                ws.write(row_num, 13, item.G, f_s)

                # суммирует только ПЫЛЬ
                if item.harmful_substance_name[0:4] == 'Пыль':
                    grain_dust_X += item.G

    # вывод по всем загрязняющим веществам --------------------------
        ws.write(row_num+1, 1, 'Сумма по каждому загрязняющему веществу', h_s)
        ws.merge(row_num+1,row_num+8,1,2)
        # вывод сумм
        ws.write(row_num+1, 3, 'Азот (1У) оксид', f_s)
        ws.write(row_num+1, 4, 2, f_s)
        ws.write(row_num+1, 13, round(q_Mno2_X, 3), f_s) # Азот (1У) оксид

        ws.write(row_num+2, 3, 'Азот (11) оксид', f_s)
        ws.write(row_num+2, 4, 3, f_s)
        ws.write(row_num+2, 13, round(q_Mno_X, 3), f_s) # Азот (11) оксид

        ws.write(row_num+3, 3, 'Углерод оксид', f_s)
        ws.write(row_num+3, 4, 4, f_s)
        ws.write(row_num+3, 13, round(q_Mco_X, 3), f_s) # Углерод оксид

        ws.write(row_num+4, 3, 'Углерод черный', f_s)
        ws.write(row_num+4, 4, 3, f_s)
        ws.write(row_num+4, 13, round(q_Mc_X, 5), f_s) # Углерод черный

        ws.write(row_num+5, 3, 'Серы диоксид', f_s)
        ws.write(row_num+5, 4, 3, f_s)
        ws.write(row_num+5, 13, round(q_Mso2_X, 5), f_s) # Серы диоксид

        ws.write(row_num+6, 3, 'Железа оксид', f_s)
        ws.write(row_num+6, 4, 3, f_s)
        ws.write(row_num+6, 13, round(q_iron_t, 5), f_s) # Железа оксид

        ws.write(row_num+7, 3, 'Марганец и его соед.', f_s)
        ws.write(row_num+7, 4, 2, f_s)
        ws.write(row_num+7, 13, round(q_mg_t, 5), f_s) # Марганец и его соед.

        ws.write(row_num+8, 3, 'Пыль зерновая', f_s)
        ws.write(row_num+8, 4, 3, f_s)
        ws.write(row_num+8, 13, round(grain_dust_X, 4), f_s) # Пыль зерновая
        row_num += 9

    # ФУТЕР ----------------------------
        ws.write(row_num, 1, 'Итого по загрязняющим веществам:', f_s)
        ws.write(row_num+1, 1, '2 класса опасности', f_s)
        ws.write(row_num+2, 1, '3 класса опасности', f_s)
        ws.write(row_num+3, 1, '4 класса опасности', f_s)
        ws.write(row_num+4, 1, 'Итого по видам топлива', f_s)
        
        ws.write(row_num+1, 13, round(q_Mno2_X + q_mg_t, 4), f_s)
        ws.write(row_num+2, 13, round(q_Mno_X + q_Mc_X + q_Mso2_X + q_iron_t + grain_dust_X, 4), f_s)
        ws.write(row_num+3, 13, round(q_Mco_X, 4), f_s)
        ws.write(row_num+4, 13, round(q_Mno2_X + q_mg_t + q_Mno_X + q_Mc_X + q_Mso2_X + q_iron_t + grain_dust_X + q_Mco_X, 4), f_s)

        ws.write(row_num+6, 1, 'Проверил', f_s)
        ws.write(row_num+6, 3, 'Главный инженер', f_s)
        ws.write(row_num+6, 7, 'С. И. Лызо', f_s)

        # длинна колонок
        ws.col(0).width  = 5*256
        ws.col(1).width  = 9*256
        ws.col(2).width  = 13*256
        ws.col(3).width  = 16*256
        ws.col(4).width  = 7*256
        ws.col(5).width  = 10*256
        ws.col(6).width  = 6*256
        ws.col(7).width  = 14*256
        ws.col(8).width  = 10*256
        ws.col(9).width  = 14*256
        ws.col(10).width = 10*256
        ws.col(11).width = 14*256
        ws.col(12).width = 10*256
        ws.col(13).width = 10*256

        response = HttpResponse(content_type='application/ms-excel')
        response.headers['Content-Disposition'] = f'attachment; filename="POD-2_{year}_{quarter}.xls"'

        wb.save(response)

        values_for_update={
            "two":round(q_Mno2_X + q_mg_t, 4),
            "three_1":round(q_Mno_X + q_Mc_X + q_Mso2_X + q_iron_t + grain_dust_X, 4),
            "four":round(q_Mco_X, 4),
        }
        DeclarationWaste.objects.update_or_create(year=year, quarter=quarter, defaults = values_for_update)

        return response


# ПОД-1
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

        def header(row_num):
            ws.write(row_num, 0, f'Год {year}', f_s)
            ws.merge(row_num,row_num,0,1)
            ws.write(row_num, 2, 'квартал', f_s)
            ws.write(row_num, 3, quarter_rim(quarter), f_s)

            row_num += 1

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

        zerno, solid = 0,0
        harmf_name = ['Пыль зерновая','Твердые суммарно']
        names = ['Элеватор','Мельница','Крупозавод','Фасовка']

        header(row_num)
        row_num += 4

        for eType in names:
            t_data = data.filter(emission_source=eType)

            for h in harmf_name:
                f_data = t_data.filter(harmful_substance_name=h)

                if f_data.exists():
                    sum = 0

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
                            solid += item_sum
                        else:
                            zerno += item_sum

                    if h == 'Твердые суммарно':
                        eType = 'Твердые суммарно'
                    row_num += 1
                    ws.write(row_num, 10, f'Итого по {eType}', f_s_bold_sum)
                    ws.merge(row_num, row_num, 10, 13)
                    ws.write(row_num, 14, round(sum, 4), f_s_bold_sum)      

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

        values_for_update={"three_2":round(solid+zerno, 4)}
        DeclarationWaste.objects.update_or_create(year=year, quarter=quarter, defaults = values_for_update)

        return response


# Декларация
class DeclarationDownloadExcel(View):
    def get(self, request, **kwargs):

        from xlutils.copy import copy
        from xlrd import open_workbook
        from django.db.models import Sum

        # получение данных из формы
        year = int(self.request.GET.get('year'))
        quarter = self.request.GET.get('quarter')
        class2 = decimal.Decimal(self.request.GET.get('2class'))
        class3 = decimal.Decimal(self.request.GET.get('3class'))
        class4 = decimal.Decimal(self.request.GET.get('4class'))

        #шрифты
        f_s = xlwt.easyxf('font: height 240, name Times New Roman;') # стандартный

        # создание таблицы
        wb = copy(open_workbook('waste/declaration.xls',formatting_info=True))
        ws = wb.get_sheet(0)

        ws.write(7, 13, quarter_rim(quarter), f_s)
        ws.write(7, 19, year, f_s)

        ws.write(14, 4, 'II класс', f_s)
        ws.write(15, 4, 'III класс', f_s)
        ws.write(16, 4, 'IV класс', f_s)

        ws.write(14, 14, float(class2), f_s)
        ws.write(15, 14, float(class3), f_s)
        ws.write(16, 14, float(class4), f_s)

        # получение записей за выбранный год
        data = DeclarationWaste.objects.filter(year=year)
        data2class, data3class, data4class = 0,0,0
        # получение значений классов
        for item in data:
            data2class += item.two
            data3class += item.three_1 + item.three_2
            data4class += item.four
        # получение записи этого года и квартала
        data_now = DeclarationWaste.objects.get(year=year, quarter=quarter)

        ws.write(14, 10, data2class, f_s)
        ws.write(15, 10, data3class, f_s)
        ws.write(16, 10, data4class, f_s)

        ws.write(14, 12, data_now.two, f_s)
        ws.write(15, 12, data_now.three_1 + data_now.three_2, f_s)
        ws.write(16, 12, data_now.four, f_s)

        two_result = round(data_now.two * class2, 2)
        three_result = round((data_now.three_1 + data_now.three_2) * class3, 2)
        four_result = round(data_now.four * class4, 2)
        all_result = round(data_now.four * class4 + (data_now.three_1 + data_now.three_2) * class3 + data_now.two * class2, 2)
        
        ws.write(14, 22, two_result, f_s)
        ws.write(15, 22, three_result, f_s)
        ws.write(16, 22, four_result, f_s)
        ws.write(17, 22, all_result, f_s)
        
        ws.write(14, 28, two_result, f_s)
        ws.write(15, 28, three_result, f_s)
        ws.write(16, 28, four_result, f_s)
        ws.write(17, 28, all_result, f_s)

        match quarter:
            case "1": 
                ws.write(23, 28, all_result, f_s)
            case "2": 
                ws.write(24, 28, all_result, f_s)
            case "3": 
                ws.write(25, 28, all_result, f_s)
            case "4": 
                ws.write(26, 28, all_result, f_s)

        ws.write(23, 26, str(year) + ' года', f_s)
        ws.write(24, 26, str(year) + ' года', f_s)
        ws.write(25, 26, str(year) + ' года', f_s)
        ws.write(26, 26, str(year+1) + ' года (год, следующий за налоговым)', f_s)
                
        # скачивание файла
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=declaration.xls"

        wb.save(response)

        return response
