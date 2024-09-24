from django import forms
from django.utils.translation import gettext_lazy as _

from sop_utils.models import SopBoolChoices

from ..models import BTIPMigration


__all__ = (
    'BTIPMigrationForm',
)


class BTIPMigrationForm(forms.ModelForm):
    '''
    creates a form for a BTIP Migration object
    choices are from the SopBoolChoices model
    '''

    hardware = forms.ChoiceField(
        choices = SopBoolChoices,
        label=_('Hardware supported ?'),
    )
    migration = forms.ChoiceField(
        choices = SopBoolChoices,
        label=_('BTIP migration done ?'),
    )

    class Meta:
        model = BTIPMigration
        fields = ('hardware', 'migration', )
