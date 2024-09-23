#!/usr/bin/env python3
#
# Filename: cli.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.03.2023
# Description: Scuffed CLI to control your bed. Mostly for testing.
#

import asyncio
import argparse
from argparse import Namespace
import logging

from .suta_ble_bed import BleSutaBed
from .suta_ble_bed_controller import SutaBleBedController
from .suta_ble_consts import BedCommands

logger = logging.getLogger(__name__)

async def worker(args: Namespace):

    async with SutaBleBedController() as controller:
        async for bed in controller.devices():
            logger.info(f"Discovered {bed.device}")

            if (args.MAC is None or bed.device.address == args.MAC):
                match args.command:
                    case "feet-up":
                        await bed.raise_feet()
                    case "feet-down":
                        await bed.lower_feet()
                    case "head-up":
                        await bed.raise_head()
                    case "head-down":
                        await bed.lower_head()
                    case "vibrate-head":
                        await bed.vibrate_head()
                    case "vibrate-feet":
                        await bed.vibrate_feet()
                    case "zero-gravity":
                        await bed.zero_gravity()
                    case "flat":
                        await bed.flat()
                    case "lounge":
                        await bed.lounge()
                break
            else:
                logger.info(f"Skipping because MAC did not match.")

def main():
    parser = argparse.ArgumentParser(
        prog="SUTA BLE Control",
        description="Control your Bluetooth-enabled SUTA (and other) bed.")

    parser.add_argument(
        "--MAC",
        required=False,
        help="MAC Address of your bed. May be ommitted, in which case we will attempt auto-discovery.")
    
    parser.add_argument(
        "command",
        choices=[command.name.lower().replace("_", "-") for command in BedCommands],
        help="Action to perform")
    
    args = parser.parse_args()
    
    asyncio.run(worker(args))

if __name__ == "__main__":
    main()