from typing import List, Optional, Union

from tapo.responses import (
    DeviceInfoHubResult,
    KE100Result,
    S200BResult,
    T100Result,
    T110Result,
    T300Result,
    T31XResult,
)
from tapo import S200BHandler, T100Handler, T110Handler, T300Handler, T31XHandler

class HubHandler:
    """Handler for the [H100](https://www.tapo.com/en/search/?q=H100) hubs."""

    def __init__(self, handler: object):
        """Private constructor.
        It should not be called from outside the tapo library.
        """

    async def refresh_session(self) -> None:
        """Refreshes the authentication session."""

    async def get_device_info(self) -> DeviceInfoHubResult:
        """Returns *device info* as `DeviceInfoHubResult`.
        It is not guaranteed to contain all the properties returned from the Tapo API.
        If the deserialization fails, or if a property that you care about it's not present,
        try `HubHandler.get_device_info_json`.

        Returns:
            DeviceInfoHubResult: Device info of Tapo H100.
            Superset of `GenericDeviceInfoResult`.
        """

    async def get_device_info_json(self) -> dict:
        """Returns *device info* as json.
        It contains all the properties returned from the Tapo API.

        Returns:
            dict: Device info as a dictionary.
        """

    async def get_child_device_list(
        self,
    ) -> List[
        Union[KE100Result, S200BResult, T100Result, T110Result, T300Result, T31XResult, None]
    ]:
        """Returns *child device list* as `ChildDeviceHubResult`.
        It is not guaranteed to contain all the properties returned from the Tapo API
        or to support all the possible devices connected to the hub.
        If the deserialization fails, or if a property that you care about it's not present,
        try `HubHandler.get_child_device_list_json`.

        Returns:
            dict: Device info as a dictionary.
        """

    async def get_child_device_list_json(self) -> dict:
        """Returns *child device list* as json.
        It contains all the properties returned from the Tapo API.

        Returns:
            dict: Device info as a dictionary.
        """

    async def get_child_device_component_list_json(self) -> dict:
        """Returns *child device component list* as json.
        It contains all the properties returned from the Tapo API.

        Returns:
            dict: Device info as a dictionary.
        """

    async def s200b(
        self, device_id: Optional[str] = None, nickname: Optional[str] = None
    ) -> S200BHandler:
        """Returns a `S200BHandler` for the device matching the provided `device_id` or `nickname`.

        Args:
            device_id (Optional[str]): The Device ID of the device
            nickname (Optional[str]): The Nickname of the device

        Returns:
            S200BHandler: Handler for the [S200B](https://www.tapo.com/en/search/?q=S200B) devices.

        Example:
            ```python
            # Connect to the hub
            client = ApiClient("tapo-username@example.com", "tapo-password")
            hub = await client.h100("192.168.1.100")

            # Get a handler for the child device
            device = await hub.s200b(device_id="0000000000000000000000000000000000000000")

            # Get the device info of the child device
            device_info = await device.get_device_info()
            print(f"Device info: {device_info.to_dict()}")
            ```
        """

    async def t100(
        self, device_id: Optional[str] = None, nickname: Optional[str] = None
    ) -> T100Handler:
        """Returns a `T100Handler` for the device matching the provided `device_id` or `nickname`.

        Args:
            device_id (Optional[str]): The Device ID of the device
            nickname (Optional[str]): The Nickname of the device

        Returns:
            T100Handler: Handler for the [T100](https://www.tapo.com/en/search/?q=T100) devices.

        Example:
            ```python
            # Connect to the hub
            client = ApiClient("tapo-username@example.com", "tapo-password")
            hub = await client.h100("192.168.1.100")

            # Get a handler for the child device
            device = await hub.t100(device_id="0000000000000000000000000000000000000000")

            # Get the device info of the child device
            device_info = await device.get_device_info()
            print(f"Device info: {device_info.to_dict()}")
            ```
        """

    async def t110(
        self, device_id: Optional[str] = None, nickname: Optional[str] = None
    ) -> T110Handler:
        """Returns a `T110Handler` for the device matching the provided `device_id` or `nickname`.

        Args:
            device_id (Optional[str]): The Device ID of the device
            nickname (Optional[str]): The Nickname of the device

        Returns:
            T110Handler: Handler for the [T110](https://www.tapo.com/en/search/?q=T110) devices.

        Example:
            ```python
            # Connect to the hub
            client = ApiClient("tapo-username@example.com", "tapo-password")
            hub = await client.h100("192.168.1.100")

            # Get a handler for the child device
            device = await hub.t110(device_id="0000000000000000000000000000000000000000")

            # Get the device info of the child device
            device_info = await device.get_device_info()
            print(f"Device info: {device_info.to_dict()}")
            ```
        """

    async def t300(
        self, device_id: Optional[str] = None, nickname: Optional[str] = None
    ) -> T300Handler:
        """Returns a `T300Handler` for the device matching the provided `device_id` or `nickname`.

        Args:
            device_id (Optional[str]): The Device ID of the device
            nickname (Optional[str]): The Nickname of the device

        Returns:
            T300Handler: Handler for the [T300](https://www.tapo.com/en/search/?q=T300) devices.

        Example:
            ```python
            # Connect to the hub
            client = ApiClient("tapo-username@example.com", "tapo-password")
            hub = await client.h100("192.168.1.100")

            # Get a handler for the child device
            device = await hub.t300(device_id="0000000000000000000000000000000000000000")

            # Get the device info of the child device
            device_info = await device.get_device_info()
            print(f"Device info: {device_info.to_dict()}")
            ```
        """

    async def t310(
        self, device_id: Optional[str] = None, nickname: Optional[str] = None
    ) -> T31XHandler:
        """Returns a `T31XHandler` for the device matching the provided `device_id` or `nickname`.
        Args:
            device_id (Optional[str]): The Device ID of the device
            nickname (Optional[str]): The Nickname of the device

        Returns:
            T31XHandler: Handler for the [T310](https://www.tapo.com/en/search/?q=T310)
            and [T315](https://www.tapo.com/en/search/?q=T315) devices.

        Example:
            ```python
            # Connect to the hub
            client = ApiClient("tapo-username@example.com", "tapo-password")
            hub = await client.h100("192.168.1.100")

            # Get a handler for the child device
            device = await hub.t310(device_id="0000000000000000000000000000000000000000")

            # Get the device info of the child device
            device_info = await device.get_device_info()
            print(f"Device info: {device_info.to_dict()}")
            ```
        """

    async def t315(
        self, device_id: Optional[str] = None, nickname: Optional[str] = None
    ) -> T31XHandler:
        """Returns a `T31XHandler` for the device matching the provided `device_id` or `nickname`.
        Args:
            device_id (Optional[str]): The Device ID of the device
            nickname (Optional[str]): The Nickname of the device

        Returns:
            T31XHandler: Handler for the [T310](https://www.tapo.com/en/search/?q=T310)
            and [T315](https://www.tapo.com/en/search/?q=T315) devices.

        Example:
            ```python
            # Connect to the hub
            client = ApiClient("tapo-username@example.com", "tapo-password")
            hub = await client.h100("192.168.1.100")

            # Get a handler for the child device
            device = await hub.t315(device_id="0000000000000000000000000000000000000000")

            # Get the device info of the child device
            device_info = await device.get_device_info()
            print(f"Device info: {device_info.to_dict()}")
            ```
        """
