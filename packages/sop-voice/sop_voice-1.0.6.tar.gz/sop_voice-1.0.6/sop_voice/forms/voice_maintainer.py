from django import forms
from django.utils.translation import gettext_lazy as _

from utilities.forms import CSVModelForm

from ..models import VoiceMaintainer


__all__ = (
    'VoiceMaintainerForm',
    'VoiceMaintainerImportForm',
)


class VoiceMaintainerForm(forms.ModelForm):
    name = forms.CharField(label=_('Maintainer'))

    class Meta:
        model = VoiceMaintainer
        fields = ('name', )


class VoiceMaintainerImportForm(forms.ModelForm):
    json_import = forms.JSONField(
        label=_('JSON'),
        help_text=('\
Enter the Maintainer in a JSON format.\
["Quonex", "Alcatel"]'),
        required=True,
    )

    class Meta:
        model = VoiceMaintainer
        fields = ('json_import', )
