from django.urls import path

from .views import part_notes
from .views import part_notes_edit
from .views import part_notes_delete

urlpatterns = [
    path('part_notes/', part_notes, name='part_notes'),
    path('part_notes/edit/', part_notes_edit, name='part_notes_edit'),
    path('part_notes/delete/', part_notes_delete, name='part_notes_delete')
]