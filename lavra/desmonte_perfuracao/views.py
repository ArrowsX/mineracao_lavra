from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import InputForm

from .helpers import Bancada


def home(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            coords = Bancada(data)
            coords.draw()
            return HttpResponseRedirect('/')
    else:
        form = InputForm()

    return render(request,
                  'desmonte_perfuracao/home.html',
                  {'form': form})
