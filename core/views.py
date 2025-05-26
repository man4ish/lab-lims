from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .models import Sample
from .forms import SampleForm


def logout_confirm(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')  # Redirect after logout

    return render(request, 'core/logout_confirm.html')


def home_view(request):
    return render(request, 'core/home.html')


class SampleListView(ListView):
    model = Sample
    template_name = 'core/sample_list.html'


class SampleDetailView(DetailView):
    model = Sample
    template_name = 'core/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You can add extra context data here if needed later
        return context


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
                recipient_list=['mandecent.gupta@gmail.com'],  # Replace with dynamic email if needed
                fail_silently=False,
            )
            return redirect(reverse('core:sample_success'))
        else:
            # form with errors will be rendered below
            pass
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
