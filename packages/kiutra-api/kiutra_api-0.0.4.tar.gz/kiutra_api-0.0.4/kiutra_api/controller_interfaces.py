#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Copyright 2020 by kiutra GmbH
# All rights reserved.
# This file is part of Kiutra-API,
# and is released under the "Apache Version 2.0 License". Please see the LICENSE
# file that should have been included as part of this package.

from kiutra_api.api_client import Device


class Control(Device):
    @property
    def blocking_devices(self) -> list:
        """
        Gets list of device names blocking the use of the controller.

        """
        return self.query_value('blocking_devices')

    @property
    def name(self) -> str:
        """
        Gets device name.

        """
        return self.query_value('name')

    @property
    def is_active(self) -> bool:
        """
        Gets indicator whether controller is active.

        """
        return self.query_value('is_active')

    @property
    def successful_termination(self) -> bool:
        """
        Gets indicator whether last controller process terminated successfully.

        """
        return self.query_value('successful_termination')

    @property
    def detailed_progress(self) -> float:
        """
        Gets detailed progress of controller sequence.

        """
        return self.query_value('detailed_progress')

    @property
    def display_progress(self) -> float:
        """
        Gets display progress of sequence in %.

        """
        return self.query_value('display_progress')

    @property
    def progress(self) -> float:
        """
        Gets progress of sequence.

        """
        return self.query_value('progress')

    @property
    def is_blocked_by(self) -> str:
        """
        Gets name(s) of blocking device(s) as string.

        """
        return self.query_value('is_blocked_by')

    @property
    def is_blocked(self) -> bool:
        """
        Gets indicator whether device is blocked.

        """
        return self.query_value('is_blocked')

    @property
    def step(self) -> str:
        """
        Gets string representation of control sequence step.

        """
        return self.query_value('step')

    @property
    def check_idle_state(self) -> bool:
        """
        Gets indicator whether sequence is in idle state and ready to use.

        """
        return self.query_value('check_idle_state')

    @property
    def internal_status_name(self) -> str:
        """
        Gets string representation of internal status name.

        """
        return self.query_value('internal_status_name')

    def start(self, target: str = 'default'):
        """
        Starts control sequence.

        """
        return self.call_method('start', target)

    def stop(self):
        """
        Stops execution of current control sequence.

        """
        return self.call_method('stop')


class SetpointControl(Control):
    @property
    def ramp(self) -> float:
        """
        Gets and sets setpoint ramp.

        """
        return self.query_value('ramp')

    @ramp.setter
    def ramp(self, ramp: float):
        self.set_value('ramp', ramp)

    @property
    def setpoint(self) -> float:
        """
        Gets and sets setpoint.

        """
        return self.query_value('setpoint')

    @setpoint.setter
    def setpoint(self, setpoint: float):
        self.set_value('setpoint', setpoint)

    @property
    def stable(self) -> bool:
        """
        Gets indicator whether controller is stable.

        """
        return self.query_value('stable')

    @property
    def ramping(self) -> bool:
        """
        Gets indicator whether controller is ramping.

        """
        return self.query_value('ramping')

    @property
    def state(self) -> str:
        """
        Gets string representation of the controlling state-machine's current state.

        """
        return self.query_value('state')

    @property
    def condition(self) -> str:
        """
        Gets string representation of current controller condition.

        """
        return self.query_value('condition')

    @property
    def internal_setpoint(self) -> float:
        """
        Gets target temperature curve.

        """
        return self.query_value('internal_setpoint')

    def start(self, target: (float, float) = None, setpoint: float = None, ramp: float = None):
        """
        Starts control sequence.

        Args:
            target: legacy notation for (setpoint, ramp)
            setpoint: Final target temperature
            ramp: Measurement ramp speed

        """
        return self.call_method('start', target=target, setpoint=setpoint, ramp=ramp)


class TemperatureSetpointControl(SetpointControl):

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
    def kelvin(self) -> float:
        """Gets measured temperature of temperature control thermometer in K.

        """
        return self.query_value('kelvin')


