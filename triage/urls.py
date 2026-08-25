from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), path("nova-triagem/", views.submit_case, name="submit_case"),
    path("caso/<str:code>/", views.case_result, name="case_result"),
    path("caso/<str:code>/agendar/<int:doctor_id>/", views.schedule, name="schedule"),
    path("caso/<str:code>/cancelar/", views.cancel_appointment, name="cancel_appointment"),
    path("painel-clinico/", views.clinical_queue, name="clinical_queue"),
]
