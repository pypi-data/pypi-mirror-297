from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.choices import ButtonColorChoices
from packaging import version


try:
    from netbox.plugins import PluginMenu
    HAVE_MENU = True
except ImportError:
    HAVE_MENU = False
    PluginMenu = PluginMenuItem

menu_buttons = (
    PluginMenuItem(
        link="plugins:netbox_slm:softwareproduct_list",
        link_text="Software Products",
        permissions=["netbox_slm.add_softwareproduct"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_slm:softwareproduct_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_slm.add_softwareproduct"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_slm:softwareproductversion_list",
        link_text="Versions",
        permissions=["netbox_slm.add_softwareproductversion"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_slm:softwareproductversion_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_slm.add_softwareproductversion"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_slm:softwareproductinstallation_list",
        link_text="Installations",
        permissions=["netbox_slm.add_softwareproductinstallation"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_slm:softwareproductinstallation_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_slm.add_softwareproductinstallation"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_slm:softwarelicense_list",
        link_text="Licenses",
        permissions=["netbox_slm.add_softwarelicense"],
        buttons=(
            PluginMenuButton(
                "plugins:netbox_slm:softwarelicense_add",
                "Add",
                "mdi mdi-plus-thick",
                permissions=["netbox_slm.add_softwarelicense"],
            ),
        ),
    ),
)


if HAVE_MENU:
    menu = PluginMenu(
        label=f'Software Management',
        groups=(
            ('Software Lifecycle Management', menu_buttons),
        ),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    # display under plugins
    menu_items = menu_buttons