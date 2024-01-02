"""Sensor platform for motion_fitness_occupancy."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass

from .const import DOMAIN
from .entity import MotionFitnessOccupancyEntity

from datetime import timedelta

SCAN_INTERVAL = timedelta(minutes=10)

ICON = "mdi:account"

LOCATIONS = [
    { 'location_id': 3457, 'name': 'Brighton' },
    { 'location_id': 3460, 'name': 'Lawson Heights' },
    { 'location_id': 3458, 'name': 'Stonebridge' },
    { 'location_id': 3459, 'name': 'Blairmore' },
]

def _get_location_description_pairs():
    return ((location, SensorEntityDescription(
        key=f"motion_fitness_occupancy_{location['location_id']}",
        name='Current Occupancy',
        has_entity_name=True,
        icon=ICON,
        native_unit_of_measurement='people',
        state_class=SensorStateClass.MEASUREMENT,
    )) for location in LOCATIONS)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    devices = [MotionFitnessOccupancyEntity(
        entity_description=entity_description,
        client=hass.data[DOMAIN][entry.entry_id],
        location_name=location['name'],
    ) for (location, entity_description) in _get_location_description_pairs()]

    async_add_devices(devices, update_before_add=True)
