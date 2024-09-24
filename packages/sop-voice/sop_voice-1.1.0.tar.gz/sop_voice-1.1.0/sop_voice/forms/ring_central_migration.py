from django import forms
from django.utils.translation import gettext_lazy as _

from sop_utils.models import SopBoolChoices

from ..models import RingCentralMigration


__all__ = (
    'RingCentralMigrationForm',
)


class RingCentralMigrationForm(forms.ModelForm):
    '''
    creates a form for a Ring Central Migration object
    choices are from the SopBoolChoices model
    '''

    hardware = forms.ChoiceField(
        choices = SopBoolChoices,
        label=_('No hardware visible ?'),
        help_text=_('Set to True if you can positively confirm that no phone related hardware is visible on the site.'),
    )
    vlan = forms.ChoiceField(
        choices = SopBoolChoices,
        label=_('No VLAN visible ?'),
        help_text=_('Set to True if you can positively confirm that there is no old/historical voice VLAN configured on the site.'),
    )
    client = forms.ChoiceField(
        choices = SopBoolChoices,
        label=_('No client visible ?'),
        help_text=_('Set to True if you can positively confirm that there is no voice client visible in the Meraki dashboard.'),
    )
    migration = forms.ChoiceField(
        choices = SopBoolChoices,
        label=_('RC Migration done ?'),
        help_text=_('Set to True if you can positively confirm that the Ring Central Migration is done on this site.'),
    )

    class Meta:
        model = RingCentralMigration
        fields = ('hardware', 'vlan', 'client', 'migration', )
