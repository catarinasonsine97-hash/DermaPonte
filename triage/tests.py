from datetime import timedelta
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Appointment, Case, Doctor
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
