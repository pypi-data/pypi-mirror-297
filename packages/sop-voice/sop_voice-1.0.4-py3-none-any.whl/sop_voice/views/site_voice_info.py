from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views import View

from dcim.models import Site
from netbox.views import generic

from sop_utils.utils import *

from ..forms.site_voice_info import *
from ..models import SiteVoiceInfo, VoiceMaintainer


__all__ = (
    'SiteVoiceInfoEditView',
    'SiteVoiceInfoAddView',
    'SiteVoiceInfoRedirectView',
    'SiteVoiceInfoDeleteView'
)


class SiteVoiceInfoRedirectView(View):
    '''
    redirects to the site voice info page
    '''
    def get(self, request, pk=None):
        return redirect('/dcim/sites/')


class SiteVoiceInfoAddView(CustomAddView):
    template_name = 'sop_utils/tools/form.html'
    model = SiteVoiceInfo
    form = SiteVoiceInfoForm

    def get_return_url(self, request, pk=None) -> str:
        try:
            return '/dcim/sites/' + str(pk) + '/voice/'
        except:
            return '/dcim/sites'

    def get_error_url(self, request, pk=None) -> str:
        return f'/plugins/sop-voice/voicemaintainer/add'

    def check_errors(self, request, pk=None) -> bool:
        if not VoiceMaintainer.objects.all().exists():
            messages.warning(request, f'No maintainer found, please add one first.')
            return True
        return False

    def get_extra_context(self, request, pk=None) -> dict:
        try:site = Site.objects.filter(pk=pk).first().name
        except:site = 'site'
        form = self.form
        return_url = self.get_return_url(request, pk)
        return {
            'object': self.model, 'form': form, 'model': self.model._meta.verbose_name.title(),
            'return_url': return_url, 'title': f'Editing {site} voice maintainer'
        }

class SiteVoiceInfoEditView(CustomEditView):
    '''
    creates a new site voice info object
    or edits an existing one
    '''
    template_name: str = 'sop_utils/tools/form.html'
    model = SiteVoiceInfo
    form = SiteVoiceInfoForm

    def get_return_url(self, request, pk=None) -> str:
        try:
            obj = SiteVoiceInfo.objects.filter(pk=pk).first().site.id
            if pk is not None:
                return f'/dcim/sites/{obj}/voice'
        except:pass
        return '/dcim/sites/'


class SiteVoiceInfoDeleteView(generic.ObjectDeleteView):
    queryset = SiteVoiceInfo.objects.all()

    def get_return_url(self, request, obj=None) -> str:
        try:
            if obj is None:
                raise Exception
            return f'/dcim/sites/{obj.site.pk}'
        except:
            return '/dcim/sites/'
