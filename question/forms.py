import django.forms as forms


class LocationForm(forms.Form):
	location = forms.CharField(max_length=100)