from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CaseForm
from .models import Appointment, Case, Doctor
from .services import calculate_priority

def home(request):
    return render(request, "triage/home.html", {"cases_count": Case.objects.count(), "doctors_count": Doctor.objects.count()})

def submit_case(request):
    form = CaseForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        case = form.save(commit=False)
        case.priority, case.score, case.reasons = calculate_priority(form.cleaned_data)
        case.save()
        return redirect("case_result", code=case.code)
    return render(request, "triage/submit.html", {"form": form})

def case_result(request, code):
    case = get_object_or_404(Case, code=code)
    doctors = Doctor.objects.filter(state=case.state).order_by("next_available")[:6]
    appointment = Appointment.objects.filter(case=case).select_related("doctor").first()
    return render(request, "triage/result.html", {"case": case, "doctors": doctors, "appointment": appointment})

def schedule(request, code, doctor_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    case = get_object_or_404(Case, code=code)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    Appointment.objects.update_or_create(case=case, defaults={"doctor": doctor, "scheduled_for": doctor.next_available})
    case.status = "scheduled"
    case.save(update_fields=["status"])
    messages.success(request, f"Consulta agendada com {doctor.name}.")
    return redirect("case_result", code=code)

def cancel_appointment(request, code):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    case = get_object_or_404(Case, code=code)
    Appointment.objects.filter(case=case).delete()
    case.status = "waiting"
    case.save(update_fields=["status"])
    messages.info(request, "O agendamento foi cancelado. Seu caso continua na fila de revisão.")
    return redirect("case_result", code=code)

def clinical_queue(request):
    order = {"urgent": 0, "soon": 1, "routine": 2}
    cases = sorted(Case.objects.all(), key=lambda c: (order[c.priority], c.created_at))
    return render(request, "triage/queue.html", {"cases": cases, "now": timezone.now()})
