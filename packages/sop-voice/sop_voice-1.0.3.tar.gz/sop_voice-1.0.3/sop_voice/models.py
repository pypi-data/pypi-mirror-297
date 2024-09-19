from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from netbox.models import NetBoxModel
from circuits.models import Provider
from dcim.models import Site

from sop_utils.models import *
from sop_utils.utils import *


__all__ = (
    'SDA_List',
    'VoiceDelivery',
    'SiteVoiceInfo',
    'BTIPMigration',
    'RingCentralMigration',
    'VoiceMaintainer'
)


class VoiceMaintainer(NetBoxModel):
    name = models.CharField(
        verbose_name=_('Maintainer'),
    )

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicemaintainer_detail', args=[self.pk])

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Voice Maintainer')
        verbose_name_plural = _('Voice Maintainers')


class SiteVoiceInfo(NetBoxModel):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
    )
    maintainer = models.ForeignKey(
        VoiceMaintainer,
        on_delete=models.CASCADE,
        verbose_name=_('Maintainer'),
        help_text=_('The maintainer of the site.'),
    )

    def __str__(self) -> str:
        try:
            return f'"{self.site} - {self.maintainer}"'
        except:
            return f'site maintainer'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:sitevoiceinfo_detail', args=[self.pk])

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Site Maintainer')
        verbose_name_plural = _('Sites Maintainer')


class VoiceDelivery(NetBoxModel):
    delivery = models.CharField(
        verbose_name=_('Delivery'),
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='voice_delivery_provider',
        verbose_name=_('Provider')
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='voice_delivery_site',
        verbose_name=_('Site'),
    )
    channel_count = models.CharField(
        verbose_name=_('Channel Count'),
    )
    status = models.CharField(
        max_length=30,
        choices=VoiceDeliveryStatusChoices,
        verbose_name=_('Status'),
    )
    ndi = models.CharField(
        max_length=100,
        verbose_name=_('NDI'),
    )
    dto = models.CharField(
        max_length=100,
        verbose_name=_('DTO'),
    )

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicedelivery_detail', args=[self.pk])

    def get_status_color(self) -> str:
        return VoiceDeliveryStatusChoices.colors.get(self.status)

    def __str__(self) -> str:
        return f'"{self.delivery} / {self.provider}"'

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Voice Delivery')
        verbose_name_plural = _('Voice Deliveries')


class SDA_List(NetBoxModel):
    delivery = models.ForeignKey(
        VoiceDelivery,
        on_delete=models.CASCADE,
        related_name='sda_list_delivery',
        verbose_name=_('Delivery'),
        help_text=_('The voice delivery.'),
    )
    start = models.CharField(
        max_length=100,
        unique=False,
        verbose_name=_('Start'),
        help_text=_('Start number of the range.'),
    )
    end = models.CharField(
        max_length=100,
        unique=False,
        verbose_name=_('End'),
        help_text=_('End number of the range. Can be left blank if the range is only one number.'),
    )

    def __str__(self) -> str:
        return f'"{self.start} >> {self.end}"'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:sda_list_detail', args=[self.pk])

    class Meta(NetBoxModel.Meta):
        ordering = ('start',)
        verbose_name = _('SDA')
        verbose_name_plural = _('SDA List')


class RingCentralMigration(NetBoxModel):
    hardware = models.CharField(
        choices=SopBoolChoices,
        verbose_name=_('Hardware'),
        help_text=_('Set to True if you can positively confirm that no phone related hardware is visible on the site.'),
    )
    vlan = models.CharField(
        choices=SopBoolChoices,
        verbose_name=_('VLAN'),
        help_text=_('Set to True if you can positively confirm that there is no old/historical voice VLAN configured on the site.'),
    )
    client = models.CharField(
        choices=SopBoolChoices,
        verbose_name=_('Client'),
        help_text=_('Set to True if you can positively confirm that there is no voice client visible in the Meraki dashboard.'),
    )
    migration = models.CharField(
        choices=SopBoolChoices,
        verbose_name=_('Migration'),
        help_text=_('Set to True if you can positively confirm that the Ring Central Migration is done on this site.'),
    )
    site = models.ForeignKey(
        to=Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
    )

    def __str__(self) -> str:
        return f'"{self.site}"'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:ringcentralmigration_detail', args=[self.pk])

    def get_hardware_color(self) -> str:
        return SopBoolChoices.colors.get(self.hardware)

    def get_vlan_color(self) -> str:
        return SopBoolChoices.colors.get(self.vlan)

    def get_client_color(self) -> str:
        return SopBoolChoices.colors.get(self.client)

    def get_migration_color(self) -> str:
        return SopBoolChoices.colors.get(self.migration)

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Ring Central Migration')
        verbose_name_plural = _('Ring Central Migrations')


class BTIPMigration(NetBoxModel):
    hardware = models.CharField(
        choices=SopBoolChoices,
        verbose_name=_('Hardware'),
        help_text=_('Set to True if you can positively confirm that no phone related hardware is visible on the site.'),
    )
    migration = models.CharField(
        choices=SopBoolChoices,
        verbose_name=_('Migration'),
        help_text=_('Set to True if you can positively confirm that the BTIP Migration is done on this site.'),
    )
    site = models.ForeignKey(
        to=Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
    )

    def __str__(self) -> str:
        return f'"{self.site}"'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:btipmigration_detail', args=[self.pk])

    def get_hardware_color(self) -> str:
        return SopBoolChoices.colors.get(self.hardware)

    def get_migration_color(self) -> str:
        return SopBoolChoices.colors.get(self.migration)

    class Meta(NetBoxModel.Meta):
        verbose_name = _('BTIP Migration')
        verbose_name_plural = _('BTIP Migrations')
