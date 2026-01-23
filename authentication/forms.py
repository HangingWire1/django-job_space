from django import forms
from authentication.models import Location, State, Township


class RegistrationForm(forms.ModelForm):
    # Explicitly define the field here
    township = forms.ModelChoiceField(queryset=Township.objects.none())

    class Meta:
        model = Location
        fields = ['state', 'township', 'detail_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Now PyCharm knows 'township' has a queryset
        self.fields['township'].queryset = Township.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['township'].queryset = Township.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset