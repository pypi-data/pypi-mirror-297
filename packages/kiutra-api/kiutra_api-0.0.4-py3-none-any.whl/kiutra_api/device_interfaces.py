#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Copyright 2020 by kiutra GmbH
# All rights reserved.
# This file is part of Kiutra-API,
# and is released under the "Apache Version 2.0 License". Please see the LICENSE
# file that should have been included as part of this package.

from kiutra_api.api_client import Device


class Thermometer(Device):

    def get_stable(self, max_error=None, setpoint=None) -> list:
        """
        Returns list of indicators for alle values within "stabilitywindow". If a value meets the stability criterion,
        the respective entry is True, else False. A value becomes True if delta_T/T < max_error
        where delta_T = abs(T-setpoint)

        Args:
            max_error: Maximum relative temperature error.
            setpoint: Setpoint value to compare to.

        Returns:
            List of boolean indicators whether an entry reaches the stability criterion.

        """
        return self.call_method('get_stable', max_error, setpoint)

    def get_settled(self, max_error=None, setpoint=None) -> bool:
        """
        Returns whether temperature is settled with respect to setpoint. Settled requires all relative errors
        delta_T/T in "stabilitywindow" to be within an epsilon of +-max_error.

        Args:
            max_error: Maximum relative temperature error.
            setpoint: Setpoint value to compare to.

        Returns:
            Indicator whether temperature is settled.
        """
        return self.call_method('get_settled', max_error, setpoint)

    def get_settling(self, max_error=None, setpoint=None) -> bool:
        """
        Returns whether temperature is settling with respect to setpoint. Settling requires at least one relative error
        delta_T/T in "stabilitywindow" to be within an epsilon of +-max_error.

        Args:
            max_error: Maximum relative temperature error.
            setpoint: Setpoint value to compare to.

        Returns:
            Indicator whether temperature is settling.
        """
        return self.call_method('get_settling', max_error, setpoint)

    @property
    def max_error(self) -> float:
        """
        Reads allowed maximum relative error of thermometer: abs(setpoint-temperature)/temperature < max_error.
        """
        return self.query_value('max_error')

    @max_error.setter
    def max_error(self, max_error: float):
        """
        Sets allowed maximum relative error of thermometer: abs(setpoint-temperature)/temperature < max_error..
        """
        self.set_value('max_error', max_error)

    @property
    def is_stable(self):
        return self.query_value('is_stable')

    @property
    def is_settling(self):
        return self.query_value('is_settling')

    @property
    def kelvin(self) -> float:
        """
        Reads the thermometer's temperature in K.
        """
        return self.query_value('kelvin')

    @property
    def kelvin_rate(self) -> float:
        """
        Reads the thermometer's estimated linear temperature rate in K/s over "transientwindow".
        """
        return self.query_value('kelvin_rate')


    @property
    def kelvin_median(self) -> float:
        """
        Reads the thermometer's temperature median in "transientwindow".
        """
        return self.query_value('kelvin_median')

    @property
    def kelvin_buffer(self) -> list:
        """
        Reads the thermometer's buffered temperatures.
        """
        return self.query_value('kelvin_buffer')

    @property
    def kelvin_stablebuffer(self) -> list:
        """
        Reads the thermometer's buffered temperatures in "stabilitywindow.
        """
        return self.query_value('kelvin_stablebuffer')

    @property
    def kelvin_transientbuffer(self) -> list:
        """
        Reads the thermometer's buffered temperatures in "transientwindow.
        """
        return self.query_value('kelvin_transientbuffer')

    @property
    def kelvin_timestamp(self) -> float:
        """
        Reads tuple of thermometer's temperature in K and time in sec. (temperature, timestamp).
        """
        return self.query_value('kelvin_timestamp')

    @property
    def kelvin_transientwindow(self) -> float:
        """
        Reads length of temperature transientwindow in sec.
        """
        return self.query_value('kelvin_transientwindow')

    @kelvin_transientwindow.setter
    def kelvin_transientwindow(self, window: int):
        """
        Overrides length of temperature transientwindow in sec.
        """
        self.set_value('kelvin_transientwindow', window)

    @property
    def kelvin_stabilitywindow(self) -> float:
        """
        Reads length of temperature stabilitywindow in sec.
        """
        return self.query_value('kelvin_stabilitywindow')

    @kelvin_stabilitywindow.setter
    def kelvin_stabilitywindow(self, window: int):
        """
        Overrides length of temperature stabilitywindow in sec.
        """
        self.set_value('kelvin_stabilitywindow', window)

    @property
    def sensorunits(self) -> float:
        """
        Reads the thermometer's temperature in sensor units (normally Ohm).
        """
        return self.query_value('sensorunits')


    @property
    def sensorunits_rate(self) -> float:
        """
        Reads the thermometer's estimated linear sensorunits rate over "transientwindow".
        """
        return self.query_value('sensorunits_rate')


    @property
    def sensorunits_median(self) -> float:
        """
        Reads the thermometer's sensorunits median in "transientwindow".
        """
        return self.query_value('sensorunits_median')

    @property
    def sensorunits_buffer(self) -> list:
        """
        Reads the thermometer's buffered sensorunits.
        """
        return self.query_value('sensorunits_buffer')

    @property
    def sensorunits_stablebuffer(self) -> list:
        """
        Reads the thermometer's buffered sensorunits in "stabilitywindow.
        """
        return self.query_value('sensorunits_stablebuffer')

    @property
    def sensorunits_transientbuffer(self) -> list:
        """
        Reads the thermometer's buffered sensorunits in "transientwindow.
        """
        return self.query_value('sensorunits_transientbuffer')

    @property
    def sensorunits_timestamp(self) -> float:
        """
        Reads tuple of thermometer's sensorunits and time in sec. (sensorunits, timestamp).
        """
        return self.query_value('sensorunits_timestamp')

    @property
    def sensorunits_transientwindow(self) -> float:
        """
        Reads length of sensorunits transientwindow in sec.
        """
        return self.query_value('sensorunits_transientwindow')

    @property
    def sensorunits_stabilitywindow(self) -> float:
        """
        Reads length of sensorunits stabilitywindow in sec.
        """
        return self.query_value('sensorunits_stabilitywindow')

    def get_buffer_after(self, key, t_after=0) -> list:
        """
        Returns buffer after t_after (unix timestamp als number).
        Args:
            key: Property name like 'kelvin' or 'sensorunit'
            t_after: timstamp after which buffered values will be returned

        Returns: buffered values as 2D matrix.

        """
        return self.call_method('get_buffer_after', key, t_after)

    @property
    def excitation(self) -> float:
        """
        Reads the thermometer's excitation in V.
        """
        return self.query_value('excitation')


