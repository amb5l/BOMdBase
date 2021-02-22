from django.urls import path

from .views import supplier_parts
from .views import supplier_parts_edit
from .views import supplier_parts_delete
from .views import supplier_parts_search
from .views import supplier_part_link_select
from .views import supplier_part_link_create
from .views import supplier_part_link_break

urlpatterns = [
    path('supplier_parts/', supplier_parts,
        name='supplier_parts'),
    path('supplier_parts/edit/', supplier_parts_edit,
        name='supplier_parts_edit'),
    path('supplier_parts/delete/', supplier_parts_delete,
        name='supplier_parts_delete'),
    path('supplier_parts/search/', supplier_parts_search,
        name='supplier_parts_search'),
    path('supplier_part_link/select/', supplier_part_link_select,
        name='supplier_part_link_select'),
    path('supplier_part_link/create/', supplier_part_link_create,
        name='supplier_part_link_create'),
    path('supplier_part_link/break/', supplier_part_link_break,
        name='supplier_part_link_break')
]