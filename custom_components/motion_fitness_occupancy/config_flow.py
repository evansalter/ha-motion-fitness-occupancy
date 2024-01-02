"""Adds config flow for Blueprint."""
from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN, NAME


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        # entries = self.hass.config_entries.async_entries()
        current_entries = self.hass.config_entries.async_entries(self.handler)
        if current_entries:
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(
            title=NAME,
            data={},
        )
