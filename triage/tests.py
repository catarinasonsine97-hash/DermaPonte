from datetime import timedelta
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Appointment, AuditEvent, Case, ClinicalReview, Doctor, UserProfile
from .services import calculate_priority

class PriorityRulesTests(TestCase):
    def test_routine_without_warning_signs(self):
        priority, score, reasons = calculate_priority({})
        self.assertEqual((priority, score), ("routine", 0))
        self.assertTrue(reasons)

    def test_soon_when_lesion_changed(self):
        self.assertEqual(calculate_priority({"changed": True})[0], "soon")

    def test_urgent_for_combined_warning_signs(self):
        self.assertEqual(calculate_priority({"bleeding": True, "not_healing": True})[0], "urgent")

class PatientFlowTests(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user("patient", password="StrongPass123!", first_name="Paciente")
        UserProfile.objects.create(user=self.patient, role="patient", city="São Paulo", state="SP")
        self.client.login(username="patient", password="StrongPass123!")

    def image(self):
        stream = BytesIO()
        Image.new("RGB", (400, 300), "#b9826b").save(stream, "JPEG")
        return SimpleUploadedFile("lesao.jpg", stream.getvalue(), content_type="image/jpeg")

    def test_submit_and_schedule_case(self):
        response = self.client.post(reverse("submit_case"), {
            "patient_name": "Paciente Teste", "email": "teste@example.com", "city": "São Paulo",
            "state": "SP", "lesion_location": "Braço", "noticed_when": "Há dois meses",
            "changed": "on", "bleeding": "on", "notes": "Caso automatizado", "consent": "on",
            "image": self.image(),
        })
        case = Case.objects.get()
        self.assertRedirects(response, reverse("case_result", args=[case.code]))
        self.assertEqual(case.priority, "urgent")
        self.assertEqual(case.patient, self.patient)
        doctor = Doctor.objects.create(name="Dra. Teste", crm="CRM-SP 1", city="São Paulo", state="SP",
                                       address="Rua Teste", next_available=timezone.now()+timedelta(days=1))
        response = self.client.post(reverse("schedule", args=[case.code, doctor.id]))
        self.assertRedirects(response, reverse("case_result", args=[case.code]))
        self.assertTrue(Appointment.objects.filter(case=case, doctor=doctor).exists())
        response = self.client.get(reverse("case_result", args=[case.code]))
        self.assertContains(response, "Agendamento confirmado")
        self.assertContains(response, "Dra. Teste")
        response = self.client.post(reverse("cancel_appointment", args=[case.code]))
        self.assertRedirects(response, reverse("case_result", args=[case.code]))
        self.assertFalse(Appointment.objects.filter(case=case).exists())

    def test_patient_cannot_access_another_case(self):
        other = User.objects.create_user("other", password="StrongPass123!")
        case = Case.objects.create(patient=other, patient_name="Outra pessoa", email="other@example.com",
                                   city="São Paulo", state="SP", lesion_location="Braço", noticed_when="Ontem",
                                   image=self.image(), consent=True)
        response = self.client.get(reverse("case_result", args=[case.code]))
        self.assertRedirects(response, reverse("patient_dashboard"))

class ClinicalReviewTests(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user("doctor", password="StrongPass123!", first_name="Dra.", last_name="Teste")
        UserProfile.objects.create(user=self.doctor, role="doctor")
        self.patient = User.objects.create_user("patient2", password="StrongPass123!")
        UserProfile.objects.create(user=self.patient, role="patient")
        image = BytesIO()
        Image.new("RGB", (100, 100), "#a87865").save(image, "JPEG")
        self.case = Case.objects.create(patient=self.patient, patient_name="Paciente", email="p@example.com",
                                        city="São Paulo", state="SP", lesion_location="Perna", noticed_when="Um mês",
                                        image=SimpleUploadedFile("case.jpg", image.getvalue(), content_type="image/jpeg"),
                                        priority="soon", consent=True)

    def test_patient_cannot_open_clinical_queue(self):
        self.client.login(username="patient2", password="StrongPass123!")
        response = self.client.get(reverse("clinical_queue"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('clinical_queue')}")

    def test_doctor_review_creates_audit_trail(self):
        self.client.login(username="doctor", password="StrongPass123!")
        response = self.client.post(reverse("review_case", args=[self.case.code]), {
            "final_priority": "urgent", "notes": "Lesão deve receber avaliação presencial prioritária.",
        })
        self.assertRedirects(response, reverse("review_case", args=[self.case.code]))
        self.case.refresh_from_db()
        self.assertEqual(self.case.priority, "urgent")
        self.assertEqual(self.case.status, "reviewed")
        self.assertTrue(ClinicalReview.objects.filter(case=self.case, reviewer=self.doctor).exists())
        self.assertTrue(AuditEvent.objects.filter(case=self.case, action="clinical_review").exists())
