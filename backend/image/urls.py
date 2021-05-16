from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.InputImageView.as_view()),
    path('getdate/', views.InfoCsv.as_view())
]