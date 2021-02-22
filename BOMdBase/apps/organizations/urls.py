from django.urls import path

from .views import organizations
from .views import organizations_edit
from .views import organizations_delete

urlpatterns = [
    path('organizations/', organizations,
        name='organizations'),
    path('organizations/edit/', organizations_edit,
        name='organizations_edit'),
    path('organizations/delete/', organizations_delete,
        name='organizations_delete')
]