import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from ..models import SDA_List


__all__ = (
    'SDA_ListTable',
)


class SDA_ListTable(NetBoxTable):
    '''
    table for all SDA List
    '''
    delivery = tables.Column(verbose_name=_('Delivery'), linkify=True)
    start = tables.Column(verbose_name=_('Start'), linkify=True)
    end = tables.Column(verbose_name=_('End'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = SDA_List
        fields = ('actions', 'pk', 'id', 'delivery', 'start', 'end')
        default_columns = ('start', 'end')
