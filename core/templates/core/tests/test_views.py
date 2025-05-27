from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from unittest.mock import patch
from core.models import Sample, Project, Organism, Instrument, Run, SequenceType, DownstreamAnalysis, Flowcell, Library, LibraryLane, Lane
from core.forms import SampleForm, LibraryForm
import io

class ViewsTest(TestCase):

    def setUp(self):
        # Create test user and groups
        self.admin_group = Group.objects.create(name='admin')
        self.user_group = Group.objects.create(name='user')

        self.admin_user = User.objects.create_user(username='admin', password='adminpass')
        self.admin_user.groups.add(self.admin_group)

        self.regular_user = User.objects.create_user(username='user', password='userpass')
        self.regular_user.groups.add(self.user_group)

        # Create test objects for related models
        self.project = Project.objects.create(label='Project1')
        self.organism = Organism.objects.create(label='Organism1')

        self.sample = Sample.objects.create(label='Sample1', project=self.project, organism=self.organism)
        self.instrument = Instrument.objects.create(name='Instrument1')
        self.run = Run.objects.create(name='Run1', flowcell_id=1)  # add flowcell later if needed
        self.sequence_type = SequenceType.objects.create(name='SeqType1')
        self.flowcell = Flowcell.objects.create(name='Flowcell1')
        self.downstream_analysis = DownstreamAnalysis.objects.create(sequence_type=self.sequence_type, name='Downstream1')

        self.library = Library.objects.create(sample=self.sample, label='Library1')
        self.lane = Lane.objects.create(name='Lane1')
        self.library_lane = LibraryLane.objects.create(library=self.library, lane=self.lane)

        self.client = Client()

    def test_sample_list_view(self):
        url = reverse('core:sample_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('object_list', response.context)
        self.assertContains(response, self.sample.label)

    def test_sample_list_view_search(self):
        url = reverse('core:sample_list') + '?q=Sample1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(self.sample.label in s.label for s in response.context['object_list']))

    def test_sample_export_csv(self):
        url = reverse('core:sample_export') + '?format=csv'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="samples.csv"', response['Content-Disposition'])
        content = response.content.decode()
        self.assertIn('Label,Project,Organism', content)

    def test_sample_export_excel(self):
        url = reverse('core:sample_export') + '?format=excel'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', response['Content-Type'])
        self.assertIn('attachment; filename="samples.xlsx"', response['Content-Disposition'])

    def test_instrument_detail_view(self):
        url = reverse('core:instrument_detail', args=[self.instrument.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['instrument'], self.instrument)

    def test_run_detail_view(self):
        url = reverse('core:run_detail', args=[self.run.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.run)

    def test_instrument_detail_modal(self):
        url = reverse('core:instrument_detail_modal', args=[self.instrument.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['instrument'], self.instrument)

    def test_downstream_analyses_by_sequence_type(self):
        url = reverse('core:downstream_analyses_by_sequence_type', args=[self.sequence_type.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sequence_type'], self.sequence_type)
        self.assertIn(self.downstream_analysis, response.context['downstream_analyses'])

    def test_analyses_by_flowcell(self):
        url = reverse('core:analyses_by_flowcell', args=[self.flowcell.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flowcell'], self.flowcell)

    def test_analyses_and_runs_by_flowcell(self):
        url = reverse('core:analyses_and_runs_by_flowcell', args=[self.flowcell.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['flowcell'], self.flowcell)

    def test_logout_confirm_get(self):
        url = reverse('core:logout_confirm')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_confirm_post(self):
        self.client.login(username='user', password='userpass')
        url = reverse('core:logout_confirm')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('login'))

    def test_home_view(self):
        url = reverse('core:home_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sample_detail_get(self):
        url = reverse('core:sample_detail', args=[self.sample.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('libraries', response.context)
        self.assertIsInstance(response.context['library_form'], LibraryForm)

    def test_sample_detail_post_valid_form(self):
        self.client.login(username='user', password='userpass')
        url = reverse('core:sample_detail', args=[self.sample.pk])
        data = {'label': 'New Library Label'}
        response = self.client.post(url, data)
        # It should redirect on success
        self.assertEqual(response.status_code, 302)

    def test_sample_detail_post_invalid_form(self):
        self.client.login(username='user', password='userpass')
        url = reverse('core:sample_detail', args=[self.sample.pk])
        data = {}  # missing required fields for LibraryForm
        response = self.client.post(url, data)
        # Should return the form with errors (status 200)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['library_form'], LibraryForm)
        self.assertTrue(response.context['library_form'].errors)

    def test_library_detail_view(self):
        url = reverse('core:library_detail', args=[self.library.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('library_lanes', response.context)

    def test_sample_create_view_get(self):
        self.client.login(username='user', password='userpass')
        url = reverse('core:sample_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SampleForm)

    @patch('core.views.send_mail')
    def test_sample_create_view_post_valid(self, mock_send_mail):
        self.client.login(username='user', password='userpass')
        url = reverse('core:sample_create')
        data = {
            'label': 'Sample2',
            'project': self.project.pk,
            'organism': self.organism.pk,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('core:sample_success'))
        self.assertTrue(mock_send_mail.called)

    def test_sample_success_view(self):
        url = reverse('core:sample_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_view_get(self):
        url = reverse('core:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_signup_view_post_valid(self):
        url = reverse('core:signup')
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('core:sample_create'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
