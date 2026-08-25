from datetime import timedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from triage.models import Case, Doctor, UserProfile

class Command(BaseCommand):
    help = "Cria profissionais fictícios para demonstração"
    def handle(self, *args, **options):
        patient, _ = User.objects.get_or_create(username="demo-paciente", defaults={"first_name": "Paciente", "last_name": "Demonstração", "email": "paciente@demo.local"})
        patient.set_password("DermaPonte123!")
        patient.save()
        UserProfile.objects.update_or_create(user=patient, defaults={"role": "patient", "city": "São Paulo", "state": "SP"})
        professional, _ = User.objects.get_or_create(username="demo-medico", defaults={"first_name": "Marina", "last_name": "Alves", "email": "medico@demo.local"})
        professional.set_password("DermaPonte123!")
        professional.save()
        UserProfile.objects.update_or_create(user=professional, defaults={"role": "doctor", "city": "São Paulo", "state": "SP"})
        doctors = [
            ("Dra. Marina Alves", "CRM-SP 000001", "São Paulo", "Av. Paulista, 900", 1, True),
            ("Dr. Lucas Ferreira", "CRM-SP 000002", "Campinas", "Rua das Acácias, 120", 2, True),
            ("Dra. Helena Nogueira", "CRM-SP 000003", "São Paulo", "Rua Vergueiro, 450", 4, False),
        ]
        for name, crm, city, address, days, tele in doctors:
            defaults={"name": name, "city": city, "state": "SP", "address": address, "next_available": timezone.now()+timedelta(days=days), "telemedicine": tele}
            if crm == "CRM-SP 000001": defaults["user"] = professional
            Doctor.objects.update_or_create(crm=crm, defaults=defaults)
        Case.objects.filter(patient__isnull=True).update(patient=patient)
        self.stdout.write(self.style.SUCCESS("Dados de demonstração criados."))
