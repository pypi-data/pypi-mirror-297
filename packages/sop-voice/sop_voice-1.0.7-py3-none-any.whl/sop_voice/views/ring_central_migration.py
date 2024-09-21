from netbox.views import generic

from ..forms.ring_central_migration import *
from ..models import RingCentralMigration, SiteVoiceInfo


class RingCentralMigrationDetailView(generic.ObjectView):
    '''
    returns the Ring Central Migration detail page with context
    '''
    queryset = RingCentralMigration.objects.all()

    def get_extra_context(self, request, instance) -> dict:
        context: dict = {}
        
        try:
            site_info = SiteVoiceInfo.objects.filter(site=instance.site).first()
            maintainer = site_info.maintainer.title()
        except:
            maintainer = None
        context['maintainer'] = maintainer
        return context


class RingCentralMigrationEditView(generic.ObjectEditView):
    '''
    edits one Ring Central Migration object
    '''
    queryset = RingCentralMigration.objects.all()
    form = RingCentralMigrationForm

    def get_return_url(self, request, obj=None):
        return '/dcim/sites/' + str(obj.site.id) + '/voice/'

