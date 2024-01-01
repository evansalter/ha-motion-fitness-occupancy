"""Sensor platform for motion_fitness_occupancy."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntityDescription

from .const import DOMAIN
from .entity import MotionFitnessOccupancyEntity

from datetime import timedelta

SCAN_INTERVAL = timedelta(minutes=5)

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
        name=location['name'],
        has_entity_name=True,
        icon=ICON,
    ) for location in LOCATIONS
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    async_add_devices(
        MotionFitnessOccupancyEntity(
            entity_description=entity_description,
            client=hass.data[DOMAIN][entry.entry_id]
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )
