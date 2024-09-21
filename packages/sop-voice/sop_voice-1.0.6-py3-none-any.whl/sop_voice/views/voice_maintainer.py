from django.utils.translation import gettext_lazy as _

from netbox.views import generic

from  sop_utils.utils import count_all_sda_list

from ..models import VoiceMaintainer, SiteVoiceInfo, VoiceSda
from ..forms.voice_maintainer import *
from ..tables.voice_maintainer import *


__all__ = (
    'VoiceMaintainerDetailView',
    'VoiceMaintainerEditView',
    'VoiceMaintainerDeleteView',
    'VoiceMaintainerBulkDeleteView',
)


class VoiceMaintainerListView(generic.ObjectListView):
    queryset = VoiceMaintainer.objects.all()
    table = VoiceMaintainerTable


class CheckMaintainerJSONFormat:
    def __init__(self, data):
        self.data = data

    def format(self, value:str) -> str:
        invalid:list = ['\n', '\"', '[', ']', '\'', '>']

        try:return ''.join(n for n in value if n not in invalid)
        except:return value        

    def check_format(self):
        checked = []
        
        for data in self.data:
            if len(data) <= 1:
                return None
            try:
                try:name = data.split(',')
                except:name = data
                checked.append({"name": self.format(name)})
            except:return None

        return checked
    
    
class VoiceMaintainerDetailView(generic.ObjectView):
    queryset = VoiceMaintainer.objects.all()

    def count_sda(self, sites) -> tuple[int, int]:
        '''
        num_count = count of all numbers
        range_count = count of all ranges
        '''
        num_count: int = 0
        range_count: int = 0

        for instance in sites:
            temp = count_all_sda_list(VoiceSda.objects.filter(delivery__site=instance.site))
            num_count += temp.__int__()[0]
            range_count += temp.__int__()[1]

        return num_count, range_count

    def get_extra_context(self, request, instance):
        context: dict = {}

        sites = SiteVoiceInfo.objects.filter(maintainer=instance)
        tmp: tuple[int, int] = self.count_sda(sites)
        context['num_site'] = SiteVoiceInfo.objects.filter(maintainer=instance).count()
        context['num_sda'] = tmp[0]
        context['num_range'] = tmp[1]
        return context


class VoiceMaintainerEditView(generic.ObjectEditView):
    '''
    edits a maintainer instance
    '''
    queryset = VoiceMaintainer.objects.all()
    form = VoiceMaintainerForm


class VoiceMaintainerDeleteView(generic.ObjectDeleteView):
    '''
    deletes a maintainer instance
    '''
    queryset = VoiceMaintainer.objects.all()


class VoiceMaintainerBulkDeleteView(generic.BulkDeleteView):
    '''
    delete selected view
    '''
    queryset = VoiceMaintainer.objects.all()
    table = VoiceMaintainerTable
