# core/tests/test_forms.py
import pytest
from django.utils import timezone
from core.forms import SampleForm, LibraryForm
from core.models import SampleType, SpecimenSource, Organism, Project, LibraryType, Protocol, Bardex

@pytest.mark.django_db
class TestSampleForm:

    def test_sample_form_valid_data(self):
        # Setup required related objects
        sample_type = SampleType.objects.create(label="Type A")
        specimen_source = SpecimenSource.objects.create(label="Source A")
        organism = Organism.objects.create(label="Organism A")
        project = Project.objects.create(label="Project A")

        form_data = {
            'label': 'Sample 1',
            'organism': organism.id,
            'project': project.id,
            'description': 'This is a sample description.',
            'sample_type': sample_type.id,
            'specimen_source': specimen_source.id,
        }
        form = SampleForm(data=form_data)
        assert form.is_valid()

    def test_sample_form_missing_required_fields(self):
        form = SampleForm(data={})
        assert not form.is_valid()
        # 'label' is required
        assert 'label' in form.errors

    def test_sample_form_widgets(self):
        form = SampleForm()
        assert 'class' in form.fields['label'].widget.attrs
        assert form.fields['label'].widget.attrs['class'] == 'form-control'


@pytest.mark.django_db
class TestLibraryForm:

    def test_library_form_valid_data(self):
        # Setup required related objects
        library_type = LibraryType.objects.create(label="LibType A")
        protocol = Protocol.objects.create(label="Protocol A")
        bardex = Bardex.objects.create(label="Bardex A")
        second_bardex = Bardex.objects.create(label="Bardex B")

        form_data = {
            'label': 'Library 1',
            'library_type': library_type.id,
            'employee_id': 123,
            'protocol': protocol.id,
            'date_created': timezone.now().date(),
            'description': 'Library description',
            'insert_size': 300,
            'client_provided': True,
            'bardex': bardex.id,
            'second_bardex': second_bardex.id,
            'active': True,
        }
        form = LibraryForm(data=form_data)
        assert form.is_valid()

    def test_library_form_missing_required_fields(self):
        form = LibraryForm(data={})
        assert not form.is_valid()
        assert 'label' in form.errors

    def test_library_form_widgets(self):
        form = LibraryForm()
        assert 'class' in form.fields['label'].widget.attrs
        assert form.fields['label'].widget.attrs['class'] == 'form-control'
