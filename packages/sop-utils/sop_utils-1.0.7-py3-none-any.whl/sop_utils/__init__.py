from netbox.plugins import PluginConfig


class SopUtilsConfig(PluginConfig):
    name = "sop_utils"
    verbose_name = "SOP Utils"
    description = "Tools for the sop_ plugins."
    version = "1.0.7"
    author = "Leorevoir"
    author_email = "leo.quinzler@epitech.eu"
    base_url = "sop-utils"


config = SopUtilsConfig
