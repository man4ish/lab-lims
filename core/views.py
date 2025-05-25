from .forms import SampleForm
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import render, redirect

def sample_create_view(request):
    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample = form.save()
            send_mail(
                subject='Sample Submission Confirmation',
                message=f'Thank you! Your sample "{sample.label}" has been submitted successfully.',
                from_email='no-reply@example.com',
                recipient_list=['mandecent.gupta@gmail.com'],  # <-- Update this for dynamic emails if needed
                fail_silently=False,
            )
            return redirect(reverse('core:sample_success'))  # <-- note the 'core:' prefix
    else:
        form = SampleForm()
    return render(request, 'core/sample_form.html', {'form': form})

def sample_success_view(request):
    return render(request, 'core/sample_success.html')
