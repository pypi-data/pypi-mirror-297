#!/usr/bin/env python3
#
# Filename: suta_ble_bed_controller.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.22.2023
# Description: Object which handles discovery and connection to SUTA-compatible devices
#

import asyncio
from bleak import BleakClient, BleakError, BleakScanner
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection
from contextlib import AbstractAsyncContextManager

import logging
from types import TracebackType

from .suta_ble_bed import BleSutaBed
from .suta_ble_scanner import SutaBleScanner
from .suta_ble_consts import BED_LOCAL_NAME

logger = logging.getLogger(__name__)

class SutaBleBedController(AbstractAsyncContextManager):

    def __init__(self, adapter: str = None) -> None:
        """
        Constructor

        @param adapter: The Bluetooth adapter to use, like "hci0"
        """
        super().__init__()

        self._bed_scanner = SutaBleScanner(self)
        self._bleak_scanner = BleakScanner(
            detection_callback=self._bed_scanner._scanner_discovery_callback,
            adapter=adapter)
        self._scanner_running: bool = False

    async def __aenter__(self):
        await self._bleak_scanner.start()
        self._scanner_running = True
        return self
    
    async def __aexit__(self, __exc_type: type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None) -> bool | None:
        self._scanner_running = False
        await self._bleak_scanner.stop()
        return await super().__aexit__(__exc_type, __exc_value, __traceback)
    
    def devices(self):
        return self._bed_scanner

    def _disconnect_callback(self, device: BleSutaBed, client: BleakClient) -> None:
        """Disconnected from device."""
        if device._expected_disconnect:
            logger.debug("Disconnect callback called")
        else:
            logger.warning("Unexpectedly disconnected")

    async def connect(self, bed: BleSutaBed) -> BleakClient:
        """
        Establish a connection to the device, which should be one controlled by this controller.

        @param device: The BleSutaBed device to which we should attach
        """
        if not self._scanner_running:
            raise "Cannot attempt to connect to a device while the scanner is not running"

        async with bed._connect_lock:
            # Check if the device is already connected
            if bed.is_connected():
                return
            try:
                logger.debug(f"Connecting to {bed.device}")
                client = await establish_connection(
                    client_class=BleakClient,
                    device=bed.device,
                    name=f'{bed.device.name} ({bed.device.address})',
                    use_services_cache=True,
                    disconnected_callback=lambda client: self._disconnect_callback(bed, client),  # type: ignore
                    ble_device_callback=lambda: bed.device,
                )
                return client
            except (asyncio.TimeoutError, BleakError) as error:
                logger.error("%s: Failed to connect to the bed: %s", bed.device, error)
                raise
