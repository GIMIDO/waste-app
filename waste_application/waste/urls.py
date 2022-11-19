from django.urls import path


from .views import *
from .excel_creator import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('organize/waste/main/', OrganizeWasteView.as_view(), name='organize-waste-main'),
    path('organize/waste/create/<str:e_s>/<int:year>/<int:q>/', CreateOrganizeWasteView.as_view(), name='organize-waste-create'),
    path('organize/waste/update/<str:e_s>/<int:year>/<int:q>/<int:pk>/', UpdateOrganizeWasteView.as_view(), name='organize-waste-update'),
    path('organize/waste/delelte/<int:pk>/', DeleteOrganizeWasteView.as_view(), name='organize-waste-delete'),
    path('download/excel/<str:toc>/<str:e_s>/<int:year>/<int:q>/', OrganizeDownloadExcel.as_view(), name='excel-download'),

    path('welding/waste/main/', WeldingWasteView.as_view(), name='welding-waste-main'),
    path('welding/waste/create/<int:year>/', CreateWeldingWasteView.as_view(), name='welding-waste-create'),
    path('welding/waste/update/<int:year>/<int:pk>/', UpdateWeldingWasteView.as_view(), name='welding-waste-update'),
    path('welding/waste/delelte/<int:pk>/', DeleteWeldingWasteView.as_view(), name='welding-waste-delete'),
    path('welding/excel/<int:year>/', WeldingDownloadExcel.as_view(), name='excel-download-welding'),

    path('unorganize/waste/main/', UnOrganizeWasteView.as_view(), name='unorganize-waste-main'),
    path('unorganize/waste/create/<str:obj_type>/<int:year>/<int:quarter>/', CreateUnOrganizeWasteView.as_view(), name='unorganize-waste-create'),
    path('unorganize/waste/update/<str:obj_type>/<int:year>/<int:quarter>/<int:pk>/', UpdateUnOrganizeWasteView.as_view(), name='unorganize-waste-update'),
    path('unorganize/waste/delelte/<int:pk>/', DeleteUnOrganizeWasteView.as_view(), name='unorganize-waste-delete'),
    path('unorganize/excel/<str:obj_type>/<int:year>/<int:quarter>/', UnOrganizeDownloadExcel.as_view(), name='excel-download-unorganize'),
]