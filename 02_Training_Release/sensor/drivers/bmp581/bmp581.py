# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`bmp581`
================================================================================

MicroPython Driver for the Bosch BMP581 pressure sensor


* Author: Jose D. Montoya


"""

#from micropython import const
from sensor.drivers.bmp581.i2c_helpers import CBits, RegisterStruct


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/MicroPython_BMP581.git"

_REG_WHOAMI = 0x01
_OSR_CONF = 0x36
_ODR_CONFIG = 0x37

# Power Modes
STANDBY = 0x00
NORMAL = 0x01
FORCED = 0x02
NON_STOP = 0x03
power_mode_values = (STANDBY, NORMAL, FORCED, NON_STOP)

# Oversample Rate
OSR1 = 0x00
OSR2 = 0x01
OSR4 = 0x02
OSR8 = 0x03
OSR16 = 0x04
OSR32 = 0x05
OSR64 = 0x06
OSR128 = 0x07
pressure_oversample_rate_values = (OSR1, OSR2, OSR4, OSR8, OSR16, OSR32, OSR64, OSR128)
temperature_oversample_rate_values = (
    OSR1,
    OSR2,
    OSR4,
    OSR8,
    OSR16,
    OSR32,
    OSR64,
    OSR128,
)


class BMP581:
    """Driver for the BMP581 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the BMP581 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x47`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`BMP581` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_bmp581 import bmp581

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        bmp581 = bmp581.BMP581(i2c)

    Now you have access to the attributes

    .. code-block:: python

        press = bmp.pressure

    """

    _device_id = RegisterStruct(_REG_WHOAMI, "B")

    _power_mode = CBits(2, _ODR_CONFIG, 0)
    _temperature_oversample_rate = CBits(3, _OSR_CONF, 0)
    _pressure_oversample_rate = CBits(3, _OSR_CONF, 3)
    _output_data_rate = CBits(5, _ODR_CONFIG, 2)
    _pressure_enabled = CBits(1, _OSR_CONF, 6)

    _temperature = CBits(24, 0x1D, 0, 3)
    _pressure = CBits(24, 0x20, 0, 3)

    def __init__(self, i2c, address: int = 0x47) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0x50:
            raise RuntimeError("Failed to find the BMP581 sensor")

        self._power_mode = NORMAL
        self._pressure_enabled = True
        self.sea_level_pressure = 101.325

    @property
    def power_mode(self) -> str:
        """
        Sensor power_mode

        +-----------------------------+------------------+
        | Mode                        | Value            |
        +=============================+==================+
        | :py:const:`bmp581.STANDBY`  | :py:const:`0x00` |
        +-----------------------------+------------------+
        | :py:const:`bmp581.NORMAL`   | :py:const:`0x01` |
        +-----------------------------+------------------+
        | :py:const:`bmp581.FORCED`   | :py:const:`0x02` |
        +-----------------------------+------------------+
        | :py:const:`bmp581.NON_STOP` | :py:const:`0X03` |
        +-----------------------------+------------------+
        """
        values = (
            "STANDBY",
            "NORMAL",
            "FORCED",
            "NON_STOP",
        )
        return values[self._power_mode]

    @power_mode.setter
    def power_mode(self, value: int) -> None:
        if value not in power_mode_values:
            raise ValueError("Value must be a valid power_mode setting")
        self._power_mode = value

    @property
    def pressure_oversample_rate(self) -> str:
        """
        Sensor pressure_oversample_rate
        Oversampling extends the measurement time per measurement by the oversampling
        factor. Higher oversampling factors offer decreased noise at the cost of
        higher power consumption.

        +---------------------------+------------------+
        | Mode                      | Value            |
        +===========================+==================+
        | :py:const:`bmp581.OSR1`   | :py:const:`0x00` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR2`   | :py:const:`0x01` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR4`   | :py:const:`0x02` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR8`   | :py:const:`0x03` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR16`  | :py:const:`0x04` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR32`  | :py:const:`0x05` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR64`  | :py:const:`0x06` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR128` | :py:const:`0x07` |
        +---------------------------+------------------+
        """
        values = (
            "OSR1",
            "OSR2",
            "OSR4",
            "OSR8",
            "OSR16",
            "OSR32",
            "OSR64",
            "OSR128",
        )
        return values[self._pressure_oversample_rate]

    @pressure_oversample_rate.setter
    def pressure_oversample_rate(self, value: int) -> None:
        if value not in pressure_oversample_rate_values:
            raise ValueError("Value must be a valid pressure_oversample_rate setting")
        self._pressure_oversample_rate = value

    @property
    def temperature_oversample_rate(self) -> str:
        """
        Sensor temperature_oversample_rate

        +---------------------------+------------------+
        | Mode                      | Value            |
        +===========================+==================+
        | :py:const:`bmp581.OSR1`   | :py:const:`0x00` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR2`   | :py:const:`0x01` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR4`   | :py:const:`0x02` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR8`   | :py:const:`0x03` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR16`  | :py:const:`0x04` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR32`  | :py:const:`0x05` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR64`  | :py:const:`0x06` |
        +---------------------------+------------------+
        | :py:const:`bmp581.OSR128` | :py:const:`0x07` |
        +---------------------------+------------------+
        """
        values = (
            "OSR1",
            "OSR2",
            "OSR4",
            "OSR8",
            "OSR16",
            "OSR32",
            "OSR64",
            "OSR128",
        )
        return values[self._temperature_oversample_rate]

    @temperature_oversample_rate.setter
    def temperature_oversample_rate(self, value: int) -> None:
        if value not in temperature_oversample_rate_values:
            raise ValueError(
                "Value must be a valid temperature_oversample_rate setting"
            )
        self._temperature_oversample_rate = value

    @property
    def output_data_rate(self) -> int:
        """
        Sensor output_data_rate. for a complete list of values please see the datasheet
        """
        return self._output_data_rate

    @output_data_rate.setter
    def output_data_rate(self, value: int) -> None:
        if value not in range(0, 32, 1):
            raise ValueError("Value must be a valid output_data_rate setting")
        self._output_data_rate = value

    @property
    def temperature(self) -> float:
        """
        The temperature sensor in Celsius
        :return: Temperature in Celsius
        """
        raw_temp = self._temperature
        return self._twos_comp(raw_temp, 24) / 2**16.0

    @property
    def pressure(self) -> float:
        """
        The sensor pressure in kPa
        :return: Pressure in kPa
        """
        raw_pressure = self._pressure
        return self._twos_comp(raw_pressure, 24) / 2**6.0 / 1000.0

    @property
    def altitude(self) -> float:
        """
        With the measured pressure p and the pressure at sea level p0 e.g. 1013.25hPa,
        the altitude in meters can be calculated with the international barometric formula
        """
        altitude = 44330.0 * (
            1.0 - ((self.pressure / self.sea_level_pressure) ** 0.190284)
        )
        return round(altitude, 1)

    @altitude.setter
    def altitude(self, value: float) -> None:
        self.sea_level_pressure = self.pressure / (1.0 - value / 44330.0) ** 5.255

    @staticmethod
    def _twos_comp(val: int, bits: int) -> int:
        if val & (1 << (bits - 1)) != 0:
            return val - (1 << bits)
        return val