class ADRControl(TemperatureSetpointControl):
    """ADR control object for low temperature setpoint and ramp control.

    Use client device like illustrated below:

    .. code-block:: python

        # initialize adr control client object with device object identifier and kiutra base IP
        adr_control = ADRControl('adr_control', '192.168.XX.XX')
        # read control object status
        code, message = adr_control.status
        # reset adr control object
        adr_control.reset()
        # start adr temperature control
        adr_control.start_adr(setpoint=0.5, ramp=0.1, pre_regenerate=True)
        # read current temperature
        T = adr_control.kelvin
        # update setpoint
        adr_control.setpoint = 1.0
    """

    @property
    def adr_mode(self) -> int:
        """Gets and sets integer describing the depth of adr operation (soon obsolete).

        """
        return self.query_value('adr_mode')

    @adr_mode.setter
    def adr_mode(self, adr_mode):
        self.set_value('adr_mode', adr_mode)

    @property
    def operation_mode(self) -> str:
        """Gets and sets string describing operation mode: cadr, adr, tandem (this will be obsolete soon).

        """
        return self.query_value('operation_mode')

    @operation_mode.setter
    def operation_mode(self, operation_mode):
        self.set_value('operation_mode', operation_mode)

    @property
    def charge(self) -> float:
        """Gets adr charge f(T, B) in %.

        """
        return self.query_value('charge')

    def recharge(self):
        """
        Start adr recharging.

        """
        return self.call_method('recharge')

    def start_adr(self, setpoint: float, ramp: float, adr_mode: int = None, operation_mode: str = None, auto_regenerate: bool = False, pre_regenerate: bool = False):
        """
        Starts adr temperature control.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            adr_mode: ADR depth of stage to control - default is None for normal operation.
            operation_mode: 'adr' for one shot cooling and 'cadr' for continuous cooling.
            auto_regenerate: automatically regenerates in one shot mode if adr charge is empty
            pre_regenerate: regenerates before starting temperature control

        """
        return self.call_method('start_adr', setpoint, ramp, adr_mode, operation_mode, auto_regenerate, pre_regenerate)

    def start_single_adr(self, setpoint: float, ramp: float):
        """
        Starts adr control only using the unit connected to the samplestge for seamless control.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]

        Returns:

        """
        return self.call_method('start_single_adr', setpoint=setpoint, ramp=ramp)

    def start_cadr(self, setpoint: float, ramp: float, pre_regenerate: bool=False):
        """
        Start countinuous adr operation.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            pre_regenerate: regenerates before starting temperature control (set to False by default)

        Returns:

        """
        return self.call_method('start_cadr', setpoint=setpoint, ramp=ramp, pre_regenerate=pre_regenerate)

    def start_serial_adr(self, setpoint: float, ramp: float):
        """
        Start a serial one-shot cooldown for optimized hold-time. This will recharge the adr magnets.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]

        Returns:

        """
        return self.call_method('start_serial_adr', setpoint=setpoint, ramp=ramp)


