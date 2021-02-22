from django.urls import path

from .views import boms, boms_edit, boms_delete, \
    boms_interactive, boms_printable, boms_import, boms_export

urlpatterns = [
    path('boms/', boms, name='boms'),
    path('boms/edit/', boms_edit, name='boms_edit'),
    path('boms/delete/', boms_delete, name='boms_delete'),
    path('boms/interactive/', boms_interactive, name='boms_interactive'),
    path('boms/printable/', boms_printable, name='boms_printable'),
    path('boms/import/', boms_import, name='boms_import'),
    path('boms/export/', boms_export, name='boms_export'),
]