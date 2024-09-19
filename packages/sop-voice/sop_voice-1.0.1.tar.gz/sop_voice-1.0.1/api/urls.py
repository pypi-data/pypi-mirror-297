from netbox.api.routers import NetBoxRouter

from .views import *


router = NetBoxRouter()

router.register('voice-deliveries', VoiceDeliveryViewSet)
router.register('sda-lists', SDA_ListViewSet)
router.register('ring-central-migrations', RingCentralMigrationViewSet)
router.register('btip-migrations', BTIPMigrationViewSet)
router.register('site-voice-infos', SiteVoiceInfoViewSet)
router.register('voice-maintainers', VoiceMaintainerViewSet)

urlpatterns = router.urls
