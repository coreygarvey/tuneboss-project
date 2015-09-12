from django import forms

CHOICES=[('Spotify','Spotify')]


class ClientUsernameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, initial=123770737)
    client = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), initial='Spotify')