from .models import *
import decimal
import math


def get_months(quarter):
    
    if (quarter == '1'):
        return {'1': 'Январь','2': 'Февраль','3': 'Март'}
    elif (quarter == '2'):
        return {'1': 'Апрель','2': 'Май','3': 'Июнь'}
    elif (quarter == '3'):
        return {'1': 'Июль','2': 'Август','3': 'Сентябрь'}
    elif (quarter == '4'):
        return {'1': 'Октябрь','2': 'Ноябрь','3': 'Декабрь'}
    else:
        return {'1': 'Месяц 1','2': 'Месяц 2','3': 'Месяц 3'}

def get_boiler_months(quarter):
    
    if (quarter == '1'):
        return ['Январь', 'Февраль', 'Март']
    elif (quarter == '2'):
        return ['Апрель', 'Май', 'Июнь']
    elif (quarter == '3'):
        return ['Июль', 'Август', 'Сентябрь']
    elif (quarter == '4'):
        return ['Октябрь', 'Ноябрь', 'Декабрь']
    else:
        return ['М1','М2','М3']

# --- #

def organize_waste_calc_all(data):

    for elem in data:
        elem.all = elem.first_month + elem.second_month + elem.third_month
        elem.G = round(elem.all * elem.M * decimal.Decimal(3600) * decimal.Decimal(0.000001), 9)

        elem.save()
    
def organize_waste_calc_all_G(data):


    all_G = 0
    all_G2 = 0
    hs = get_hs_o()

    for elem in data:
        if elem.harmful_substance_name == hs[0]:
            all_G += elem.G
            elem.G = round(elem.G, 4)

        elif elem.harmful_substance_name == hs[1]:
            all_G2 += elem.G
            elem.G = round(elem.G, 4)

    return [round(all_G, 4), round(all_G2, 4)]

def get_hs_o():
    return ['Пыль зерновая', 'Твердые суммарно']


# --- #

def welding_waste_calc(data):

    for elem in data:
        elem.iron_ox_ton = round(elem.emission * elem.iron_ox_kg * decimal.Decimal(0.000001), 9)
        elem.mg_ton = round(elem.iron_ox_kg * elem.mg_gg * decimal.Decimal(0.000001), 9)
        elem.hyd_flu_ton = round(elem.iron_ox_kg * elem.hyd_flu_gkg * decimal.Decimal(0.000001), 9)

        elem.save()

def get_quarters(data):

    q = 0
    quarters = []
    for elem in data:
        if (elem.quarter > q):
            quarters.append(elem.quarter)
            q = elem.quarter

    return quarters

def welding_waste_sum_calc(data):

    if (data.exists()):
        pass
    else:
        return None

    q = 1

    sum_calc = {}

    sum_iron_ox_kg, sum_iron_ox_ton, sum_mg_gg, sum_mg_ton, sum_hyd_flu_gkg, sum_hyd_flu_ton = 0,0,0,0,0,0

    year_i_kg, year_i_t, year_m_g, year_m_t, year_hf_g, year_hf_t = 0,0,0,0,0,0

    while (q <= 4):

        for elem in data:

            if (q == elem.quarter):
                sum_iron_ox_kg += elem.iron_ox_kg
                sum_iron_ox_ton += elem.iron_ox_ton
                sum_mg_gg += elem.mg_gg
                sum_mg_ton += elem.mg_ton
                sum_hyd_flu_gkg += elem.hyd_flu_gkg
                sum_hyd_flu_ton += elem.hyd_flu_ton

                year_i_kg += elem.iron_ox_kg
                year_i_t += elem.iron_ox_ton
                year_m_g += elem.mg_gg
                year_m_t += elem.mg_ton
                year_hf_g += elem.hyd_flu_gkg
                year_hf_t += elem.hyd_flu_ton

            elem.iron_ox_ton = round(elem.iron_ox_ton, 5)
            elem.mg_ton = round(elem.mg_ton, 6)
            elem.hyd_flu_ton = round(elem.hyd_flu_ton, 7)

        json_i = {
                    "s_i_kg": str(round(sum_iron_ox_kg, 5)),
                    "s_i_t": str(round(sum_iron_ox_ton, 5)),
                    "s_m_g": str(round(sum_mg_gg, 5)),
                    "s_m_t": str(round(sum_mg_ton, 5)),
                    "s_hf_g": str(round(sum_hyd_flu_gkg, 7)),
                    "s_hf_t": str(round(sum_hyd_flu_ton, 7))
                }

        sum_calc[str(q)] = json_i
        q += 1
        sum_iron_ox_kg, sum_iron_ox_ton, sum_mg_gg, sum_mg_ton, sum_hyd_flu_gkg, sum_hyd_flu_ton = 0,0,0,0,0,0

    json_y = {
            "y_i_kg": str(round(year_i_kg, 5)),
            "y_i_t": str(round(year_i_t, 5)),
            "y_m_g": str(round(year_m_g, 5)),
            "y_m_t": str(round(year_m_t, 5)),
            "y_hf_g": str(round(year_hf_g, 7)),
            "y_hf_t": str(round(year_hf_t, 7))
        }
    sum_calc["year"] = json_y

    return sum_calc

