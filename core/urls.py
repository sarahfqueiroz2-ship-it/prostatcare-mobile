from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('sair/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('relatorio/', views.relatorio_view, name='relatorio'),
    path('relatorio/pdf/<int:paciente_id>/', views.relatorio_pdf_view, name='relatorio_pdf'),
]
