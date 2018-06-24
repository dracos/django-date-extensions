from django.shortcuts import render
from .forms import DatesForm

def view(request):
    dates_form = DatesForm(request.GET or None)
    dates_form.is_valid()
    return render(request, 'form.html', {'form': dates_form})

