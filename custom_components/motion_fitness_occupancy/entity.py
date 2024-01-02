"""BlueprintEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import ATTRIBUTION, DOMAIN
from .api import MotionFitnessOccupancyApiClient


class MotionFitnessOccupancyEntity(SensorEntity):
    """BlueprintEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        entity_description: SensorEntityDescription,
        client: MotionFitnessOccupancyApiClient,
        location_name: str,
    ) -> None:
        """Initialize."""
        super().__init__()
        self.entity_description = entity_description
        self._attr_unique_id = self.entity_description.key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=f"Motion Fitness {location_name}",
        )
        self.client = client

    async def async_update(self) -> None:
        """Update the entity with the latest occupancy count."""
        location_id = self.unique_id.split('_')[-1]
        result = await self.client.async_get_occupancy_for_location(location_id)
        self._attr_native_value = result
