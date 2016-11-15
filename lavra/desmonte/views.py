from django.shortcuts import render

from .forms import InputForm

from .helpers import processed, export


def home(request):
    if request.method == 'POST':
        if 'pdf' in request.POST:  # Need attribute 'name' in <input>
            form = InputForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                return export(processed(data))
        else:
            form = InputForm()
    else:
        form = InputForm()

    return render(request, 'desmonte/home.html', {'form': form})