class Magnet(Device):
    @property
    def current(self) -> float:
        """
        Reads power supply current.
        """
        return self.query_value('current')

    @property
    def current_rate(self) -> float:
        """
        Reads the magnet's estimated linear current rate over "transientwindow".
        """
        return self.query_value('current_rate')

    @property
    def current_median(self) -> float:
        """
        Reads the magnet's current median in "transientwindow".
        """
        return self.query_value('current_median')

    @property
    def current_buffer(self) -> list:
        """
        Reads the magnet's buffered current.
        """
        return self.query_value('current_buffer')

    @property
    def current_stablebuffer(self) -> list:
        """
        Reads the magnet's buffered current in "stabilitywindow.
        """
        return self.query_value('current_stablebuffer')

    @property
    def current_transientbuffer(self) -> list:
        """
        Reads the magnet's buffered current in "transientwindow.
        """
        return self.query_value('current_transientbuffer')

    @property
    def current_timestamp(self) -> float:
        """
        Reads tuple of magnet's current and time in sec. (current, timestamp).
        """
        return self.query_value('current_timestamp')

    @property
    def current_transientwindow(self) -> float:
        """
        Reads length of current transientwindow in sec.
        """
        return self.query_value('current_transientwindow')

    @property
    def current_stabilitywindow(self) -> float:
        """
        Reads length of current stabilitywindow in sec.
        """
        return self.query_value('current_stabilitywindow')

    def get_buffer_after(self, key, t_after=0) -> list:
        """
        Returns buffer after t_after (unix timestamp als number).
        Args:
            key: Property name like 'kelvin' or 'sensorunit'
            t_after: timstamp after which buffered values will be returned

        Returns: buffered values as 2D matrix.

        """
        return self.call_method('get_buffer_after', key, t_after)

    @property
    def tesla(self) -> float:
        """
        Reads power supply tesla.
        """
        return self.query_value('tesla')

    @property
    def tesla_rate(self) -> float:
        """
        Reads the magnet's estimated linear tesla rate over "transientwindow".
        """
        return self.query_value('tesla_rate')

    @property
    def tesla_median(self) -> float:
        """
        Reads the magnet's tesla median in "transientwindow".
        """
        return self.query_value('tesla_median')

    @property
    def tesla_buffer(self) -> list:
        """
        Reads the magnet's buffered tesla.
        """
        return self.query_value('tesla_buffer')

    @property
    def tesla_stablebuffer(self) -> list:
        """
        Reads the magnet's buffered tesla in "stabilitywindow.
        """
        return self.query_value('tesla_stablebuffer')

    @property
    def tesla_transientbuffer(self) -> list:
        """
        Reads the magnet's buffered tesla in "transientwindow.
        """
        return self.query_value('tesla_transientbuffer')

    @property
    def tesla_timestamp(self) -> float:
        """
        Reads tuple of magnet's tesla and time in sec. (tesla, timestamp).
        """
        return self.query_value('tesla_timestamp')

    @property
    def tesla_transientwindow(self) -> float:
        """
        Reads length of tesla transientwindow in sec.
        """
        return self.query_value('tesla_transientwindow')

    @property
    def tesla_stabilitywindow(self) -> float:
        """
        Reads length of tesla stabilitywindow in sec.
        """
        return self.query_value('tesla_stabilitywindow')

    @property
    def voltage(self) -> float:
        """
        Reads power supply voltage.
        """
        return self.query_value('voltage')

    @property
    def voltage_rate(self) -> float:
        """
        Reads power supply voltage rate.
        """
        return self.query_value('voltage_rate')

    @property
    def field(self) -> float:
        """
        Reads power supply field.
        """
        return self.query_value('field')

    @property
    def field_rate(self) -> float:
        """
        Reads power supply field.
        """
        return self.query_value('field_rate')


