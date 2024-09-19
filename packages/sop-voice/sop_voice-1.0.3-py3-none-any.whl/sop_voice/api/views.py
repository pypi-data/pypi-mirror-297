from netbox.api.viewsets import NetBoxModelViewSet
from netbox.api.metadata import ContentTypeMetadata

from ..models import *
from .serializers import *


__all__ = (
    'VoiceDeliveryViewSet',
    'SDA_ListViewSet',
    'RingCentralMigrationViewSet',
    'BTIPMigrationViewSet',
    'SiteVoiceInfoViewSet',
    'VoiceMaintainerViewSet',
)


class VoiceMaintainerViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = VoiceMaintainer.objects.all()
    serializer_class = VoiceMaintainerSerializer


class SiteVoiceInfoViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = SiteVoiceInfo.objects.all()
    serializer_class = SiteVoiceInfoSerializer


class RingCentralMigrationViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = RingCentralMigration.objects.all()
    serializer_class = RingCentralMigrationSerializer


class BTIPMigrationViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = BTIPMigration.objects.all()
    serializer_class = BTIPMigrationSerializer


class SDA_ListViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = SDA_List.objects.all()
    serializer_class = SDA_ListSerializer


class VoiceDeliveryViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = VoiceDelivery.objects.all()
    serializer_class = VoiceDeliverySerializer
