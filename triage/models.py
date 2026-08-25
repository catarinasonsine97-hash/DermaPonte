import uuid
from django.db import models

class Case(models.Model):
    PRIORITIES = [("urgent", "Revisão prioritária"), ("soon", "Revisão breve"), ("routine", "Revisão de rotina")]
    STATUS = [("waiting", "Aguardando revisão"), ("reviewed", "Revisado"), ("scheduled", "Consulta agendada")]
    code = models.CharField(max_length=10, unique=True, editable=False)
    patient_name = models.CharField("Nome", max_length=120)
    email = models.EmailField("E-mail")
    city = models.CharField("Cidade", max_length=80)
    state = models.CharField("UF", max_length=2, default="SP")
    lesion_location = models.CharField("Local da lesão", max_length=120)
    noticed_when = models.CharField("Quando percebeu a lesão?", max_length=120)
    changed = models.BooleanField("Mudou de tamanho, formato ou cor?", default=False)
    bleeding = models.BooleanField("Sangra?", default=False)
    itching_or_pain = models.BooleanField("Coça ou dói?", default=False)
    not_healing = models.BooleanField("Não cicatriza há quatro semanas?", default=False)
    personal_history = models.BooleanField("Histórico pessoal de câncer de pele?", default=False)
    family_history = models.BooleanField("Histórico familiar de câncer de pele?", default=False)
    notes = models.TextField("Observações", blank=True)
    image = models.ImageField("Foto da lesão", upload_to="cases/")
    consent = models.BooleanField("Consentimento", default=False)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default="routine")
    score = models.PositiveSmallIntegerField(default=0)
    reasons = models.JSONField(default=list)
    status = models.CharField(max_length=12, choices=STATUS, default="waiting")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

class Doctor(models.Model):
    name = models.CharField(max_length=120)
    crm = models.CharField(max_length=30)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=2, default="SP")
    address = models.CharField(max_length=180)
    next_available = models.DateTimeField()
    telemedicine = models.BooleanField(default=True)

class Appointment(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    scheduled_for = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
