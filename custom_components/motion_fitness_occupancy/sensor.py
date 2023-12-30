"""Sensor platform for motion_fitness_occupancy."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN
from .coordinator import MotionFitnessOccupancyDataUpdateCoordinator
from .entity import MotionFitnessOccurpancyEntity

ICON = "mdi:account"

LOCATIONS = [
    { 'location_id': 3457, 'name': 'Brighton' },
    { 'location_id': 3460, 'name': 'Lawson Heights' },
    { 'location_id': 3458, 'name': 'Stonebridge' },
    { 'location_id': 3459, 'name': 'Blairmore' },
]

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key=f"motion_fitness_occupancy_{location['location_id']}",
        name=f"{location['name']} Motion Fitness Occupancy",
        icon=ICON,
    ) for location in LOCATIONS
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        IntegrationBlueprintSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IntegrationBlueprintSensor(MotionFitnessOccurpancyEntity, SensorEntity):
    """motion_fitness_occupancy Sensor class."""

    def __init__(
        self,
        coordinator: MotionFitnessOccupancyDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.coordinator.data
