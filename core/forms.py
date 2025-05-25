# core/forms.py
from django import forms
from core.models import Sample, SampleType, SpecimenSource, Organism, Project

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
