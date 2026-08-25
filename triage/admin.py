from django.contrib import admin
from .models import Appointment, AuditEvent, Case, ClinicalReview, Doctor, UserProfile

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("code", "patient_name", "priority", "status", "created_at")
    list_filter = ("priority", "status", "state")
    search_fields = ("code", "patient_name", "email")

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(UserProfile)
admin.site.register(ClinicalReview)
admin.site.register(AuditEvent)
