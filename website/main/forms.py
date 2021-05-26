from django import forms

class tikerForm(forms.Form):
    ticker = forms.CharField(label='stock ticker', max_length=5)
