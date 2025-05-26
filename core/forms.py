# core/forms.py
from django import forms
from core.models import Sample, SampleType, SpecimenSource, Organism, Project
from django import forms
from core.models import Library

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

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = [
            'label',
            'library_type',
            'employee_id',
            'protocol',
            'date_created',
            'description',
            'insert_size',
            'client_provided',
            'bardex',
            'second_bardex',
            'active',
        ]
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'library_type': forms.Select(attrs={'class': 'form-control'}),
            'employee_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'protocol': forms.Select(attrs={'class': 'form-control'}),
            'date_created': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'insert_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'client_provided': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bardex': forms.Select(attrs={'class': 'form-control'}),
            'second_bardex': forms.Select(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

