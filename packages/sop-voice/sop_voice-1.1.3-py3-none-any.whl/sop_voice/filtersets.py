import django_filters
from django.db.models import Q
from django.utils.translation import gettext_lazy as _ 

from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import MultiValueCharFilter
from dcim.models import Site

from sop_utils.models import VoiceDeliveryStatusChoices, VoiceMaintainerStatusChoice

from .forms.voice_sda import VoiceSdaFilterForm
from .models import VoiceSda, VoiceDelivery, VoiceMaintainer, SiteVoiceInfo


class VoiceDeliveryFilterSet(NetBoxModelFilterSet):
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='site',
        label=_('Site (ID)')
    )
    status = django_filters.MultipleChoiceFilter(
        choices=VoiceDeliveryStatusChoices,
        null_value=None
    )

    class Meta:
        model = VoiceDelivery
        fields = ('id', 'delivery', 'provider', 'status')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(delivery__icontains=value) |
            Q(start__icontains=value) |
            Q(end__icontains=value)
        )


class VoiceMaintainerFilterSet(NetBoxModelFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=VoiceMaintainerStatusChoice,
        null_value=None
    )

    class Meta:
        model = VoiceMaintainer
        fields = ('id', 'name', 'status')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )


class VoiceSdaFilterSet(NetBoxModelFilterSet):
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        field_name='delivery__site',
        label=_('Site (ID)')
    )
    maintainer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VoiceMaintainer.objects.all(),
        field_name='delivery__site',
        method='sda_maintainer_filter',
        label=_('Maintainer (ID)')
    )
    delivery_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VoiceDelivery.objects.all(),
        field_name='delivery_id',
        label=_('Delivery (ID)')
    )

    class Meta:
        model = VoiceSda
        fields = ('id', 'start', 'end', 'delivery_id')

    def sda_maintainer_filter(self, queryset, name, value):
        if not value:
            return queryset
        site_ids = SiteVoiceInfo.objects.filter(maintainer__in=value).values_list('site_id', flat=True)
        return queryset.filter(delivery__site_id__in=site_ids)

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(delivery__icontains=value) |
            Q(start__icontains=value) |
            Q(end__icontains=value)
        )
