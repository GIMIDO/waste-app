from django.urls import path


from .views import *
from .excel_creator import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('organize/waste/main/', OrganizeWasteView.as_view(), name='organize-waste-main'),
    path('organize/waste/create/<str:e_s>/<int:year>/<int:q>/', CreateOrganizeWasteView.as_view(), name='organize-waste-create'),
    path('organize/waste/update/<str:e_s>/<int:year>/<int:q>/<int:pk>/', UpdateOrganizeWasteView.as_view(), name='organize-waste-update'),
    path('organize/waste/delelte/<int:pk>/', DeleteOrganizeWasteView.as_view(), name='organize-waste-delete'),

    path('download/excel/<str:toc>/<str:e_s>/<int:year>/<int:q>/', DownloadExcel.as_view(), name='excel-download'),
]