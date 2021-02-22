from django.urls import path

from .views import manufacturer_parts
from .views import manufacturer_parts_edit
from .views import manufacturer_parts_delete
from .views import manufacturer_parts_search
from .views import manufacturer_part_links_select
from .views import manufacturer_part_links_create
from .views import manufacturer_part_links_break

urlpatterns = [
    path('manufacturer_parts/', manufacturer_parts,
        name='manufacturer_parts'),
    path('manufacturer_parts/edit/', manufacturer_parts_edit,
        name='manufacturer_parts_edit'),
    path('manufacturer_parts/delete/', manufacturer_parts_delete,
        name='manufacturer_parts_delete'),
    path('manufacturer_parts/search/', manufacturer_parts_search,
        name='manufacturer_parts_search'),
    path('manufacturer_part_links/select/', manufacturer_part_links_select,
        name='manufacturer_part_links_select'),
    path('manufacturer_part_links/create/', manufacturer_part_links_create,
        name='manufacturer_part_links_create'),
    path('manufacturer_part_links/break/', manufacturer_part_links_break,
        name='manufacturer_part_links_break')
]