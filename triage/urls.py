from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("entrar/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", views.register, name="register"),
    path("painel/", views.dashboard, name="dashboard"),
    path("meus-casos/", views.patient_dashboard, name="patient_dashboard"),
    path("nova-triagem/", views.submit_case, name="submit_case"),
    path("caso/<str:code>/", views.case_result, name="case_result"),
    path("caso/<str:code>/agendar/<int:doctor_id>/", views.schedule, name="schedule"),
    path("caso/<str:code>/cancelar/", views.cancel_appointment, name="cancel_appointment"),
    path("painel-clinico/", views.clinical_queue, name="clinical_queue"),
    path("painel-clinico/<str:code>/revisar/", views.review_case, name="review_case"),
]
