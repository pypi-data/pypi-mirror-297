from django.urls import path

from netbox.views.generic import ObjectChangeLogView, ObjectJournalView

from .views import voice_maintainer as vm
from .views import voice_delivery as vd
from .views import sda_list as sda
from .views import ring_central_migration as rc
from .views import btip_migration as btip
from .views import site_voice_info as svi
from .views import tab_view

from .models import *


app_name = 'sop_voice'


urlpatterns = [

    # voice maintainer
    path('voicemaintainer_list', vm.VoiceMaintainerListView.as_view(), name='voicemaintainer_list'),
    path('voicemaintainer/<int:pk>', vm.VoiceMaintainerDetailView.as_view(), name='voicemaintainer_detail'),
    path('voicemaintainer/add', vm.VoiceMaintainerEditView.as_view(), name='voicemaintainer_add'),
    path('voicemaintainer/delete/', vm.VoiceMaintainerBulkDeleteView.as_view(), name='voicemaintainer_bulk_delete'),
    path('voicemaintainer/edit/<int:pk>', vm.VoiceMaintainerEditView.as_view(), name='voicemaintainer_edit'),
    path('voicemaintainer/import/', vm.VoiceMaintainerEditView.as_view(), name='voicemaintainer_import'),
    path('voicemaintainer/delete/<int:pk>', vm.VoiceMaintainerDeleteView.as_view(), name='voicemaintainer_delete'),
    path('voicemaintainer/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='voicemaintainer_changelog', kwargs={'model': VoiceMaintainer}),
    path('voicemaintainer/journal/<int:pk>', ObjectJournalView.as_view(), name='voicemaintainer_journal', kwargs={'model': VoiceMaintainer}),

    # voice delivery
    path('voice-delivery/<int:pk>', vd.VoiceDeliveryDetailView.as_view(), name='voicedelivery_detail'),
    path('voice-delivery/add', vd.VoiceDeliveryAddView.as_view(), name='voicedelivery_add'),
    path('voice-delivery/edit', vd.VoiceDeliveryBulkEditView.as_view(), name='voicedelivery_bulk_edit'),
    path('voice-delivery/delete', vd.VoiceDeliveryBulkDeleteView.as_view(), name='voicedelivery_bulk_delete'),
    path('voice-delivery/add/<int:pk>', vd.VoiceDeliveryAddView.as_view(), name='voicedelivery_add'),
    path('voice-delivery/edit/<int:pk>', vd.VoiceDeliveryEditView.as_view(), name='voicedelivery_edit'),
    path('voice-delivery/delete/<int:pk>', vd.VoiceDeliveryDeleteView.as_view(), name='voicedelivery_delete'),
    path('voice-delivery/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='voicedelivery_changelog', kwargs={'model': VoiceDelivery}),
    path('voice-delivery/journal/<int:pk>', ObjectJournalView.as_view(), name='voicedelivery_journal', kwargs={'model': VoiceDelivery}),

    # sda list
    path('sda-list/<int:pk>', sda.SDA_ListDetailView.as_view(), name='sda_list_detail'),
    path('sda-list/add/', sda.SDA_ListAddView.as_view(), name='sda_list_add'),
    path('sda-list/edit/', sda.SDA_ListBulkEditView.as_view(),  name='sda_list_bulk_edit'),
    path('sda-list/delete/', sda.SDA_ListBulkDeleteView.as_view(), name='sda_list_bulk_delete'),
    path('sda-list/add/<int:pk>', sda.SDA_ListAddView.as_view(), name='sda_list_add'),
    path('sda-list/edit/<int:pk>', sda.SDA_ListEditView.as_view(), name='sda_list_edit'),
    path('sda-list/delete/<int:pk>', sda.SDA_ListDeleteView.as_view(), name='sda_list_delete'),
    path('sda-list/import/<int:pk>', sda.SDA_ListImportView.as_view(), name='sda_list_import'),
    path('sda-list/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='sda_list_changelog', kwargs={'model': SDA_List}),
    path('sda-list/journal/<int:pk>', ObjectJournalView.as_view(), name='sda_list_journal', kwargs={'model': SDA_List}),
 
    # ring central migration
    path('ring-central-migration/<int:pk>', rc.RingCentralMigrationDetailView.as_view(), name='ringcentralmigration_detail'),
    path('ring-central-migration/edit/<int:pk>', rc.RingCentralMigrationEditView.as_view(), name='ringcentralmigration_edit'),
    path('ring-central-migration/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='ringcentralmigration_changelog', kwargs={'model': RingCentralMigration}),
    path('ring-central-migration/journal/<int:pk>', ObjectJournalView.as_view(), name='ringcentralmigration_journal', kwargs={'model': RingCentralMigration}),

    # btip migration
    path('btip-migration/<int:pk>', btip.BTIPMigrationDetailView.as_view(), name='btipmigration_detail'),
    path('btip-migration/edit/<int:pk>', btip.BTIPMigrationEditView.as_view(), name='btipmigration_edit'),
    path('btip-migration/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='btipmigration_changelog', kwargs={'model': BTIPMigration}),
    path('btip-migration/journal/<int:pk>', ObjectJournalView.as_view(), name='btipmigration_journal', kwargs={'model': BTIPMigration}),

    # site voice info
    path('site-voice-info/<int:pk>', svi.SiteVoiceInfoRedirectView.as_view(), name='sitevoiceinfo_detail'),
    path('site-voice-info/add/', svi.SiteVoiceInfoAddView.as_view(), name='sitevoiceinfo_add'),
    path('site-voice-info/add/<int:pk>', svi.SiteVoiceInfoAddView.as_view(), name='sitevoiceinfo_add'),
    path('site-voice-info/edit/<int:pk>', svi.SiteVoiceInfoEditView.as_view(), name='sitevoiceinfo_edit'),
    path('site-voice-info/delete/<int:pk>', svi.SiteVoiceInfoDeleteView.as_view(), name='sitevoiceinfo_delete'),
    path('site-voice-info/changelog/<int:pk>', ObjectChangeLogView.as_view(), name='sitevoiceinfo_changelog', kwargs={'model': SiteVoiceInfo}),
    path('site-voice-info/journal/<int:pk>', ObjectJournalView.as_view(), name='sitevoiceinfo_journal', kwargs={'model': SiteVoiceInfo}),
]
