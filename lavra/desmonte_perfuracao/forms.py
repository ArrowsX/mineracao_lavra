from django import forms


class InputForm(forms.Form):
    producao = forms.IntegerField(label='Produção',
                                  widget=forms.TextInput)
    densidade = forms.IntegerField(label='Densidade da rocha',
                                   widget=forms.TextInput)
    frequencia = forms.IntegerField(label='Frequência por semana',
                                    widget=forms.TextInput)
    turno = forms.IntegerField(label='Turnos de hora',
                               widget=forms.TextInput)
    rcu = forms.IntegerField(label='RCU',
                             widget=forms.TextInput)
    inclinacao = forms.IntegerField(label='Inclinação (β)',
                                    widget=forms.TextInput)
