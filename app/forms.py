from django import forms
from .models import Volunteer


class VolunteerForm(forms.ModelForm):
	class Meta:
		model = Volunteer
		fields = ['name', 'contact', 'address', 'picture', 'area']
