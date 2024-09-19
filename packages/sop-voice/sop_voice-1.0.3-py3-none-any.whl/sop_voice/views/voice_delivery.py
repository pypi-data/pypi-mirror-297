from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from circuits.models import Provider

from sop_utils.utils import *

from ..forms.voice_delivery import VoiceDeliveryForm
from ..tables.voice_delivery import *
from ..tables.sda_list import *
from ..models import *


__all__ =  (
    'VoiceDeliveryDetailView',
    'VoiceDeliveryEditView',
    'VoiceDeliveryDeleteView',
    'VoiceDeliveryBulkEditView',
    'VoiceDeliveryDeleteView'
)


class VoiceDeliveryBulkEditView(generic.BulkEditView):
    queryset = VoiceDelivery.objects.all()
    table = VoiceDeliveryTable
    form = VoiceDeliveryForm

    def get_return_url(self, request, obj=None):
        try:
            if obj is None:raise Exception
            return f'/dcim/sites/{obj.site}/'
        except:return '/dcim/sites'


class VoiceDeliveryBulkDeleteView(generic.BulkDeleteView):
    queryset = VoiceDelivery.objects.all()
    table = VoiceDeliveryTable

    def get_return_url(self, request, obj=None):
        try:
            if obj is None:raise Exception
            return f'/dcim/sites/{obj.site}/'
        except:return '/dcim/sites'


class VoiceDeliveryDetailView(generic.ObjectView, PermissionRequiredMixin):
    '''
    returns the Voice Delivery detail page with context
    '''
    queryset = VoiceDelivery.objects.all()

    def get_extra_context(self, request, instance) -> dict:
        context: dict = {}

        sda_list = SDA_List.objects.filter(delivery=instance)
        temp: tuple[int, int] = count_all_sda_list(sda_list).__int__()

        try:
            site_info = SiteVoiceInfo.objects.filter(site=instance.site.id)
            context['maintainer'] = site_info.first().maintainer
        except:pass
        context['num_sda'] = temp[0]
        context['num_range'] = temp[1]
        return context


class VoiceDeliveryAddView(CustomAddView):
    '''
    creates anew Voice Delivery instance
    '''
    template_name: str = 'sop_utils/tools/form.html'
    model = VoiceDelivery
    form = VoiceDeliveryForm

    def get_return_url(self, request, pk=None):
        if pk is not None:
            return f'/dcim/sites/{pk}/voice/'
        return '/dcim/sites/'

    def check_errors(self, request, pk=None) -> bool:
        if not Provider.objects.all().exists():
            messages.warning(request, _('No provider found, pease create one first.'))
            return False
        return False


class VoiceDeliveryEditView(CustomEditView):
    template_name: str = 'sop_utils/tools/form.html'
    model = VoiceDelivery
    form = VoiceDeliveryForm

    def get_return_url(self, request, pk=None) -> str:
        try:
            obj = VoiceDelivery.objects.filter(pk=pk).first().site.id
            if pk is not None:
                return f'/dcim/sites/{obj}/voice'
        except:pass
        return '/dcim/sites/'

    def check_errors(self, request, pk=None) -> bool:
        if not Provider.objects.all().exists():
            messages.warning(request, _('No provider found, please create one first.'))
            return False
        return False
        


class VoiceDeliveryDeleteView(generic.ObjectDeleteView, PermissionRequiredMixin):
    '''
    deletes a Voice Delivery object
    '''
    queryset = VoiceDelivery.objects.all()
