from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.contrib import messages

from utilities.permissions import get_permission_for_model
from netbox.views import generic

from sop_utils.utils import *

from ..forms.sda_list import *
from ..tables.sda_list import *
from ..models import *


__all__ = (
    'SDA_ListEditView',
    'SDA_ListDeleteView',
    'SDA_ListDetailView',
    'SDA_ListAddView',
    'SDA_ListImportView',
    'SDA_ListBulkEditView',
    'SDA_ListBulkDeleteView'
)


class SDA_ListBulkEditView(generic.BulkEditView):
    '''
    for the "edit selected" view
    '''
    queryset = SDA_List.objects.all()
    table = SDA_ListTable
    form = SDA_ListForm


class SDA_ListBulkDeleteView(generic.BulkDeleteView):
    '''
    for the "delete selected" view
    '''
    queryset = SDA_List.objects.all()
    table = SDA_ListTable

    def get_return_url(self, request, obj=None):
        return f'/dcim/sites'


class SDA_ListEditView(generic.ObjectEditView):
    '''
    edits a SDA List instance
    '''
    queryset = SDA_List.objects.all()
    form = SDA_ListForm

    def get_return_url(self, request, obj=None):
        return '/dcim/sites/' + str(obj.delivery.site.id) + '/voice/'


class SDA_ListDeleteView(generic.ObjectDeleteView):
    '''
    deletes a SDA List instance
    '''
    queryset = SDA_List.objects.all()


class SDA_ListDetailView(generic.ObjectView, PermissionRequiredMixin):
    '''
    returns the SDA List detial page with context
    '''
    queryset = SDA_List.objects.all()


class SDA_ListAddView(CustomAddView):
    '''
    creates a new SDA List instance
    '''
    template_name: str = 'sop_utils/tools/form.html'
    model = SDA_List
    form = SDA_ListForm

    def check_errors(self, request, pk=None) -> bool:
        if pk is None:
            return True
        if not VoiceDelivery.objects.filter(site=pk).exists():
            messages.warning(request, _('No delivery found, please create one first.'))
            return True
        return False

    def get_form_context(self, form, pk=None):
        if pk is not None and form is not None:
            delivery = VoiceDelivery.objects.filter(site=pk)
            form.fields['delivery'].queryset = delivery
        return form

    def save_form(self, request, form, site=None) -> None:
        try:
            if form.cleaned_data['end'] == '':
                form.cleaned_data['end'] = form.cleaned_data['start']
            SDA_List(**form.cleaned_data).save()
            messages.success(request, _(f'Successfully added a {self.model._meta.verbose_name}.'))
        except:
            messages.error(request, _(f'Error adding a {self.model._meta.verbose_name}.'))
        return


class SDA_ListImportView(View, AccessMixin):
    '''
    import a list  of SDA numbers
    the JSON norm is:
    ```
    [
        "start  >>  end",
    ]
    ```
    '''
    template: str = 'sop_utils/tools/form.html'

    def get_extra_context(self, request, delivery, pk) -> dict:
        '''
        returns extra context for the form
        '''
        form = SDA_ListImportForm(request.GET)
        if delivery is not None:
            form.fields['delivery'].queryset = VoiceDelivery.objects.filter(site=pk)
        return_url = f'/dcim/sites/{pk}/voice/'
        return {'form': form, 'object': SDA_List, 'model': SDA_List._meta.verbose_name.title(),
            'return_url': return_url, 'title': f'Import new SDA'}

    def get(self, request, pk):
        '''
        returns the form
        '''
        if not request.user.has_perm(get_permission_for_model(SDA_List, 'add')):
            return self.handle_no_permission()
        try:
            delivery = get_object_or_404(VoiceDelivery, site=pk)
        except:
            messages.warning(request, _('No delivery found, please create one first.'))
            delivery = None
            return redirect('/dcim/sites/' + str(pk) + '/voice/')
        return render(request, self.template, self.get_extra_context(request, delivery, pk))

    def save_form(self, request, form, delivery, pk) -> bool:
        '''
        check if the JSON format is valid and save the form data
        '''
        obj = CheckJSONImportFormat(form.cleaned_data['json_import'])
        checked: list[dict[str, str]]|None = obj.check_format()
        count: int = 0

        '''
        for every line in the json file, create a new SDA_List instance
        '''
        if checked is None:
            return False
        [SDA_List(start=data['start'],end=data['end'],delivery=delivery).save() for data in checked]
        messages.success(request, _('Successfully imported numbers'))
        return True


    def post(self, request, pk):
        if not request.user.has_perm(get_permission_for_model(SDA_List, 'add')):
            return self.handle_no_permission()
        try:
            delivery = get_object_or_404(VoiceDelivery, site=pk)
        except:
            messages.warning(request, _('No delivery found, please create one first.'))
            delivery = None
            return redirect('/dcim/sites/' + str(pk) + '/voice/')
        form = SDA_ListImportForm(request.POST)
        form.fields['delivery'].queryset = VoiceDelivery.objects.filter(site=pk)

        if form.is_valid() and self.save_form(request, form, delivery, pk):
            return redirect('/dcim/sites/' + str(pk) + '/voice/')

        messages.error(request, _('Invalid JSON'))
        return render(request, self.template, self.get_extra_context(request, delivery, pk))
