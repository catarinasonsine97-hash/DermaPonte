from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Case, ClinicalReview, UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)
    first_name = forms.CharField(label="Nome", max_length=80)
    last_name = forms.CharField(label="Sobrenome", max_length=80)
    city = forms.CharField(label="Cidade", max_length=80)
    state = forms.CharField(label="UF", max_length=2, initial="SP")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "city", "state", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role="patient", city=self.cleaned_data["city"], state=self.cleaned_data["state"].upper())
        return user

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["patient_name", "email", "city", "state", "lesion_location", "noticed_when",
                  "changed", "bleeding", "itching_or_pain", "not_healing", "personal_history",
                  "family_history", "notes", "image", "consent"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3}), "state": forms.TextInput(attrs={"maxlength": 2})}

    def clean_consent(self):
        if not self.cleaned_data.get("consent"):
            raise forms.ValidationError("O consentimento é necessário para enviar o caso.")
        return True

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 8 * 1024 * 1024:
            raise forms.ValidationError("A imagem deve ter no máximo 8 MB.")
        return image

class ClinicalReviewForm(forms.ModelForm):
    class Meta:
        model = ClinicalReview
        fields = ["final_priority", "notes"]
        labels = {"final_priority": "Prioridade final", "notes": "Justificativa profissional"}
        widgets = {"notes": forms.Textarea(attrs={"rows": 5, "placeholder": "Registre os sinais observados e a justificativa da decisão."})}

    def clean_notes(self):
        notes = self.cleaned_data["notes"].strip()
        if len(notes) < 15:
            raise forms.ValidationError("A justificativa deve ter pelo menos 15 caracteres.")
        return notes
