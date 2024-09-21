from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import VoiceMaintainer


__all__ = (
    'VoiceMaintainerForm',
)


class VoiceMaintainerForm(forms.ModelForm):
    name = forms.CharField(label=_('Maintainer'))

    class Meta:
        model = VoiceMaintainer
        fields = ('name', )
