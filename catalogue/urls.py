from django.urls import path
from .views import CatalogueView

urlpatterns = [
    path('list/', CatalogueView.as_view(), name='catalogue-list'),
]