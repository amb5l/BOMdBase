from django.urls import path

from .views import logical_part_links_select, logical_part_links_create, \
    logical_part_links_break

urlpatterns = [
    path('logical_part_links/select/', logical_part_links_select,
        name='logical_part_links_select'),
    path('logical_part_links/create/', logical_part_links_create,
        name='logical_part_links_create'),
    path('logical_part_links/break/', logical_part_links_break,
        name='logical_part_links_break'),
]