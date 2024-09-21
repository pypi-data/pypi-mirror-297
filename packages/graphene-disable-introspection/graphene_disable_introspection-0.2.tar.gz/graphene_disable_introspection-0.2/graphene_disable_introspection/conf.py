from django.conf import settings as dj_settings
from django.core.signals import setting_changed

from graphene_disable_introspection.validators import (
    validate_disabled_introspection_types,
)

__all__ = ["settings"]


class GrapheneDisableIntrospectionSettings(object):
    """
    Class that holds introspection settings.

    The settings object is an instance of this class and is reloaded when
    the ``setting_changed`` signal is dispatched.
    """

    SETTINGS = {
        "DISABLED_INTROSPECTION_TYPES": (
            "DISABLED_INTROSPECTION_TYPES",
            ["__schema", "__type", "__typename"],
        )
    }

    def __init__(self):
        # make sure we don't assign self._settings directly here, to avoid
        # recursion in __setattr__, we delegate to the parent instead
        super(GrapheneDisableIntrospectionSettings, self).__setattr__("_settings", {})
        self.load()

    def load(self):
        for user_setting, (introspection_setting, default) in self.SETTINGS.items():
            value = getattr(dj_settings, user_setting, default)
            if introspection_setting == "DISABLED_INTROSPECTION_TYPES":
                validate_disabled_introspection_types(value)
            self._settings[introspection_setting] = value

    def reload(self):
        self.__init__()

    def __getattr__(self, attr):
        if attr not in self._settings:
            raise AttributeError(
                "'GrapheneDisableIntrospectionSettings' object has not attribute '%s'"
                % attr
            )
        return self._settings[attr]

    def __setattr__(self, attr, value):
        if attr not in self._settings:
            raise AttributeError(
                "'GrapheneDisableIntrospectionSettings' object has not attribute '%s'"
                % attr
            )
        self._settings[attr] = value


# Signal handler to reload settings when needed
def reload_settings(*args, **kwargs):
    val = kwargs.get("setting")
    if val in settings.SETTINGS:
        settings.reload()


# Connect the setting_changed signal to our handler
setting_changed.connect(reload_settings)

# This is our global settings object
settings = GrapheneDisableIntrospectionSettings()
