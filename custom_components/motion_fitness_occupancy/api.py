"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout

import re


class IntegrationBlueprintApiClientError(Exception):
    """Exception to indicate a general API error."""


class IntegrationBlueprintApiClientCommunicationError(
    IntegrationBlueprintApiClientError
):
    """Exception to indicate a communication error."""


class IntegrationBlueprintApiClientAuthenticationError(
    IntegrationBlueprintApiClientError
):
    """Exception to indicate an authentication error."""


class MotionFitnessOccupancyApiClient:
    """Sample API Client."""

    URL_FORMAT = "https://www.inchargelife.com/App/CheckInCounter.aspx?MasterID=16853&LocationID={location_id}"
    REGEX = r'<input name="txtHiddenCurrentValue" type="text" value="(\d+)" id="txtHiddenCurrentValue" style="display:none;" \/>'

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._session = session

    async def async_get_occupancy_for_location(self, location_id) -> int:
        """Fetch and parse the occupancy for a given location."""
        response = await self._api_wrapper(
            method="get",
            url=self.URL_FORMAT.format(location_id=location_id)
        )
        matched = re.search(self.REGEX, response)
        num_str = matched.group(1)
        return int(num_str) if num_str else 0

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise IntegrationBlueprintApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.text()

        except asyncio.TimeoutError as exception:
            raise IntegrationBlueprintApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise IntegrationBlueprintApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise IntegrationBlueprintApiClientError(
                "Something really wrong happened!"
            ) from exception
