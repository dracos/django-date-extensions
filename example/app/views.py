from django.shortcuts import render_to_response
from .forms import DatesForm

def view(request):
    dates_form = DatesForm(request.GET or None)       
    valid = dates_form.is_valid()
    return render_to_response('form.html', { 'form': dates_form })

