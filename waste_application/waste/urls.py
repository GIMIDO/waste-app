from django.urls import path


from .views import *
from .excel_creator import *


urlpatterns = [
    # --- --- --- ГЛАВНАЯ
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # --- --- --- ОРГАНИЗОВАННЫЕ
    path('organize/waste/main/', OrganizeWasteView.as_view(), name='organize-waste-main'),
    path('organize/waste/create/<str:e_s>/<int:year>/<int:q>/', CreateOrganizeWasteView.as_view(), name='organize-waste-create'),
    path('organize/waste/update/<str:e_s>/<int:year>/<int:q>/<int:pk>/', UpdateOrganizeWasteView.as_view(), name='organize-waste-update'),
    path('organize/waste/delelte/<int:pk>/', DeleteOrganizeWasteView.as_view(), name='organize-waste-delete'),

    path('download/excel/<str:e_s>/<int:year>/<int:q>/', OrganizeDownloadExcel.as_view(), name='excel-download'),
    path('download/IRS/excel/<str:e_s>/<int:year>/<int:q>/', IRSOrganizeDownloadExcel.as_view(), name='IRS-excel-download'),

    # --- --- --- СВАРКА
    path('welding/waste/main/', WeldingWasteView.as_view(), name='welding-waste-main'),
    path('welding/waste/create/<int:year>/', CreateWeldingWasteView.as_view(), name='welding-waste-create'),
    path('welding/waste/update/<int:year>/<int:pk>/', UpdateWeldingWasteView.as_view(), name='welding-waste-update'),
    path('welding/waste/delelte/<int:pk>/', DeleteWeldingWasteView.as_view(), name='welding-waste-delete'),

    path('welding/excel/<int:year>/', WeldingDownloadExcel.as_view(), name='excel-download-welding'),

    # --- --- --- НЕОРГАНИЗОВАННЫЕ
    path('unorganize/waste/main/', UnOrganizeWasteView.as_view(), name='unorganize-waste-main'),
    path('unorganize/waste/create/<str:obj_type>/<int:year>/<int:quarter>/', CreateUnOrganizeWasteView.as_view(), name='unorganize-waste-create'),
    path('unorganize/waste/update/<str:obj_type>/<int:year>/<int:quarter>/<int:pk>/', UpdateUnOrganizeWasteView.as_view(), name='unorganize-waste-update'),
    path('unorganize/waste/delelte/<int:pk>/', DeleteUnOrganizeWasteView.as_view(), name='unorganize-waste-delete'),

    path('unorganize/excel/<str:obj_type>/<int:year>/<int:quarter>/', UnOrganizeDownloadExcel.as_view(), name='excel-download-unorganize'),

    # --- --- --- КОТЕЛЬНЫЕ
    path('boiler/waste/main/', BoilerWasteView.as_view(), name='boiler-waste-main'),

    path('boiler/waste/create/nitrogen/<int:year>/<int:q>/', CreateBoilerNitrogenWasteView.as_view(), name='boiler-nitrogen-waste-create'),
    path('boiler/waste/create/carbon/<int:year>/<int:q>/', CreateBoilerCarbonOxWasteView.as_view(), name='boiler-carbon-waste-create'),
    path('boiler/waste/create/sulf-carb/<int:year>/<int:q>/', CreateBoilerSulfCarbWasteView.as_view(), name='boiler-sulf_carb-waste-create'),

    path('boiler/waste/update/nitrogen/<int:year>/<int:q>/<int:pk>/', UpdateBoilerNitrogenWasteView.as_view(), name='boiler-nitrogen-waste-update'),
    path('boiler/waste/update/carbon/<int:year>/<int:q>/<int:pk>/', UpdateBoilerCarbonOxWasteView.as_view(), name='boiler-carbon-waste-update'),
    path('boiler/waste/update/sulf-carb/<int:year>/<int:q>/<int:pk>/', UpdateBoilerSulfCarbWasteView.as_view(), name='boiler-sulf_carb-waste-update'),
    
    path('boiler/waste/delete/nitrogen/<int:pk>/', DeleteBoilerNitrogenWasteView.as_view(), name='boiler-nitrogen-waste-delete'),
    path('boiler/waste/delete/carbon/<int:pk>/', DeleteBoilerCarbonOxWasteView.as_view(), name='boiler-carbon-waste-delete'),
    path('boiler/waste/delete/sulf-carb/<int:pk>/', DeleteBoilerSulfCarbWasteView.as_view(), name='boiler-sulf_carb-waste-delete'),

    path('boiler/excel/<int:year>/<int:quarter>/', BoilerDownloadExcel.as_view(), name='excel-download-boiler'),
]