from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import *


__all__ = (
    'VoiceSdaForm',
    'VoiceSdaImportForm',
)


class VoiceSdaForm(forms.ModelForm):
    ''''
    creates a form for a SDA List instance
    '''
    start = forms.CharField(
        label=_('Start'),
        required=True,
        help_text=_('Start number of the range.'),
    )
    end = forms.CharField(
        label=_('End'),
        required=False,
        help_text=_('End number of the range. Can be left blank if the range is only one number.'),
    )
    delivery = forms.ModelChoiceField(
        label=_('Delivery'),
        queryset=VoiceDelivery.objects.all(),
        required=True,
        help_text=_('Choose how this range is delivered.'),
    )

    class Meta:
        model = VoiceSda
        fields = ('start', 'end', 'delivery', )


class VoiceSdaImportForm(forms.ModelForm):
    '''
    creates a form for importing a list of SDA List objects
    '''
    json_import = forms.JSONField(
        label=_('JSON'),
        help_text=('\
Enter the SDA List range number in a JSON format.\
[\
    "start >> end",\
    "start >> end",\
]'),
        required=True,
    )
    delivery = forms.ModelChoiceField(
        label=_('Delivery'),
        queryset=VoiceDelivery.objects.all(),
        required=True,
        help_text=_('The voice delivery the voice number range is assigned to.'),
    )

    class Meta:
        model = VoiceSda
        fields = ('json_import', 'delivery', )

    
