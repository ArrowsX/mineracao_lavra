from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

from .forms import InputForm

from .helpers import process


def home(request):
    if request.method == 'POST':
        if 'pdf' in request.POST:
            form = InputForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                pdf = process(data)
                return pdf
        else:
            form = InputForm()
    else:
        form = InputForm()

    return render(request, 'home.html', {'form': form})
