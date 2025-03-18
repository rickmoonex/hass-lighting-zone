"""Constants for Lighing Zone."""

import voluptuous as vol
from homeassistant.const import Platform
from homeassistant.helpers import config_validation as cv

DOMAIN = "lighting_zone"

PLATFORMS = [Platform.BINARY_SENSOR]

CONF_MEMBERS = "members"

SERVICE_DIM_ZONE_ABSOLUTE = "dim_zone_absolute"
FIELD_DIM_LEVEL = "dim_level"
SERVICE_DIM_ZONE_ABSOLUTE_SCHEMA = {vol.Required(FIELD_DIM_LEVEL): cv.positive_int}

SERVICE_DIM_ZONE_RELATIVE = "dim_zone_relative"
FIELD_AMOUNT = "amount"
SERVICE_DIM_ZONE_RELATIVE_SCHEMA = {vol.Required(FIELD_AMOUNT): int}