class TemperatureControl(TemperatureSetpointControl):
    """
    Continuous temperature control object for full-range temperature setpoint and ramp control.

    Use client device like illustrated below:

    .. code-block:: python

        temperature_control = TemperatureControl('temperature_control', '192.168.XX.XX')
        code, message = temperature_control.status
        temperature_control.reset()
        temperature_control.start_sequence([(0.1, 0.15, 120), (5.0, 0.2, 0)])

    """
    @property
    def adr_pid_table(self) -> list:
        """
        Gets specified adr pid table.

        """
        return self.query_value('adr_pid_table')

    @adr_pid_table.setter
    def adr_pid_table(self, table):
        self.set_value('adr_pid_table', table)

    @property
    def heater_pid_table(self) -> list:
        """
        Gets specified heater pid table.

        """
        return self.query_value('heater_pid_table')

    @heater_pid_table.setter
    def heater_pid_table(self, table):
        self.set_value('heater_pid_table', table)

    @property
    def sequential(self) -> bool:
        """
        Gets and sets bool indicating whether setpoint sequence should be used.

        """
        return self.query_value('sequential')

    @sequential.setter
    def sequential(self, sequential):
        self.set_value('sequential', sequential)

    @property
    def sections(self) -> list:
        """
        Gets and sets setpoint sequence sections as list of triples: *[(float, float, float)].*

        """
        return self.query_value('sections')

    @sections.setter
    def sections(self, sections: list):
        self.set_value('sections', sections)

    def start_sequence(self, sections: list):
        """
        Starts temperature control of setpoint sequence.

        sections:
            List of triples containing: temperature setpoint, controlled ramp and hold-time: *[(setpoint, ramp, holdtime)]/[(float, float, float)]*
        """
        return self.call_method('start_sequence', sections)

    @property
    def adr_pid(self) -> (float, float, float):
        """
        Gets adr pid values.

        """
        return self.query_value('adr_pid')

    @property
    def heater_pid(self):
        """
        Gets heater pid values.

        """
        return self.query_value('heater_pid')

    def get_ramping_info(self):
        """
        Returns dictionary containing information about any ongoing ramp or temperature control process.

        """
        return self.call_method('get_ramping_info')

    def recharge(self):
        """
        Start adr recharging.

        """
        return self.call_method('recharge')

    def cooldown(self):
        """
        Cooldown to bath temperature if temperature is above bath temperature.

        """
        return self.call_method('cooldown')

    def start_single_adr(self, setpoint: float, ramp: float, start_temperature: float = None,
                   setup_speed: float = None, init_hold: float = 0., pre_regenerate: bool = True):
        """
        Smooth single shot using only last adr-stage for seamless operation.

        Args:
            setpoint: temperature setpoint in K
            ramp: target temperature ramp in K/min
            start_temperature: start temperature in K (optional)
            setup_speed: ramp in K/min to approach start temperature if specified (optional)
            init_hold: time to wait at start temperature in s (optional)
            pre_regenerate: regenerate befor starting?

        Returns:

        """
        raise self.call_method('start_single_adr', setpoint=setpoint, ramp=ramp, start_temperature=start_temperature,
                   setup_speed=setup_speed, init_hold=init_hold, pre_regenerate=pre_regenerate)

    def start_serial_adr(self, setpoint: float, ramp: float, start_temperature: float = None,
                   pre_regenerate: bool = True, setup_speed: float = None, init_hold: float = 0.):
        raise self.call_method('start_serial_adr', setpoint=setpoint, ramp=ramp, start_temperature=start_temperature,
                   setup_speed=setup_speed, init_hold=init_hold, pre_regenerate=pre_regenerate)

    def start_cadr(self, setpoint: float, ramp: float, start_temperature: float = None,
                   pre_regenerate: bool = True, setup_speed: float = None, init_hold: float = 0.):
        """
        Start countinuous adr operation.
        """
        raise self.call_method('start_cadr', setpoint=setpoint, ramp=ramp, start_temperature=start_temperature,
                   pre_regenerate=pre_regenerate, setup_speed=setup_speed, init_hold=init_hold)

    def start_heater_control(self, setpoint: float, ramp: float, start_temperature: float = None,
                   setup_speed: float = None, init_hold: float = 0):
        """
        Heater only control aplicable above bath temperature.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            start_temperature:
            setup_speed:
            init_hold:

        Returns:

        """
        raise self.call_method('start_heater_control', setpoint=setpoint, ramp=ramp, start_temperature=start_temperature,
                   setup_speed=setup_speed, init_hold=init_hold)

    def start_control(self, **kwargs):
        """
        Generic start method. This is recommended for experienced users and targeted at automations.

        Args:
            *args:
            **kwargs:

        Returns:

        """
        raise self.call_method('start_control', **kwargs)

    def propose_control_mode(self, setpoint: float, ramp: float, mode: str = 'ramp', start_temperature: float = None):
        """
        Returns a proposed control mode based on the given parameters.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            mode: Prioritization mode (ramp/stabilize).
            start_temperature:

        Returns:

        """
        return self.call_method('propose_control_mode', setpoint=setpoint, ramp=ramp, mode=mode, start_temperature=start_temperature)

    def start_proposed_mode(self, setpoint: float, ramp: float, mode: str = 'ramp', start_temperature: float = None):
        """
        Returns the proposed control mode based on the given parameters.

        Args:
            setpoint: setpoint temperature to control [K]
            ramp: temperature ramp to control [K/min]
            mode: Prioritization mode (ramp/stabilize).
            start_temperature:

        Returns:

        """
        return self.call_method('start_proposed_mode', setpoint=setpoint, ramp=ramp, mode=mode, start_temperature=start_temperature)

    def return_to_idle(self, *args, **kwargs):
        """
        Resets or activates components of the controller to solve potential issues.

        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.call_method('return_to_idle')


class CryostatControl(Control):
    """
    A *CryostatControl* object offers the possibility to control operations concerning the entire cryostat like evacuating
    the dewar or warming up the system. It also offers access to system-wide device metrics and monitoring information.

    Use client device like illustrated below:

    .. code-block:: python

        cryostat_control = CryostatControl('cryostat', '192.168.XX.XX')
        code, message = cryostat_control.status
        cryostat_control.cooldown()

    To start a cooldown from an arbitrary RPC client, use **cryostat_control.cooldown** and the remote procedure **call**.

    .. attention::
        Some options might not be available depending on the hardware configuration.

    """

    @property
    def kelvin(self) -> float:
        """
        Gets filtered temperature of system thermometer in K.

        """
        return self.query_value('kelvin')

    @property
    def temperature_rate(self) -> float:
        """
        Gets linearized temperature change rate of system in K/min.

        """
        return self.query_value('temperature_rate')

    @property
    def pressure(self) -> float:
        """
        Gets filtered isolation vacuum pressure.

        """
        return self.query_value('pressure')

    @property
    def runstatus(self) -> bool:
        """
        Gets cryocooler run status.

        """
        return self.query_value('runstatus')

    def device_check(self):
        """
        Runs check whether all devices are ready to use.

        """
        return self.call_method('device_check')

    def restart_service(self):
        """
        Restarts kiutra software. This will stop any ongoing control process und close all monostable valves.

        """
        return self.call_method('restart_service')

    def initialize(self, **kwargs):
        """
        Initializes system components. This will e.,g., home the sample loader, set the system air-pressure and
        check/reset other critical components.

        """

    def evacuate(self, **kwargs):
        """
        Evacuates the cryostat
        """
        self.call_method("evacuate", **kwargs)

    def stop_pumps(self, **kwargs):
        """
        Stops the pumps
        """
        self.call_method("stop_pumps", **kwargs)

    def cooldown(self, **kwargs):
        """
        Cools down the cryostat
        """
        self.call_method("cooldown", **kwargs)

    def stop_cryocooler(self, **kwargs):
        """
        Stops the cold head
        """
        self.call_method("stop_cryocooler", **kwargs)

    def warmup(self, **kwargs):
        """
        Stops cold head and actively warms up system if a heater is installed
        """
        self.call_method("warmup", **kwargs)

    def stop_heater(self, **kwargs):
        """
        Stops any heating process
        """
        self.call_method("stop_heater", **kwargs)

    def purge(self, **kwargs):
        """
        Purges or vents the cryostat depending on the attached gas.
        """
        self.call_method("purge", **kwargs)

    def vent_dewar(self, **kwargs):
        """
        Vents the cryostat when system is warm but evacuated.
        """
        self.call_method("vent_dewar", **kwargs)

    def trouble_shoot(self, **kwargs):
        """
        A trouble shoot will be executed to solve communication issues.
        """
        self.call_method("trouble_shoot", **kwargs)

    def return_to_idle(self, **kwargs):
        """
        Returns to a safe state.
        """
        self.call_method("return_to_idle", **kwargs)

    def clear_magnets(self, **kwargs):
        """
        Initiates discharging of all magnets.
        """
        self.call_method("clear_magnets", **kwargs)

    def check_magnets(self, **kwargs):
        """
        Waits for magnets to be empty. Stops after timeout.
        """
        self.call_method("check_magnets", **kwargs)

    def open_gate(self, **kwargs):
        """
        Safely open the gate.
        """
        self.call_method("open_gate", **kwargs)

    def close_gate(self, **kwargs):
        """
        Safely close the gate.
        """
        self.call_method("close_gate", **kwargs)

    def open_baffles(self, **kwargs):
        """
        Safely open the baffles.
        """
        self.call_method("open_baffles", **kwargs)

    def close_baffles(self, **kwargs):
        """
        Safely close the baffles.
        """
        self.call_method("close_baffles", **kwargs)

    def start_cryocooler(self, **kwargs):
        """
        Safely switch on cryocooler and monitor cooldown.
        """
        self.call_method("start_cryocooler", **kwargs)

    def pump_airlock(self, **kwargs):
        """
        Evacuate the airlock chamber.
        """
        self.call_method("pump_airlock", **kwargs)

    def vent(self, **kwargs):
        """
        Warmup and vent system.
        """
        self.call_method("vent", **kwargs)

    def pump_suspend(self, **kwargs):
        """
        Safely stop pumps.
        """
        self.call_method("pump_suspend", **kwargs)

    def cooldown_only(self, **kwargs):
        """
        Cooldown system after it has been evacuated.
        """
        self.call_method("cooldown_only", **kwargs)

    def cooldown_block(self, **kwargs):
        """
        Safely switch on cryocooler and monitor cooldown.
        """
        self.call_method("cooldown_block", **kwargs)

    def vent_airlock(self, **kwargs):
        """
        Vent the airlock chamber.
        """
        self.call_method("vent_airlock", **kwargs)


class HeaterControl(TemperatureSetpointControl):

    """
    Temperature control object for a resistive heater.

    Use client device like illustrated below:

    .. code-block:: python

        # initialize heater control client object with device object identifier and kiutra base IP
        sample_heater = HeaterControl('sample_heater', '192.168.XX.XX')
        # read control object status
        code, message = sample_heater.status
        # reset adr control object
        sample_heater.reset()
        # start resistive temperature control
        sample_heater.start((100., 0.25)) # --> setpoint = 100 K, ramp = 0.25 K/min)

    """

    @property
    def power(self) -> float:
        """
        Returns estimated output power in W.

        """
        return self.query_value('power')

    @property
    def input(self) -> str:
        """
        Returns identifier of selected input loop

        """
        return self.query_value('input')


    @property
    def range(self) -> str:
        """
        Returns active heater range.

        """
        return self.query_value('range')

    @property
    def current(self) -> float:
        """
        Returns measured output current.

        """
        return self.query_value('current')

    @property
    def output_current(self) -> float:
        """
        Returns measured output current.

        """
        return self.query_value('output_current')

    @property
    def pid(self) -> (float, float, float):
        """
        Returns current PID parameters.

        """
        return self.query_value('pid')

    @property
    def pid_table(self) -> list:
        """
        Gets specified pid table.

        Sets new pid table.
        Format: [[T_lb, P, I, D],...]
        """
        return self.query_value('pid_table')

    @pid_table.setter
    def pid_table(self, table):
        self.set_value('pid_table', table)

    @property
    def ramp_table(self) -> bool:
        """
        Gets and sets indicator whether to use pid table.

        """
        return self.query_value('ramp_table')

    @ramp_table.setter
    def ramp_table(self, use_ramp):
        self.set_value('ramp_table', use_ramp)


class MagnetControl(SetpointControl):
    """
    Magnet control object for a super conducting sample magnet.

    Use client device like illustrated below:

    .. code-block:: python

        # initialize magnet control client object with device object identifier and kiutra base IP
        sample_magnet = MagnetControl('sample_magnet', '192.168.XX.XX')
        # read control object status
        code, message = sample_magnet.status
        # reset magnet control object
        sample_magnet.reset()
        # start magnet control
        sample_magnet.start((3., 0.25)) # --> setpoint = 3 T, ramp = 0.25 T/min

    """

    @property
    def voltage(self):
        """
        Gets voltage current in V.

        """
        return self.query_value('voltage')

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
    def current_setpoint(self):
        """
        Gets current setpoint in A.

        """
        return self.query_value('current_setpoint')

    @property
    def field(self):
        """
        Gets field in T.

        """
        return self.query_value('field')

    @property
    def field_rate(self):
        """
        Gets field rate setpoint in T/min.

        """
        return self.query_value('field_rate')

    @property
    def field_setpoint(self):
        """
        Gets field setpoint in T.

        """
        return self.query_value('field_setpoint')

    @property
    def power(self):
        """
        Gets output power in W.

        """
        return self.query_value('power')

    def on(self):
        """Switch magnet power supply(s) on

        """
        return self.call_method('on')

    def off(self):
        """Switch magnet power supply(s) off

        """
        return self.call_method('off')


class SampleControl(Control):
    """
    The sample control object offers the possibility to control operations concerning the sample transfer.

    Use client device like illustrated below:

    .. code-block:: python

        sample_loader = SampleControl('sample_loader', '192.168.XX.XX')
        code, message = sample_loader.status
        sample_loader.load_sample()
        # sample_loader.unload_sample()

    To start a sample loading process from an arbitrary RPC client, use **sample_loader.load_sample** and the remote procedure **call**.

    .. attention::
        Some options might not be available, depending on the hardware configuration.

    """

    def load_sample(self):
        """
        Starts sample loading process. This will require you to open the door at the beginning of the procedure.

        """
        self.call_method('load_sample')

    def unload_sample(self):
        """
        Starts sample unloading process.

        """
        self.call_method('unload_sample')

    def transfer_sample(self):
        """
        Starts loading process. This will require you to open the door at the beginning of the procedure. This can
        be used for both loading and unloading but might include unnecessary steps.

        """
        self.call_method('transfer_sample')

    def return_to_idle(self):
        """
        Brings the sample loader to a state from which you can safely load/unload a sample.

        """
        self.call_method('return_to_idle')

    def close_airlock(self):
        """
        Evacuates and seals the airlock.

        """
        self.call_method('close_airlock')

    def open_airlock(self):
        """
        Vents the airlock to be safely opened.

        """
        self.call_method('open_airlock')

    def pump_airlock(self):
        """
        Evacuates and seals the airlock.

        """
        self.call_method('pump_airlock')

    def vent_airlock(self):
        """
        Vents the airlock to be safely opened.

        """
        self.call_method('vent_airlock')

    def short_purge_airlock(self):
        """
        Purges the airlock for a short time to speedup warming up the sample using connected purge gas.

        """
        self.call_method('short_purge_airlock')

    def purge_airlock(self):
        """
        Purges the airlock to ambient pressure to speedup warming up the sample using connected purge gas.

        """
        self.call_method('purge_airlock')

    @property
    def sample_loaded(self) -> bool:
        """
        Gets (and sets) indicator whether a sample is loaded.

        .. attention::
            If your device does not have automatic sample detection, you can override the sample state assumed by the system.

        """
        return self.query_value('sample_loaded')

    @sample_loaded.setter
    def sample_loaded(self, sample_loaded):
        self.set_value('sample_loaded', sample_loaded)

    @property
    def door_open(self) -> bool:
        """
        Gets indicator whether the door is open.

        """
        return self.query_value('door_open')

    @property
    def rollback_necessary(self) -> bool:
        """
        Gets indicator whether a rollback is necessary (at least one device not ready).

        """
        return self.query_value('rollback_necessary')
