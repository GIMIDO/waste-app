from django.urls import path

from .views import *
from .excel_creator import *


urlpatterns = [
    # --- --- --- ГЛАВНАЯ --- --- ---
    # главная
    path('', HomeView.as_view(), name='home'),

    # логин
    path('login/', LoginView.as_view(), name='login'),
    # выход из аккаунта
    path('logout/', LogoutView.as_view(), name='logout'),
    

    # --- --- --- ОТЧЕТЫ --- --- ---
    # страничка с ПОД-1 и ПОД-2
    path('report/', NalogView.as_view(), name='report'),

    # страничка с Декларацией
    path('declaration/', DeclarationView.as_view(), name='declaration'),
    # скачать ПОД-1
    path('download/IRS/excel/', IRSOrganizeDownloadExcel.as_view(), name='IRS-excel-download'),
    # скачать ПОД-2
    path('download/IRS2/excel/', IRS2OrganizeDownloadExcel.as_view(), name='IRS-excel-download2'),

    # скачать Декларацию
    path('download/declaration/excel/', DeclarationDownloadExcel.as_view(), name='declaration-excel-download'),


    # --- --- --- ОРГАНИЗОВАННЫЕ --- --- ---
    # страничка с выводом данных
    path('organize/waste/main/', OrganizeWasteView.as_view(), name='organize-waste-main'),

    # страничка создания
    path('organize/waste/create/<str:e_s>/<int:year>/<int:q>/', CreateOrganizeWasteView.as_view(), name='organize-waste-create'),
    # страничка изменения
    path('organize/waste/update/<str:e_s>/<int:year>/<int:q>/<int:pk>/', UpdateOrganizeWasteView.as_view(), name='organize-waste-update'),
    # страничка удаления
    path('organize/waste/delelte/<int:pk>/', DeleteOrganizeWasteView.as_view(), name='organize-waste-delete'),

    # скачать в виде Excel-таблицы
    path('download/excel/<str:e_s>/<int:year>/<int:q>/', OrganizeDownloadExcel.as_view(), name='excel-download'),


    # --- --- --- СВАРКА --- --- --- 
    # страничка с выводом данных
    path('welding/waste/main/', WeldingWasteView.as_view(), name='welding-waste-main'),

    # страничка создания
    path('welding/waste/create/<int:year>/', CreateWeldingWasteView.as_view(), name='welding-waste-create'),
    # страничка изменения
    path('welding/waste/update/<int:year>/<int:pk>/', UpdateWeldingWasteView.as_view(), name='welding-waste-update'),
    # страничка удаления
    path('welding/waste/delelte/<int:pk>/', DeleteWeldingWasteView.as_view(), name='welding-waste-delete'),

    # скачать в виде Excel-таблицы
    path('welding/excel/<int:year>/', WeldingDownloadExcel.as_view(), name='excel-download-welding'),


    # --- --- --- НЕОРГАНИЗОВАННЫЕ --- --- ---
    # страничка с выводом данных
    path('unorganize/waste/main/', UnOrganizeWasteView.as_view(), name='unorganize-waste-main'),

    # страничка создания
    path('unorganize/waste/create/<str:obj_type>/<int:year>/<int:quarter>/', CreateUnOrganizeWasteView.as_view(), name='unorganize-waste-create'),
    # страничка изменения
    path('unorganize/waste/update/<str:obj_type>/<int:year>/<int:quarter>/<int:pk>/', UpdateUnOrganizeWasteView.as_view(), name='unorganize-waste-update'),
    # страничка удаления
    path('unorganize/waste/delelte/<int:pk>/', DeleteUnOrganizeWasteView.as_view(), name='unorganize-waste-delete'),

    # скачать в виде Excel-таблицы
    path('unorganize/excel/<str:obj_type>/<int:year>/<int:quarter>/', UnOrganizeDownloadExcel.as_view(), name='excel-download-unorganize'),


    # --- --- --- КОТЕЛЬНЫЕ --- --- ---
    # страничка с выводом данных
    path('boiler/waste/main/', BoilerWasteView.as_view(), name='boiler-waste-main'),
    
    # страничка создания Азот диоксид и азот оксид
    path('boiler/waste/create/nitrogen/<int:year>/<int:q>/', CreateBoilerNitrogenWasteView.as_view(), name='boiler-nitrogen-waste-create'),
    # страничка создания Углерод оксид
    path('boiler/waste/create/carbon/<int:year>/<int:q>/', CreateBoilerCarbonOxWasteView.as_view(), name='boiler-carbon-waste-create'),
    # страничка создания дизельное топливо и сажа
    path('boiler/waste/create/sulf-carb/<int:year>/<int:q>/', CreateBoilerSulfCarbWasteView.as_view(), name='boiler-sulf_carb-waste-create'),

    # страничка изменения Азот диоксид и азот оксид
    path('boiler/waste/update/nitrogen/<int:year>/<int:q>/<int:pk>/', UpdateBoilerNitrogenWasteView.as_view(), name='boiler-nitrogen-waste-update'),
    # страничка изменения Углерод оксид
    path('boiler/waste/update/carbon/<int:year>/<int:q>/<int:pk>/', UpdateBoilerCarbonOxWasteView.as_view(), name='boiler-carbon-waste-update'),
    # страничка изменения дизельное топливо и сажа
    path('boiler/waste/update/sulf-carb/<int:year>/<int:q>/<int:pk>/', UpdateBoilerSulfCarbWasteView.as_view(), name='boiler-sulf_carb-waste-update'),
    
    # страничка удаления Азот диоксид и азот оксид
    path('boiler/waste/delete/nitrogen/<int:pk>/', DeleteBoilerNitrogenWasteView.as_view(), name='boiler-nitrogen-waste-delete'),
    # страничка удаления Углерод оксид
    path('boiler/waste/delete/carbon/<int:pk>/', DeleteBoilerCarbonOxWasteView.as_view(), name='boiler-carbon-waste-delete'),
    # страничка удаления дизельное топливо и сажа
    path('boiler/waste/delete/sulf-carb/<int:pk>/', DeleteBoilerSulfCarbWasteView.as_view(), name='boiler-sulf_carb-waste-delete'),

    # скачать в виде Excel-таблицы
    path('boiler/excel/<int:year>/<int:quarter>/', BoilerDownloadExcel.as_view(), name='excel-download-boiler'),
]