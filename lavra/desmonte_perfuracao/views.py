from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import InputForm


def home(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            return HttpResponseRedirect('/')
    else:
        form = InputForm()

    return render(request, 'desmonte_perfuracao/home.html', {'form': form})
