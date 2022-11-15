
from django.views.generic import View
from django.http import HttpResponse

import xlwt

from .utils import *
from .models import *


class DownloadExcel(View):

    CHOISE = {
        'ow': OrganizeWaste
    }

    def get(self, request, **kwargs):

        toc = kwargs.get('toc')
        emission_source = kwargs.get('e_s')
        year = kwargs.get('year')
        quarter = kwargs.get('q')

        data = self.CHOISE[toc].objects.filter(
            emission_source=emission_source,
            year=year,
            quarter=quarter
        )

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

        for my_row in data:
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
        
        ws.write(row_num + 1, 7, 'Итого орган. ист. элеватора:', font_style)
        ws.write(row_num + 1, 8, organize_waste_calc_all_G(data), font_style)

        wb.save(response)
        return response