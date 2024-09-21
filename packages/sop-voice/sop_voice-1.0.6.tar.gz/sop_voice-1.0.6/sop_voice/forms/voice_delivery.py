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
        label=_('Provider'),
        help_text=_('SIP TRUNK, T0, T2, ...')
    )
    channel_count = forms.CharField(
        required=False,
        label=_('Channel Count'),
        help_text=_('G.711 cidec - 96kbps reserved bandwidth per channel')
    )
    status = forms.ChoiceField(
        choices=VoiceDeliveryStatusChoices,
        required=True,
        label=_('Status'),
    )
    ndi = forms.CharField(
        required=False,
        max_length=100,
        label=_('MBN / NDI'),
        help_text=_("Main Billing Number / Numéro de Désignation d'Installation - E164 format")
    )
    dto = forms.CharField(
        required=False,
        max_length=100,
        label=_('DTO'),
        help_text=_('E164 format')
    )

    class Meta:
        model = VoiceDelivery
        fields = ('delivery', 'provider', 'channel_count', 'status', 'ndi', 'dto')
