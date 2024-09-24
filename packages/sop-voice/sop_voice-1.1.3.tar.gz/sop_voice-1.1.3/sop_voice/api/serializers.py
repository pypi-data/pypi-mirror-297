from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer

from ..models import *


__all__ = (
    'VoiceDeliverySerializer',
    'NestedVoiceDeliverySerializer',
    'VoiceSdaSerializer',
    'NestedVoiceSdaSerializer',
    'SiteVoiceInfoSerializer',
    'NestedSiteVoiceInfoSerializer',
    'VoiceMaintainerSerializer',
    'NestedVoiceMaintainerSerializer'
)


#
# site voice maintainer
#


class VoiceMaintainerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicemaintainer-detail'
    )

    class Meta:
        model = VoiceMaintainer
        fields = ('url', 'name', )


class NestedVoiceMaintainerSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicemaintainer-detail'
    )

    class Meta:
        model = VoiceMaintainer
        fields = ('url', 'name', )


#
# site voice info
#


class SiteVoiceInfoSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:sitevoiceinfo-detail'
    )

    class Meta:
        model = SiteVoiceInfo
        fields = ('url', 'id', 'site', 'maintainer')


class NestedSiteVoiceInfoSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:sitevoiceinfo-detail'
    )

    class Meta:
        model = SiteVoiceInfo
        fields = ('url', 'id', 'site', 'maintainer')


#
# sda list
#


class VoiceSdaSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicesda-detail'
    )

    class Meta:
        model = VoiceSda
        fields = ('url', 'id', 'delivery', 'start', 'end')


class NestedVoiceSdaSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicesda-detail'
    )

    class Meta:
        model = VoiceSda
        fields = ('url', 'id', 'delivery', 'start', 'end')


#
# voice delivery
#


class VoiceDeliverySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicedelivery-detail'
    )

    class Meta:
        model = VoiceDelivery
        fields = ('url', 'id', 'delivery', 'provider', 'site',
                'channel_count', 'status'
        )


class NestedVoiceDeliverySerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicedelivery-detail'
    )

    class Meta:
        model = VoiceDelivery
        fields = ('url', 'id', 'delivery', 'provider', 'site',
                'channel_count', 'status'
        )