# --- #

def unorganize_waste_calculate(data):

    for elem in data:
        elem.all = elem.first_month + elem.second_month + elem.third_month
        elem.Tw = round(elem.T * elem.all / decimal.Decimal(3600), 9)
        elem.G = round(elem.Tw * elem.M * decimal.Decimal(3600) * decimal.Decimal(0.000001), 9)

        elem.all = round(elem.all, 3)

        elem.save()

def unorganize_calc_data(data, obj_type):
    match obj_type:
        case "Мельзавод":
            h_s = ['Пыль зерновая м/з', 'Пыль мучная']
            p_1, p_2 = 0, 0

            for elem in data:
                if elem.harmful_substance_name == h_s[0]:
                    p_1 += elem.G
                elif elem.harmful_substance_name == h_s[1]:
                    p_2 += elem.G

                elem.Tw = round(elem.Tw, 1)
                elem.G = round(elem.G, 4)
            
            return [round(p_1, 4), round(p_2, 4)]

        case "Крупозавод":
            h_s = ['Пыль зерновая к/з']
            p_1 = 0

            for elem in data:
                p_1 += elem.G
            
                elem.Tw = round(elem.Tw, 1)
                elem.G = round(elem.G, 4)

            return [p_1]

        case "РБ":
            h_s = ['Пыль зерновая р/б']
            p_1 = 0

            for elem in data:
                p_1 += elem.G
            
                elem.Tw = round(elem.Tw, 1)
                elem.G = round(elem.G, 4)

            return [p_1]

        case "Фосфин":
            h_s = ['фосфин (водород фосфористый)']
            p_1 = 0

            for elem in data:
                p_1 += elem.G
            
                elem.Tw = round(elem.Tw, 1)
                elem.G = round(elem.G, 4)

            return [p_1]
    
def get_hs(obj_type):

    match obj_type:
        case "Мельзавод":
            return ['Пыль зерновая м/з', 'Пыль мучная']

        case "Крупозавод":
            return ['Пыль зерновая к/з']

        case "РБ":
            return ['Пыль зерновая р/б']

        case "Фосфин":
            return['фосфин (водород фосфористый)']

# --- #

def boiler_carbon_waste_calc(data):

    for elem in data:
        elem.Qh_calc = round(elem.Qh * elem.name.K * decimal.Decimal(0.001), 9)
        elem.Cco = round(elem.Qh_calc * elem.name.q3 * elem.name.R, 9)
        elem.Mco = round(elem.B * elem.Cco * decimal.Decimal(0.001), 9)

        elem.save()

def boiler_nitrogen_waste_calc(data):

    for elem in data:
        elem.Q = round(elem.Qh * elem.name.K * decimal.Decimal(0.001), 9)
        elem.Bs = round(elem.B / (decimal.Decimal(3.6) * elem.T), 9)
        elem.Knox = round((decimal.Decimal(0.01) * decimal.Decimal(math.sqrt(decimal.Decimal(1.59) * elem.Q * elem.Bs))) + decimal.Decimal(0.03), 9)
        elem.Mnox = round(decimal.Decimal(0.001) * elem.B * elem.Q * elem.Knox * elem.name.Bk * elem.name.Bt, 9)
        elem.Mno2 = round(decimal.Decimal(0.8) * elem.Mnox, 9)
        elem.Mno = round(decimal.Decimal(0.13) * elem.Mnox, 9)

        elem.save()

def boiler_CB_SD_calc(data):

    for elem in data:
        elem.Mso2 = round(decimal.Decimal(0.02) * elem.B * decimal.Decimal(0.4) * (1 - decimal.Decimal(0.02)),4) 
        elem.Mc = round(decimal.Decimal(0.01) * elem.B * decimal.Decimal(0.02) * decimal.Decimal(42.44 / 32.68),4)

        elem.save()

def boiler_carbon_waste_month(data, months):

    B1, B2, B3 = 0, 0, 0
    Mco1, Mco2, Mco3 = 0, 0, 0

    for elem in data:
        if elem.month == months[0]:
            B1 += elem.B
            Mco1 += elem.Mco

        elif elem.month == months[1]:
            B2 += elem.B
            Mco2 += elem.Mco

        elif elem.month == months[2]:
            B3 += elem.B
            Mco3 += elem.Mco

        
        elem.Qh_calc = round(elem.Qh_calc, 4)
        elem.Cco = round(elem.Cco, 4)
        elem.Mco = round(elem.Mco, 4)

    return [[months[0], B1, round(Mco1, 4)], [months[1], B2, round(Mco2, 4)], [months[2], B3, round(Mco3, 4)]]

