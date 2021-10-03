from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin,ImportExportMixin

class ImportExportAdmin(ImportExportActionModelAdmin):
    pass

# Register your models here.
from .models import *
from .semi_models import *

admin.site.register(Qpen)
admin.site.register(OpenLeading)
admin.site.register(Closed)

admin.site.register(LifeVector)
admin.site.register(Dummy)

admin.site.register(Intensity,ImportExportAdmin)
admin.site.register(Feelings,ImportExportAdmin)
admin.site.register(Category,ImportExportAdmin)
admin.site.register(SubCategory,ImportExportAdmin)
admin.site.register(Genre,ImportExportAdmin)
admin.site.register(Decade,ImportExportAdmin)