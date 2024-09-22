from netbox.plugins import PluginConfig

__version__ = "1.8.3"


class SLMConfig(PluginConfig):
    name = "netbox_slm"
    verbose_name = "Software Lifecycle Management"
    description = "Software Lifecycle Management Netbox Plugin."
    version = __version__
    author = "hungnv99"
    author_email = "open-source-projects@hungnv99.vn"
    base_url = "slm"
    required_settings = []
    default_settings = {"version_info": False}


config = SLMConfig
