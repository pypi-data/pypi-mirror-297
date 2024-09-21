from netbox.views import generic

from ..forms.btip_migration import *
from ..models import BTIPMigration, SiteVoiceInfo


class BTIPMigrationDetailView(generic.ObjectView):
    '''
    returns the BTIP Migration detail page with context
    '''
    queryset = BTIPMigration.objects.all()

    def get_extra_context(self, request, instance) -> dict:
        context: dict = {}
        
        try:
            site_info = SiteVoiceInfo.objects.filter(site=instance.site).first()
            maintainer = site_info.maintainer.title()
        except:
            maintainer = None
        context['maintainer'] = maintainer
        return context


class BTIPMigrationEditView(generic.ObjectEditView):
    '''
    edits one BTIP Migration object
    '''
    queryset = BTIPMigration.objects.all()
    form = BTIPMigrationForm

    def get_return_url(self, request, obj=None) -> str:
        return '/dcim/sites/' + str(obj.site.id) + '/voice/'
