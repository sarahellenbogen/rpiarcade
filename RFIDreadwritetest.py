# SPDX-FileCopyrightText: <text> 2015 Tony DiCola, Roberto Laricchia,
# and Francesco Crisafulli, for Adafruit Industries </text>

# SPDX-License-Identifier: MIT

# Example of detecting and reading a block from a MiFare classic NFC card.

"""
This example shows connecting to the PN532 and writing & reading a mifare classic
type RFID tag
"""

import board
import busio

# Additional import needed for I2C/SPI
from digitalio import DigitalInOut
#
# NOTE: pick the import that matches the interface being used
#
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
#from adafruit_pn532.i2c import PN532_I2C

from adafruit_pn532.spi import PN532_SPI
# from adafruit_pn532.uart import PN532_UART



# SPI connection:
spi = busio.SPI(board.SCK_1, MOSI = board.MOSI_1, MISO =  board.MISO_1)
cs_pin = DigitalInOut(board.D16)
pn532 = PN532_SPI(spi, cs_pin, debug=False)


# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to write to!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

uid = None
while uid is None:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=2)

# print("Found card with UID:", [hex(i) for i in uid])

authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
if not authenticated:
    print("Authentication failed!")

value = 0
data = value.to_bytes(16, 'big')
pn532.mifare_classic_write_block(4, data)

array = int.from_bytes(pn532.mifare_classic_read_block(4), "big")
print("read data:" + hex(array))
