from django.urls import path
from . import views
import uuid

urlpatterns = [
    path('', views.generate_certificate),
    path('display_certificate/<int:certificate_id>/', views.display_certificate, name='display_certificate'),
    path('display_certificate/<int:certificate_id>/download/', views.download_certificate_pdf, name='download_certificate_pdf'),
    path('verify/<int:certificate_id>/', views.verify_certificate, name='verify_certificate'),    
]