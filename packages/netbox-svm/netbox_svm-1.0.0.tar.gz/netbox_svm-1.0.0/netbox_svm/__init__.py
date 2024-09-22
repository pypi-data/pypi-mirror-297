from netbox.plugins import PluginConfig

__version__ = "1.0.0"


class SLMConfig(PluginConfig):
    name = "netbox_svm"
    verbose_name = "Software Version Management"
    description = "Software Version Management Netbox Plugin."
    version = __version__
    author = "hungnv99"
    author_email = "open-source-projects@hungnv99.vn"
    base_url = "slm"
    required_settings = []
    default_settings = {"version_info": False}


config = SLMConfig
