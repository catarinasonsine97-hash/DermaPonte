from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from triage.models import Doctor

class Command(BaseCommand):
    help = "Cria profissionais fictícios para demonstração"
    def handle(self, *args, **options):
        doctors = [
            ("Dra. Marina Alves", "CRM-SP 000001", "São Paulo", "Av. Paulista, 900", 1, True),
            ("Dr. Lucas Ferreira", "CRM-SP 000002", "Campinas", "Rua das Acácias, 120", 2, True),
            ("Dra. Helena Nogueira", "CRM-SP 000003", "São Paulo", "Rua Vergueiro, 450", 4, False),
        ]
        for name, crm, city, address, days, tele in doctors:
            Doctor.objects.update_or_create(crm=crm, defaults={"name": name, "city": city, "state": "SP", "address": address, "next_available": timezone.now()+timedelta(days=days), "telemedicine": tele})
        self.stdout.write(self.style.SUCCESS("Dados de demonstração criados."))