class WarmupHeater(Device):
    @property
    def kelvin(self) -> float:
        """
        Reads the control thermometer's temperature in K.
        """
        return self.query_value('kelvin')

    @property
    def power(self) -> float:
        """
        Reads the heater's power consumption in W.
        """
        return self.query_value('power')

    @property
    def setpoint(self) -> float:
        """
        Reads the heater's temperature setpoint in K.
        """
        return self.query_value('setpoint')

    @property
    def rate(self) -> float:
        """
        Reads the heater's temperature ramp rate in K/min.
        """
        return self.query_value('rate')

    @property
    def range(self) -> float:
        """
        Reads the selected heater range.
        """
        return self.query_value('range')

    @property
    def input(self) -> float:
        """
        Reads the selected input channel.
        """
        return self.query_value('input')

    @property
    def current(self) -> float:
        """
        Reads the heater's output current in A.
        """
        return self.query_value('current')

    @property
    def voltage(self) -> float:
        """
        Reads the heater's output voltage in V.
        """
        return self.query_value('voltage')

    def stop(self):
        """
        Stops current heating process.
        """
        return self.call_method('stop')

    def off(self):
        """
        Switches heating loop to mode off.
        """
        return self.call_method('off')


class Heatswitch(Device):
    @property
    def is_open(self) -> bool:
        """
        Indicates whether the heat switch is open.
        """
        return self.query_value('is_open')

    @property
    def is_closed(self) -> bool:
        """
        Indicates whether the heat switch is closed.
        """
        return self.query_value('is_closed')

    @property
    def setpoint(self) -> str:
        """
        Reads and sets the heat switch's target setpoint.
        """
        return self.query_value('setpoint')

    @setpoint.setter
    def setpoint(self, setpoint: str):
        self.set_value('setpoint', setpoint)

    @property
    def position(self) -> float:
        """
        Reads the heat switch position (0-100%).
        """
        return self.query_value('position')

    def open(self):
        """
        Open heat switch.
        """
        return self.call_method('open')

    def closed(self):
        """
        Close heat switch.
        """
        return self.call_method('closed')


