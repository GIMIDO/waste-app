from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(OrganizeWaste)
admin.site.register(WeldingWaste)
admin.site.register(UnOrganizeWaste)

admin.site.register(BoilerWaste)
admin.site.register(BoilerCarbonOxWaste)
admin.site.register(BoilerNitrogenWaste)

admin.site.register(BoilerSulfCarbWaste)

admin.site.register(DeclarationWaste)