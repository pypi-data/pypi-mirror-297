#!/usr/bin/env python3
#
# Filename: suta_ble_bed.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.03.2023
# Description: Handle BLE communications for a SUTA bed frame such as the i500 or i800.
#   Which also appears to be identical to the Sleep Motion beds.
#   BLE communication based on:
#   https://github.com/stevendodd/sleepmotion-ble/blob/main/pi-zero/sleepmotion-ble.py
#   Code structure inspired by:
#   https://github.com/sopelj/python-ember-mug/blob/main/ember_mug/mug.py
#
#   Trying to decide if your bed is compatible?
#   Connect to it with a generic BLE GATT handler, such as BLE Scanner on Android
#   If one of the services GUIDs starts with "FEE9", it likely is. Try it out!
#   It is unlikely anything harmful will happen, but I take no responsibility if
#   your bed catches on fire.
#

from __future__ import annotations

import asyncio
import contextlib

from bleak import BleakClient, BleakError, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice

from collections.abc import AsyncIterator
import typing
from typing import Any, Callable, Literal
import logging

if typing.TYPE_CHECKING:
    from .suta_ble_bed_controller import SutaBleBedController

from .suta_ble_consts import BedServices, BedCommands, BedCharacteristic

logger = logging.getLogger(__name__)

class BleSutaBed:

    def __init__(
        self,
        ble_device: BLEDevice,
        controller: SutaBleBedController,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        @param ble_device: The bleak.BLEDevice which represents the connection to the bed
        @param controller: The SutaBleBedController which controls this connection
        """
        self.device = ble_device
        self.controller: SutaBleBedController = controller

        self._client: BleakClient = None  # type: ignore[assignment]
        self._connect_lock = asyncio.Lock()
        self._operation_lock = asyncio.Lock()
        self._expected_disconnect = False

    def is_connected(self) -> bool:
        return self._client is not None and self._client.is_connected

    async def raise_feet(self) -> None:
        '''
        Raise the feet of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.FEET_UP.to_bytes(5, 'big'))

    async def lower_feet(self) -> None:
        '''
        Lower the feet of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.FEET_DOWN.to_bytes(5, 'big'))

    async def raise_head(self) -> None:
        '''
        Raise the head of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.HEAD_UP.to_bytes(5, 'big'))

    async def lower_head(self) -> None:
        '''
        Lower the head of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.HEAD_DOWN.to_bytes(5, 'big'))

    async def raise_head_and_feet(self) -> None:
        '''
        Raise the head and feet of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.HEAD_AND_FEET_UP.to_bytes(5, 'big'))

    async def lower_head_and_feet(self) -> None:
        '''
        Lower the head and feet of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.HEAD_AND_FEET_DOWN.to_bytes(5, 'big'))

    async def beep(self) -> None:
        '''
        Beep the bed.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.THREE_BEEP1.to_bytes(5, 'big'))

    async def vibrate_head(self) -> None:
        '''
        Toggle vibration on the head of the bed.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.VIBRATE_HEAD.to_bytes(5, 'big'))

    async def vibrate_feet(self) -> None:
        '''
        Toggle vibration on the feet of the bed.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.VIBRATE_FEET.to_bytes(5, 'big'))

    async def flat(self) -> None:
        '''
        Set the bed to flat.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.FLAT.to_bytes(5, 'big'))

    async def zero_gravity(self) -> None:
        '''
        Set the bed to zero gravity.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.ZERO_GRAVITY.to_bytes(5, 'big'))

    async def lounge(self) -> None:
        '''
        Set the bed to lounge.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.LOUNGE.to_bytes(5, 'big'))

    async def _write(self, service: BedServices, characteristic: BedCharacteristic, data: bytearray) -> None:
        """Helper to write characteristic."""
        if self._operation_lock.locked():
            logger.debug("Operation already in progress. Waiting for it to complete")
        async with self._operation_lock:
            await self._ensure_connection()
            try:
                await self._client.write_gatt_char(characteristic.value, data)
                logger.debug("Wrote '%s' to attribute '%s'", data, characteristic)
            except BleakError as e:
                logger.error("Failed to write '%s' to attribute '%s': %s", data, characteristic, e)
                raise

    async def _ensure_connection(self) -> None:
        """Connect to bed."""
        if self._connect_lock.locked():
            logger.debug("Connection to %s already in progress. Waiting first.", self.device.name)

        if self.is_connected():
            return

        self._client = await self.controller.connect(self)
        self._expected_disconnect = False
        return
