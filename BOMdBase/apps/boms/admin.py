from django.contrib import admin

from .models import BOM
from .models import BOMItem

admin.site.register(BOM)
admin.site.register(BOMItem)