class Valve(Device):
    @property
    def is_open(self) -> bool:
        """
        Indicates whether the valve is open.
        """
        return self.query_value('is_open')

    @property
    def position(self) -> str:
        """
        Returns a string representation of the valve's position.
        """
        return self.query_value('position')

    @property
    def is_closed(self) -> bool:
        """
        Indicates whether the valve is closed.
        """
        return self.query_value('is_closed')

    def closed(self):
        """
        Close valve.

        .. note::
            Admin-level access required.

        """
        return self.call_method('closed')


class TurboPump(Device):
    @property
    def voltage(self) -> float:
        """
        Pump's motor voltage draw in V.
        """
        return self.query_value('voltage')

    @property
    def current(self) -> float:
        """
        Pump's motor current draw in A.
        """
        return self.query_value('current')

    @property
    def temperature(self) -> float:
        """
        Pump's motor temperature in °C.
        """
        return self.query_value('temperature')

    @property
    def power(self) -> float:
        """
        Pump's motor power consumption in W.
        """
        return self.query_value('power')

    @property
    def frequency(self) -> float:
        """
        Pump's current rotor frequency in Hz.
        """
        return self.query_value('frequency')

    @property
    def operation_counter(self) -> int:
        """
        Number of starts.
        """
        return self.query_value('operation_counter')

    @property
    def operation_hours(self) -> float:
        """
        Total operation hours.
        """
        return self.query_value('operation_hours')

    @property
    def is_on(self) -> bool:
        """
        Indicates whether the pump is drawing power.
        """
        return self.query_value('is_on')

    @property
    def is_rotating(self) -> bool:
        """
        Indicates whether the pump's rotor is spinning.
        """
        return self.query_value('is_rotating')

    @property
    def is_off(self) -> bool:
        """
        Indicates whether the pump is switched off.
        """
        return self.query_value('is_off')

    def stop(self):
        """
        Stop turbo pump.

        .. note::
            Admin-level access required.

        """
        return self.call_method('stop')


class ForePump(Device):
    @property
    def is_on(self) -> bool:
        """
        Indicates whether the pump is drawing power.
        """
        return self.query_value('is_on')

    @property
    def is_off(self) -> bool:
        """
        Indicates whether the pump is switched off.
        """
        return self.query_value('is_off')

    def stop(self):
        """
        Stop fore pump.

        .. note::
            Admin-level access required.

        """
        return self.call_method('stop')

    def start(self):
        """
        Start Fore pump.

        .. note::
            Admin-level access required.

        """
        return self.call_method('start')

    def off(self):
        """
        Switches the pump to off.

        .. note::
            Admin-level access required.

        """
        return self.call_method('off')

    def on(self):
        """
        Switches the pump to on.

        .. note::
            Admin-level access required.

        """
        return self.call_method('on')


class Gauge(Device):
    @property
    def pressure(self):
        """
        Reads current pressure in mbar/bar.
        """
        return self.query_value('pressure')

    @property
    def voltage(self):
        """
        Reads raw sensor voltage.
        """
        return self.query_value('voltage')


