"""Config flow for Lighting Zone."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import voluptuous as vol
from homeassistant.components.light.const import DOMAIN as LIGHT_DOMAIN
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import CONF_MEMBERS, DOMAIN

if TYPE_CHECKING:
    from collections.abc import Mapping

OPTIONS_SCHEMA = {
    vol.Required(CONF_MEMBERS): selector.EntitySelector(
        selector.EntitySelectorConfig(domain=LIGHT_DOMAIN, multiple=True)
    )
}

CONFIG_SCHEMA = {vol.Required(CONF_NAME): selector.TextSelector(), **OPTIONS_SCHEMA}

CONFIG_FLOW = {"user": SchemaFlowFormStep(vol.Schema(CONFIG_SCHEMA))}

OPTIONS_FLOW = {"init": SchemaFlowFormStep(vol.Schema(OPTIONS_SCHEMA))}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or option flow."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        return cast("str", options["name"])
