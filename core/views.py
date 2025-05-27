from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .models import Sample
from .forms import SampleForm
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from core.forms import LibraryForm
from core.models import Sample, Library
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Library
from django.views.generic import DetailView
from .models import LibraryLane

from django.views.generic import DetailView
from .models import Lane
from django.shortcuts import render, get_object_or_404
from .models import Analyses, Flowcell

from .models import Flowcell, Analyses, Run, SequenceType, DownstreamAnalysis # Make sure to import all necessary models
from django.views.generic import DetailView # For class-based detail view
from .models import Project
from .models import Instrument, InstrumentType

from .models import Instrument # Make sure Instrument model is imported

from .models import Run # Make sure Run model is imported

from django.views.generic import ListView
from django.db.models import Q
from .models import Sample

from django.http import HttpResponse
import csv
import pandas as pd

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

# Helper functions to check group membership
def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='admin').exists()

def is_user(user):
    return user.is_authenticated and user.groups.filter(name='user').exists()

# Decorator versions for function views
admin_required = user_passes_test(is_admin)
user_or_admin_required = user_passes_test(lambda u: is_admin(u) or is_user(u))

class SampleListView(ListView):
    model = Sample
    template_name = 'core/sample_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(label__icontains=query) |
                Q(description__icontains=query) |
                Q(project__label__icontains=query) |
                Q(organism__label__icontains=query)
            )
        return queryset
    
def sample_export(request):
    query = request.GET.get('q')
    format_ = request.GET.get('format', 'csv').lower()

    queryset = Sample.objects.all()
    if query:
        queryset = queryset.filter(
            Q(label__icontains=query) |
            Q(description__icontains=query) |
            Q(project__label__icontains=query) |
            Q(organism__label__icontains=query)
        )

    data = queryset.values('label', 'project__label', 'organism__label')

    if format_ == 'excel':
        import pandas as pd

        df = pd.DataFrame(list(data))
        df.rename(columns={
            'label': 'Label',
            'project__label': 'Project',
            'organism__label': 'Organism'
        }, inplace=True)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="samples.xlsx"'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Samples')

        return response

    else:  # CSV
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="samples.csv"'

        writer = csv.writer(response)
        writer.writerow(['Label', 'Project', 'Organism'])
        for sample in data:
            writer.writerow([
                sample['label'],
                sample['project__label'],
                sample['organism__label'],
            ])

        return response

class InstrumentDetailView(DetailView):
    model = Instrument
    template_name = 'core/instrument_detail.html' # This is the template it will use
    context_object_name = 'instrument' # This makes the Instrument object available as 'instrument' in the template

class RunDetailView(DetailView):
    model = Run
    template_name = 'core/run_detail.html' # You'll need to create this template
    context_object_name = 'object' # Or 'run' if you prefer that context name

def instrument_detail_modal(request, pk):
    instrument = Instrument.objects.get(pk=pk)
    return render(request, 'core/instrument_detail_modal.html', {'instrument': instrument})

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html' # Create this template file next!
    context_object_name = 'project' # Name of the object in the template context


def downstream_analyses_by_sequence_type(request, sequence_type_id):
    # Get the specific SequenceType object
    sequence_type = get_object_or_404(SequenceType, id=sequence_type_id)

    # Get all DownstreamAnalysis objects related to this SequenceType
    # We use the related_name='downstream_analyses' defined in the DownstreamAnalysis model
    downstream_analyses = sequence_type.downstream_analyses.all()

    return render(request, 'core/downstream_analyses_by_sequence_type.html', {
        'sequence_type': sequence_type,
        'downstream_analyses': downstream_analyses,
    })

def analyses_by_flowcell(request, flowcell_id):
    flowcell = get_object_or_404(Flowcell, id=flowcell_id)
    analyses = flowcell.analyses.all()  # using related_name
    return render(request, 'core/analyses_by_flowcell.html', {
        'flowcell': flowcell,
        'analyses': analyses
    })

def analyses_and_runs_by_flowcell(request, flowcell_id):
    flowcell = get_object_or_404(Flowcell, id=flowcell_id)

    # Get all analyses associated with this flowcell
    analyses = flowcell.analyses.all()  # Uses related_name='analyses' in Analyses model

    # Get all runs associated with this flowcell
    runs = flowcell.runs.all() # Uses related_name='runs' in Run model

    return render(request, 'core/analyses_and_runs_by_flowcell.html', {
        'flowcell': flowcell,
        'analyses': analyses,
        'runs': runs, # Pass the runs data to the template
    })


class LaneDetailView(DetailView):
    model = Lane
    template_name = 'core/lane_detail.html'  # You can change this path if you want


def logout_confirm(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')  # or wherever you want after logout

    return render(request, 'core/logout_confirm.html')

def home_view(request):
    return render(request, 'core/home.html')


class SampleDetailView(DetailView):
    model = Sample
    template_name = 'core/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sample = self.get_object()
        context['libraries'] = sample.libraries.all()  # Related libraries
        context['library_form'] = LibraryForm()
        return context

    def post(self, request, *args, **kwargs):
        # Handle library form submission on sample detail page
        self.object = self.get_object()
        form = LibraryForm(request.POST)
        if form.is_valid():
            library = form.save(commit=False)
            library.sample = self.object  # Link library to current sample
            library.save()
            return redirect('core:sample_detail', pk=self.object.pk)
        context = self.get_context_data()
        context['library_form'] = form  # return form with errors
        return self.render_to_response(context)
    
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'core/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['library_lanes'] = library.library_lanes.select_related('lane')
        return context    

class LibraryUpdateView(UpdateView):
    model = Library
    fields = '__all__'  # or use a specific form
    template_name = 'core/library_form.html'

    def get_success_url(self):
        return reverse_lazy('core:library_detail', kwargs={'pk': self.object.pk})

class LibraryDeleteView(DeleteView):
    model = Library
    template_name = 'core/library_confirm_delete.html'
    success_url = reverse_lazy('core:sample_list')



class LibraryLaneDetailView(DetailView):
    model = LibraryLane
    template_name = 'core/librarylane_detail.html'


class SampleUpdateView(UpdateView):
    model = Sample
    form_class = SampleForm
    template_name = 'core/sample_form.html'
    success_url = reverse_lazy('core:sample_list')

class SampleDeleteView(DeleteView):
    model = Sample
    template_name = 'core/sample_confirm_delete.html'
    success_url = reverse_lazy('core:sample_list')

@login_required
def sample_create_view(request):
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample = form.save()
            send_mail(
                subject='Sample Submission Confirmation',
                message=f'Thank you! Your sample "{sample.label}" has been submitted successfully.',
                from_email='no-reply@example.com',
                recipient_list=['mandecent.gupta@gmail.com'],  # Replace or make dynamic
                fail_silently=False,
            )
            return redirect(reverse('core:sample_success'))
    else:
        form = SampleForm()
    return render(request, 'core/sample_form.html', {'form': form})

def sample_success_view(request):
    return render(request, 'core/sample_success.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:sample_create')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
