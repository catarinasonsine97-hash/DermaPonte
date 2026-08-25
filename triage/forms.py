from django import forms
from .models import Case

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
