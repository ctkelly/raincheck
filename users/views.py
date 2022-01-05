from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # If I assign user_registration = form.save(), can I assign name = user_registration.username? YES IT WORKS
            # Was previously just form.save()
            user_registration = form.save()
            name = user_registration.username
            # name = request.POST['username'] # Don't need this if form.save() assigned to variable
            ctx = {'name': name}
            subject = render_to_string(
                template_name='users/register_success_email_subject.txt'
            ).strip()
            message = render_to_string(
                template_name='users/register_success_email_message.txt',
                context=ctx,
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.RECIPIENT_ADDRESS]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('events:all')

    else:  # If the request is GET instead of POST
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


