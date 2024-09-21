from django.utils.translation import gettext_lazy as _

from netbox.registry import registry
from netbox.navigation import *
from netbox.navigation.menu import MENUS


VOICE = Menu(
    label=_('Voice'),
    icon_class="mdi mdi-phone",
    groups=(
        MenuGroup(
            label=_('Maintainer'),
            items=(
                MenuItem(
                    link=f'plugins:sop_voice:voicemaintainer_list',
                    link_text=_('Voice Maintainer'),
                    permissions=[f'sop_voice.view_voicemaintainer'],
                    buttons=(
                        MenuItemButton(
                            link=f'plugins:sop_voice:voicemaintainer_add',
                            title='Add',
                            icon_class='mdi mdi-plus-thick',
                            permissions=[f'sop_voice.add_voicemaintainer'],
                        ),
                    ),
                ),
            ),
        ),
    ),
)

MENUS.append(VOICE)
