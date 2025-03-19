"""Adds the Lighting Zone's binary sensor."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant.components.binary_sensor import (
    PLATFORM_SCHEMA as BINARY_SENSOR_PLATFORM_SCHEMA,
)
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.components.light.const import (
    DOMAIN as LIGHT_DOMAIN,
)
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIQUE_ID,
    EVENT_HOMEASSISTANT_START,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import (
    CoreState,
    Event,
    EventStateChangedData,
    HomeAssistant,
    callback,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import (
    async_get_current_platform,
)
from homeassistant.helpers.event import (
    async_track_state_change_event,
)

from .const import (
    CONF_MEMBERS,
    SERVICE_DIM_ZONE_ABSOLUTE,
    SERVICE_DIM_ZONE_ABSOLUTE_SCHEMA,
    SERVICE_DIM_ZONE_RELATIVE,
    SERVICE_DIM_ZONE_RELATIVE_SCHEMA,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Lighting Zone"

PLATFORM_SCHEMA_COMMON = vol.Schema(
    {
        vol.Required(CONF_MEMBERS): cv.entity_ids,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)

PLATFORM_SCHEMA = BINARY_SENSOR_PLATFORM_SCHEMA.extend(PLATFORM_SCHEMA_COMMON.schema)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,  # noqa: ANN001
) -> None:
    """Initialize config entry."""
    platform = async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_DIM_ZONE_ABSOLUTE,
        cv.make_entity_service_schema(SERVICE_DIM_ZONE_ABSOLUTE_SCHEMA),
        "dim_zone_absolute",
    )
    platform.async_register_entity_service(
        SERVICE_DIM_ZONE_RELATIVE,
        cv.make_entity_service_schema(SERVICE_DIM_ZONE_RELATIVE_SCHEMA),
        "dim_zone_relative",
    )

    await _async_setup_config(
        hass,
        PLATFORM_SCHEMA_COMMON(dict(config_entry.options)),
        config_entry.entry_id,
        async_add_entities,
    )


async def _async_setup_config(
    hass: HomeAssistant,
    config: Mapping[str, Any],
    unique_id: str | None,
    async_add_entities,  # noqa: ANN001
) -> None:
    """Set up the lighting zone platform."""
    name: str = config[CONF_NAME]
    members: list[str] = config[CONF_MEMBERS]

    async_add_entities([LightingZone(hass, name, members, unique_id)])


class LightingZone(BinarySensorEntity):
    """Representation of a Lighting Zone device."""

    _attr_should_poll = False

    def __init__(
        self,
        _: HomeAssistant,
        name: str,
        members: list[str],
        unique_id: str | None,
    ) -> None:
        """Initialize the Lighting Zone."""
        self._attr_name = name
        self.members = members
        self._attr_unique_id = unique_id

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Add listener
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, self.members, self._async_member_changed
            )
        )

        @callback
        def _async_startup(_: Event | None = None) -> None:
            """Init on startup."""
            self._async_update_zone_state()
            self.async_write_ha_state()

        if self.hass.state is CoreState.running:
            _async_startup()
        else:
            self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, _async_startup)

    async def _async_member_changed(self, _: Event[EventStateChangedData]) -> None:
        """Handle member update."""
        self._async_update_zone_state()
        self.async_write_ha_state()

    @callback
    def _async_update_zone_state(self) -> None:
        states = [
            state.state
            for entity_id in self.members
            if (state := self.hass.states.get(entity_id)) is not None
        ]
        on_members = [
            entity_id
            for entity_id in self.members
            if (state := self.hass.states.get(entity_id)) is not None
            and state.state == STATE_ON
        ]
        off_members = [
            entity_id
            for entity_id in self.members
            if (state := self.hass.states.get(entity_id)) is not None
            and state.state == STATE_OFF
        ]

        # Set group as unavailable if all members are unavailable or missing
        self._attr_available = any(state != STATE_UNAVAILABLE for state in states)

        valid_state = any(
            state not in (STATE_UNKNOWN, STATE_UNAVAILABLE) for state in states
        )
        if not valid_state:
            self._attr_is_on = None
        else:
            self._attr_is_on = any(state == STATE_ON for state in states)
            self._attr_extra_state_attributes = {
                "members": self.members,
                "members_on": on_members,
                "members_off": off_members,
            }

    async def dim_zone_absolute(
        self, brightness: int | None = None, brightness_pct: int | None = None
    ) -> None:
        """Dim zone."""
        for member in self.members:
            if brightness_pct is not None:
                await self.hass.services.async_call(
                    LIGHT_DOMAIN,
                    SERVICE_TURN_ON,
                    {"brightness_pct": brightness_pct},
                    target={"entity_id": member},
                )
            else:
                await self.hass.services.async_call(
                    LIGHT_DOMAIN,
                    SERVICE_TURN_ON,
                    {"brightness": brightness},
                    target={"entity_id": member},
                )

    async def dim_zone_relative(
        self, brightness_step: int | None = None, brightness_step_pct: int | None = None
    ) -> None:
        """Dim zone."""
        for member in self.members:
            if brightness_step_pct is not None:
                await self.hass.services.async_call(
                    LIGHT_DOMAIN,
                    SERVICE_TURN_ON,
                    {"brightness_step_pct": brightness_step_pct},
                    target={"entity_id": member},
                )
            else:
                await self.hass.services.async_call(
                    LIGHT_DOMAIN,
                    SERVICE_TURN_ON,
                    {"brightness_step": brightness_step},
                    target={"entity_id": member},
                )