def boiler_nitrogen_waste_month(data, months):

    B1, B2, B3 = 0, 0, 0
    Mno1, Mno2, Mno3 = 0, 0, 0
    Mno2_1, Mno2_2, Mno2_3 = 0, 0, 0

    for elem in data:
        if elem.month == months[0]:
            B1 += elem.B
            Mno1 += elem.Mno
            Mno2_1 += elem.Mno2

        elif elem.month == months[1]:
            B2 += elem.B
            Mno2 += elem.Mno
            Mno2_2 += elem.Mno2

        elif elem.month == months[2]:
            B3 += elem.B
            Mno3 += elem.Mno
            Mno2_3 += elem.Mno2

        
        elem.Q = round(elem.Q, 4)
        elem.Bs = round(elem.Bs, 4)
        elem.Knox = round(elem.Knox, 4)
        elem.Mnox = round(elem.Mnox, 4)
        elem.Mno2 = round(elem.Mno2, 4)
        elem.Mno = round(elem.Mno, 4)

    return [[months[0], B1, round(Mno1, 4), round(Mno2_1, 4)], [months[1], B2, round(Mno2, 4), round(Mno2_2, 4)], [months[2], B3, round(Mno3, 4), round(Mno2_3, 4)]]

def boiler_CB_SD_q(data):

    Mc_sum, Mso2_sum = 0,0

    for elem in data:
        Mc_sum += elem.Mc
        Mso2_sum += elem.Mso2

    return [Mc_sum, Mso2_sum]

# --- #

def pod_1_save(year, quarter):

    data = OrganizeWaste.objects.filter(year=year, quarter=quarter)

    zerno, solid = 0,0
    harmf_name = ['Пыль зерновая','Твердые суммарно']
    names = ['Элеватор','Мельница','Крупозавод','Фасовка']

    for eType in names:
        t_data = data.filter(emission_source=eType)

        for h in harmf_name:
            f_data = t_data.filter(harmful_substance_name=h)

            if f_data.exists():
                sum = 0

                for item in f_data:
                    item_sum = 0
                    
                    item_sum += item.M * item.first_month * 3600 * decimal.Decimal(0.000001)
                    item_sum += item.M * item.second_month * 3600 * decimal.Decimal(0.000001)
                    item_sum += item.M * item.third_month * 3600 * decimal.Decimal(0.000001)
                    sum += item_sum

                    if item.harmful_substance_name == 'Твердые суммарно':
                        solid += item_sum
                    else:
                        zerno += item_sum

    values_for_update = {"three_2": round(solid+zerno, 4)}
    DeclarationWaste.objects.update_or_create(
        year=year, quarter=quarter, defaults=values_for_update)

def pod_2_save(year, quarter):

    months = get_boiler_months(str(quarter))
    dataBT = BoilerWaste.objects.all()
    q_Mno_X, q_Mno2_X, q_Mco_X, q_Mc_X, q_Mso2_X = 0, 0, 0, 0, 0

    for item in dataBT:
        carbon = BoilerCarbonOxWaste.objects.filter(
            quarter=quarter, name=item, year=year)
        nitrogen = BoilerNitrogenWaste.objects.filter(
            quarter=quarter, name=item, year=year)
        carb_sulf = BoilerSulfCarbWaste.objects.filter(
            quarter=quarter, name=item, year=year)

        if nitrogen.exists():
            q_Mno2, q_Mno, = 0, 0

            for elem in months:
                for dataElem in nitrogen:
                    if dataElem.month == elem:
                        q_Mno += dataElem.Mno
                        q_Mno2 += dataElem.Mno2

            q_Mno2_X += q_Mno2
            q_Mno_X += q_Mno

        if carbon.exists():
            q_Mco = 0

            for elem in months:
                for dataElem in carbon:
                    if dataElem.month == elem:
                        q_Mco += dataElem.Mco

            q_Mco_X += q_Mco

        if carb_sulf.exists():
            q_Mc, q_Mso2 = 0, 0

            for elem in months:
                for dataElem in carb_sulf:
                    if dataElem.name == item and dataElem.month == elem:
                        q_Mc += dataElem.Mc
                        q_Mso2 += dataElem.Mso2

            q_Mso2_X += q_Mso2
            q_Mc_X += q_Mc

    welding = WeldingWaste.objects.filter(quarter=quarter, year=year)
    q_iron, q_mg = 0, 0
    q_iron_t, q_mg_t = 0, 0

    if welding.exists():
        t_iron, t_mg = '', ''

        for item in welding:
            q_iron += item.iron_ox_kg
            q_mg += item.mg_gg

            q_iron_t += item.iron_ox_ton
            q_mg_t += item.mg_ton

            t_iron += str(round(item.emission, 2)) + ' '
            t_mg += str(round(item.mg_gg, 2)) + ' '

    data = UnOrganizeWaste.objects.filter(year=year, quarter=quarter)
    grain_dust_X = 0

    for item in data:
        if not item.e_s_number == '6028':
            if item.harmful_substance_name[0:4] == 'Пыль':
                grain_dust_X += item.G

    values_for_update = {
        "two": round(q_Mno2_X + q_mg_t, 4),
        "three_1": round(q_Mno_X + q_Mc_X + q_Mso2_X + q_iron_t + grain_dust_X, 4),
        "four": round(q_Mco_X, 4),
    }
    
    DeclarationWaste.objects.update_or_create(
        year=year, quarter=quarter, defaults=values_for_update)
