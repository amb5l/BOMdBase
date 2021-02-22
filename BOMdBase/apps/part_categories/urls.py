from django.urls import path

from .views import part_categories
from .views import part_categories_edit
from .views import part_categories_delete

urlpatterns = [
    path('part_categories/', part_categories,
        name='part_categories'),
    path('part_categories/edit/', part_categories_edit,
        name='part_categories_edit'),
    path('part_categories/delete/', part_categories_delete,
        name='part_categories_delete'),
]