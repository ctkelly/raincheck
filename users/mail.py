from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string


def wrapper_send_one_invitation_update_mail(subject_template, msg_template, recipient_list, ctx):

    subject = render_to_string(template_name=subject_template).strip()
    message = render_to_string(template_name=msg_template, context=ctx,)
    from_email = settings.EMAIL_HOST_USER
    return send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def wrapper_send_mass_mail(subject_template, msg_template, context1, context2, friend1, friend2):

    subject = render_to_string(template_name=subject_template).strip()
    owner_message = render_to_string(template_name=msg_template, context=context1,)
    invitee_message = render_to_string(template_name=msg_template, context=context2,)
    from_email = settings.EMAIL_HOST_USER
    friend1_message = (subject, owner_message, from_email, [friend1.email])
    friend2_message = (subject, invitee_message, from_email, [friend2.email])
    return send_mass_mail((friend1_message, friend2_message), fail_silently=False)
