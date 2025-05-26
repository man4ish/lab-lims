from django import forms
from core.models import Sample
from django.core.exceptions import ValidationError
import re

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = [
            'label',
            'organism',
            'project',
            'description',
            'sample_type',
            'specimen_source',
        ]
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'organism': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sample_type': forms.Select(attrs={'class': 'form-control'}),
            'specimen_source': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_label(self):
        label = self.cleaned_data.get('label')
        if not re.match(r'^[\w-]+$', label):
            raise ValidationError('Label can only contain letters, numbers, underscores, and hyphens.')

        # Exclude current instance from uniqueness check (for edits)
        qs = Sample.objects.filter(label=label)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Sample with this label already exists.')

        return label
    
    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        organism = cleaned_data.get('organism')

        # If you want to validate something like "organism must be compatible with project"
        # you need a way to check this, maybe via related models or business logic.

        # Since your Project doesn't have an organism field,
        # just ensure both are selected or validate your own business rules here.

        if not project:
            raise forms.ValidationError("Please select a project.")
        if not organism:
            raise forms.ValidationError("Please select an organism.")

        # Example: if you have a custom rule, check it here, e.g.
        # if organism not in allowed_organisms_for_project(project):
        #     raise forms.ValidationError("Organism not valid for this project.")

        return cleaned_data
