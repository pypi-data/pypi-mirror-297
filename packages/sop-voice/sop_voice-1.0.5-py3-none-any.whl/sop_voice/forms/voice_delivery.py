from django import forms
from django.utils.translation import gettext_lazy as _

from circuits.models import Provider

from sop_utils.models import VoiceDeliveryStatusChoices

from ..models import *


__all__ = (
    'VoiceDeliveryForm',
)


class VoiceDeliveryForm(forms.ModelForm):
    '''
    creates a form for a Voice Delivery object
    '''
    delivery = forms.CharField(
        label=_('Delivery Method'),
    )
    provider = forms.ModelChoiceField(
        required=True,
        queryset=Provider.objects.all(),
        label=_('Provider')
    )
    channel_count = forms.CharField(
        required=False,
        label=_('Channel Count'),
    )
    status = forms.ChoiceField(
        choices=VoiceDeliveryStatusChoices,
        required=True,
        label=_('Status'),
    )
    ndi = forms.CharField(
        required=False,
        max_length=100,
        label=_('NDI'),
    )
    dto = forms.CharField(
        required=False,
        max_length=100,
        label=_('DTO'),
    )

    class Meta:
        model = VoiceDelivery
        fields = ('delivery', 'provider', 'channel_count', 'status', 'ndi', 'dto')
