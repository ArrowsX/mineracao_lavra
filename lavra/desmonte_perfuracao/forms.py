from django.forms import Form, IntegerField, FloatField, TextInput


class InputForm(Form):
    producao = IntegerField(
        label='Produção anual (t/ano)',
        initial=2000000,
        widget=TextInput)
    densidade = FloatField(
        label='Densidade da rocha (t/m³)',
        initial=2.6,
        widget=TextInput)
    frequencia = IntegerField(
        label='Frequência por semana',
        initial=1,
        widget=TextInput)
    turno = IntegerField(
        label='Turnos (horas)',
        initial=8,
        widget=TextInput)
    rcu = IntegerField(
        label='RCU (MPa)',
        initial=80,
        widget=TextInput)
    inclinacao = IntegerField(
        label='Inclinação (β)',
        initial=15,
        widget=TextInput)
    p1 = FloatField(
        label='Explosivo da coluna (g/cm³)',
        initial=0.8,
        widget=TextInput)
    p2 = FloatField(
        label='Explosivo da fundo (g/cm³)',
        initial=1.1,
        widget=TextInput)
