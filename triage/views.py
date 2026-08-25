from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CaseForm, ClinicalReviewForm, RegistrationForm
from .models import Appointment, AuditEvent, Case, ClinicalReview, Doctor
from .services import calculate_priority

def home(request):
    return render(request, "triage/home.html", {"cases_count": Case.objects.count(), "doctors_count": Doctor.objects.count()})

def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Conta criada. Você já pode iniciar sua triagem.")
        return redirect("patient_dashboard")
    return render(request, "registration/register.html", {"form": form})

def is_doctor(user):
    return user.is_authenticated and (user.is_staff or getattr(getattr(user, "profile", None), "role", None) == "doctor")

@login_required
def dashboard(request):
    return redirect("clinical_queue" if is_doctor(request.user) else "patient_dashboard")

@login_required
def patient_dashboard(request):
    cases = request.user.cases.select_related().order_by("-created_at")
    return render(request, "triage/patient_dashboard.html", {"cases": cases})

@login_required
def submit_case(request):
    profile = getattr(request.user, "profile", None)
    initial = {"patient_name": request.user.get_full_name(), "email": request.user.email,
               "city": getattr(profile, "city", ""), "state": getattr(profile, "state", "SP")}
    form = CaseForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        case = form.save(commit=False)
        case.patient = request.user
        case.priority, case.score, case.reasons = calculate_priority(form.cleaned_data)
        case.save()
        AuditEvent.objects.create(case=case, actor=request.user, action="case_created", details={"priority": case.priority, "score": case.score})
        return redirect("case_result", code=case.code)
    return render(request, "triage/submit.html", {"form": form})

@login_required
def case_result(request, code):
    case = get_object_or_404(Case, code=code)
    if not is_doctor(request.user) and case.patient_id != request.user.id:
        messages.error(request, "Você não tem acesso a este caso.")
        return redirect("patient_dashboard")
    doctors = Doctor.objects.filter(state=case.state).order_by("next_available")[:6]
    appointment = Appointment.objects.filter(case=case).select_related("doctor").first()
    return render(request, "triage/result.html", {"case": case, "doctors": doctors, "appointment": appointment})

@login_required
def schedule(request, code, doctor_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    case = get_object_or_404(Case, code=code)
    if case.patient_id != request.user.id:
        return redirect("dashboard")
    doctor = get_object_or_404(Doctor, id=doctor_id)
    Appointment.objects.update_or_create(case=case, defaults={"doctor": doctor, "scheduled_for": doctor.next_available})
    case.status = "scheduled"
    case.save(update_fields=["status"])
    AuditEvent.objects.create(case=case, actor=request.user, action="appointment_scheduled", details={"doctor": doctor.name, "scheduled_for": doctor.next_available.isoformat()})
    messages.success(request, f"Consulta agendada com {doctor.name}.")
    return redirect("case_result", code=code)

@login_required
def cancel_appointment(request, code):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    case = get_object_or_404(Case, code=code)
    if case.patient_id != request.user.id:
        return redirect("dashboard")
    Appointment.objects.filter(case=case).delete()
    case.status = "waiting"
    case.save(update_fields=["status"])
    AuditEvent.objects.create(case=case, actor=request.user, action="appointment_cancelled")
    messages.info(request, "O agendamento foi cancelado. Seu caso continua na fila de revisão.")
    return redirect("case_result", code=code)

@user_passes_test(is_doctor)
def clinical_queue(request):
    order = {"urgent": 0, "soon": 1, "routine": 2}
    cases = sorted(Case.objects.all(), key=lambda c: (order[c.priority], c.created_at))
    return render(request, "triage/queue.html", {"cases": cases, "now": timezone.now()})

@user_passes_test(is_doctor)
def review_case(request, code):
    case = get_object_or_404(Case, code=code)
    form = ClinicalReviewForm(request.POST or None, initial={"final_priority": case.priority})
    if request.method == "POST" and form.is_valid():
        previous = case.priority
        review = form.save(commit=False)
        review.case = case
        review.reviewer = request.user
        review.automated_priority = previous
        review.save()
        case.priority = review.final_priority
        case.status = "reviewed"
        case.save(update_fields=["priority", "status"])
        AuditEvent.objects.create(case=case, actor=request.user, action="clinical_review",
                                  details={"previous_priority": previous, "final_priority": review.final_priority, "review_id": review.id})
        messages.success(request, "Revisão clínica registrada com rastreabilidade.")
        return redirect("review_case", code=code)
    reviews = case.reviews.select_related("reviewer").order_by("-created_at")
    return render(request, "triage/review.html", {"case": case, "form": form, "reviews": reviews, "events": case.audit_events.all()[:10]})