class Compressor(Device):

    @property
    def runstatus(self):
        """
        Indicates whether the compressor is running.
        """
        return self.query_value('runstatus')

    @property
    def gasflow_error(self) -> bool:
        """
        Indicates a motor gas flow error.
        """
        return self.query_value('gasflow_error')

    @property
    def gastemp_error(self) -> bool:
        """
        Indicates a motor gas temperature error.
        """
        return self.query_value('gastemp_error')

    @property
    def waterflow_error(self) -> bool:
        """
        Indicates a motor water flow error.
        """
        return self.query_value('waterflow_error')

    @property
    def watertemp_error(self) -> bool:
        """
        Indicates a motor water temperature error.
        """
        return self.query_value('watertemp_error')

    @property
    def motortemp_error(self) -> bool:
        """
        Indicates a motor temperature error.
        """
        return self.query_value('motortemp_error')

    @property
    def power_error(self) -> bool:
        """
        Indicates a power temperature error.
        """
        return self.query_value('power_error')

    @property
    def return_pressure(self) -> float:
        """
        Reads the compressor return pressure in bar.
        """
        return self.query_value('return_pressure')

    @property
    def operating_hours(self) -> float:
        """
        Reads and sets operating hours as stored on the compressor control unit (CCU).
        """
        return self.query_value('operating_hours')

    @operating_hours.setter
    def operating_hours(self, hours: float):
        self.set_value('operating_hours', hours)

    @property
    def voltage(self) -> float:
        """
        Reads the raw compressor return pressure voltage.
        """
        return self.query_value('voltage')

    def off(self):
        """
        Switches the compressor off.
        """
        return self.call_method('off')

    def on(self):
        """
        Switches the compressor on.
        """
        return self.call_method('on')


class Baffles(Device):
    @property
    def is_open(self) -> bool:
        """
        Indicates whether the baffles are open.
        """
        return self.query_value('is_open')

    @property
    def is_closed(self) -> bool:
        """
        Indicates whether the baffles are closed.
        """
        return self.query_value('is_closed')

    @property
    def setpoint(self) -> str:
        """
        Reads and sets the baffles' target setpoint.

        .. note::
            Admin-level access required.
        """
        return self.query_value('setpoint')

    @setpoint.setter
    def setpoint(self, setpoint: str):
        self.set_value('setpoint', setpoint)

    @property
    def position(self) -> float:
        """
        Reads the heat baffles position (0-100%).
        """
        return self.query_value('position')

    def stop(self):
        """
        Stops baffles.
        """
        return self.call_method('stop')


class Winch(Device):

    @property
    def bellows_is_up(self) -> bool:
        """
        Indicates whether the the bellows is up.
        """
        return self.query_value('bellows_is_up')

    @property
    def bellows_is_down(self) -> bool:
        """
        Indicates whether the the bellows is down.
        """
        return self.query_value('bellows_is_down')

    @property
    def door_is_closed(self) -> bool:
        """
        Indicates whether the airlock door is closed.
        """
        return self.query_value('door_is_closed')

    @property
    def door_is_open(self) -> bool:
        """
        Indicates whether the airlock door is open.
        """
        return self.query_value('door_is_open')

    @property
    def raw_position(self) -> float:
        """
        Reads the motor's raw position.
        """
        return self.query_value('raw_position')

    @property
    def position(self) -> float:
        """
        Reads the motor position (0-100%)
        """
        return self.query_value('position')

    @property
    def setpoint(self) -> str:
        """
        Reads the motor's setpoint (up/down).
        """
        return self.query_value('setpoint')

    def stop(self):
        """
        Stops the motor immediately.
        """
        return self.call_method('stop')

    def home(self):
        """
        Homes the motor position.

        .. note::
            Admin-level access required.

        """
        return self.call_method('home')


class PressureRegulator(Device):
    @property
    def pressure(self):
        """
        Reads current pressure in mbar/bar.
        """
        return self.query_value('pressure')

    @pressure.setter
    def pressure(self, pressure):
        self.set_value('pressure', pressure)

    @property
    def pressure_setpoint(self):
        """
        Reads current pressure setpoint in mbar/bar.
        """
        return self.query_value('pressure_setpoint')

    @property
    def voltage(self):
        """
        Reads raw sensor voltage.
        """
        return self.query_value('voltage')