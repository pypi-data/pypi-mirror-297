import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable

from ..models import VoiceMaintainer


__all__ = (
    'VoiceMaintainerTable',
)

class VoiceMaintainerTable(NetBoxTable):
    '''
    table for all Voice Deliveries
    '''
    name = tables.Column(verbose_name=_('Name'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = VoiceMaintainer
        fields = ('pk', 'id', 'actions', 'name')
        default_columns = ('name',)
