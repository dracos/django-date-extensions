from django.shortcuts import render_to_response

from examples.django.form_fields.forms import DatesForm


def view(request):
    dates_form = DatesForm(request.GET or None)
    return render_to_response("form.html", {"form": dates_form})
