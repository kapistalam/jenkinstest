"""Support for Function generator devices"""

import logging
import time
import verboselogs
import math

from sytpy.devices.ESA.FSUP50 import FSUP50
from sytpy.devices.ESA.N9030A import N9030A

class ESA():
    """
    Class driver for Electrical Spectrum Analyzer.
    """

    def __init__(self, resource_name, **kwargs):
        """
        Minimal user example with sytpy.testbed::

            import sytpy.testbed.testbed as testbed

            # Connect to all devices in default device group
            # Assumption: device label TX_ESA used for our device
            TB = testbed.TB()

            # configure all devices to defaults
            TB.InitTB()

            # Write frequency
            TB.devices["TX_ESA"].frequency = 100

        Minimal user example outside of sytpy.testbed::

            import sytpy

            # connect to device
            ESA = sytpy.devices.ESA("GPIB0::16::INSTR", params["devicedriver"]="FSUP50", label="ESA")

            # get a defined state of my device
            ESA.reset()
            ESA.InitDevice()

            # Get frequency
            ESA.get_start_frequency()

        DeviceCfg.xml example for Electrical Spectrum Analyzer (ESA):

        .. code-block:: xml

            <ifvise address="GPIB0::18::INSTR" access="0" timeout="0">
                <device lable="ESA" class="ESA" devicedriver="HP8565E" driverversion="02.00" comment=""/>
            </ifvise>

        :param str resource_name: IP/GPIB or com address
        :param kwargs: see :ref:`General Device <dev_guide_general_device>` for details of possible values

        :raises NotImplementedError: for not supported device drivers
        :raises ImportError: when device could not be created
        """

        # add logger instance to module
        verboselogs.install()
        self.logger = logging.getLogger(__name__)
        self.logger.spam('FW class init called ')

        self.params = kwargs

        # prepare variable to store last measurements used in get_status
        # all values should be initialized to -99
        self.last_measurement = {}

        # instance the python driver for the specified device driver
        # when the device needs specific parameters from kwargs then
        # ensure that a check is done here or in the driver itself
        try:
            if self.params["devicedriver"] == 'FSUP50':

                # store device object at variable self.devh (device handle)
                # all devices have to use the same variable name
                self.devh = FSUP50(resource_name, **kwargs)
                self.logger.verbose("%-20s: Device information %s %s, serial=%s, FW=%s", self.params["label"],
                                    self.devh.vendor, self.devh.model, self.devh.serial, self.devh.fw)

            elif self.params["devicedriver"] == 'N9030A':
                self.devh = N9030A(resource_name, **kwargs)
                self.logger.verbose("%-20s: Device information %s %s, serial=%s, FW=%s", self.params["label"],
                                    self.devh.vendor, self.devh.model, self.devh.serial, self.devh.fw)

            else:
                raise NotImplementedError("the devicetype %s is not implemented", self.params["devicedriver"])
        except:
            self.logger.exception("Could not import module %s" % self.params["devicedriver"])
            raise Exception("ImportError")

    def reset(self):
        """
        Reset the device and sets it to the manufacturer default settings.
        """
        self.devh.rst()

    def wait_to_complete(self):
        """
        wait for the commands to complete.
        """
        self.devh.wait_busy()

    def InitDevice(self):
        """
        Initializes the device to some reasonable save default settings.

        A Electrical spectrum analyzer will be initialized to following settings:

            * start_frequency = 10Hz
        """
        self.devh.set_start_frequency(10)

    def get_rawdata_from_spectrum(self, pathname, filename):
        return self.devh.get_rawdata_from_spectrum(pathname, filename)

    def set_start_frequency(self, freq):
        self.devh.set_start_frequency(freq)
    set_start_frequency.__doc__ = FSUP50.set_start_frequency.__doc__

    def get_start_frequency(self):
        return self.devh.get_start_frequency()
    get_start_frequency.__doc__ = FSUP50.get_start_frequency.__doc__

    def set_stop_frequency(self, freq):
        self.devh.set_stop_frequency(freq)
    set_stop_frequency.__doc__ = FSUP50.set_stop_frequency.__doc__

    def get_stop_frequency(self):
        return self.devh.get_stop_frequency()
    get_stop_frequency.__doc__ = FSUP50.get_stop_frequency.__doc__

    def set_video_bw(self, bw):
        self.devh.set_video_bw(bw)
    set_video_bw.__doc__ = FSUP50.set_video_bw.__doc__

    def get_video_bw(self):
        return self.devh.get_video_bw()
    get_video_bw.__doc__ = FSUP50.get_video_bw.__doc__

    def set_resolution_bw(self, resolution_bw):
        self.devh.set_resolution_bw(resolution_bw)
    set_resolution_bw.__doc__ = FSUP50.set_resolution_bw.__doc__

    def get_resolution_bw(self):
        return self.devh.get_resolution_bw
    get_resolution_bw.__doc__ = FSUP50.get_resolution_bw.__doc__

    def set_center_frequency(self, freq):
        self.devh.set_center_frequency(freq)
    set_center_frequency.__doc__ = FSUP50.set_center_frequency.__doc__

    def get_center_frequency(self):
        return self.devh.get_center_frequency()
    get_center_frequency.__doc__ = N9030A.get_center_frequency.__doc__


    def set_span_frequency(self, span):
        self.devh.set_span_frequency(span)
    set_span_frequency.__doc__ = FSUP50.set_span_frequency.__doc__

    def get_marker_frequency(self):
        return self.devh.get_marker_frequency()
    get_marker_frequency.__doc__ = FSUP50.get_marker_frequency.__doc__

    def get_marker_amplitude(self, marker=1):
        if self.params["devicedriver"] == 'FSUP50':
            return self.devh.get_marker_amplitude()
        elif self.params["devicedriver"] == 'N9030A':
            return self.devh.get_marker_amplitude(marker)
    get_marker_amplitude.__doc__ = FSUP50.get_marker_amplitude.__doc__

    def get_sweeptime(self):
        return self.devh.get_sweeptime()
    get_sweeptime.__doc__ = FSUP50.get_sweeptime.__doc__

    def set_sweep_single(self, value):
        self.devh.set_sweep_single(value)
    set_sweep_single.__doc__ = FSUP50.set_sweep_single.__doc__

    def set_move_marker_peak(self, marker=1):
        if self.params["devicedriver"] == 'FSUP50':
            self.devh.set_move_marker_peak()
        elif self.params["devicedriver"] == 'N9030A':
            self.devh.set_move_marker_peak(marker)
    set_move_marker_peak.__doc__ = FSUP50.set_move_marker_peak.__doc__

    def get_instrument_select_option(self):
        return self.devh.get_instrument_select_option()
    get_instrument_select_option.__doc__ = N9030A.get_instrument_select_option.__doc__

    def set_instrument_select(self, value):
        self.devh.set_instrument_select(value)
    set_instrument_select.__doc__ = N9030A.set_instrument_select.__doc__

    def set_correction_noise_floor(self, value):
         self.devh.set_correction_noise_floor(value)
    set_correction_noise_floor.__doc__ = N9030A.set_correction_noise_floor.__doc__

    def set_calculate_marker_bandpower(self, value):
        self.devh.set_calculate_marker_bandpower(value)
    set_calculate_marker_bandpower.__doc__ = N9030A.set_calculate_marker_bandpower.__doc__

    def get_marker_band_left_freq(self, marker):
        return self.devh.get_marker_band_left_freq(marker)
    get_marker_band_left_freq.__doc__ = N9030A.get_marker_band_left_freq.__doc__

    def set_marker_band_left_freq(self, marker, freq):
        self.devh.set_marker_band_left_freq(marker, freq)
    set_marker_band_left_freq.__doc__ = N9030A.set_marker_band_left_freq.__doc__

    def get_marker_band_right_freq(self, marker):
        return self.devh.get_marker_band_right_freq(marker)
    get_marker_band_right_freq.__doc__ = N9030A.get_marker_band_right_freq.__doc__

    def set_marker_band_right_freq(self, marker, freq):
        self.devh.set_marker_band_right_freq(marker, freq)
    set_marker_band_right_freq.__doc__ = N9030A.set_marker_band_right_freq.__doc__

    def get_calculate_marker_x(self, marker):
         return self.devh.get_calculate_marker_x(marker)
    get_calculate_marker_x.__doc__ = N9030A.get_calculate_marker_x.__doc__

    def set_resolution_bw_auto(self, value):
        self.devh.set_resolution_bw_auto(value)
    set_resolution_bw_auto.__doc__ = N9030A.set_resolution_bw_auto.__doc__

    # noinspection PyUnusedLocal
    def get_status(self, extended=False):
        """
        Returns dictionary with device status.

        This device returns:
            * dummy

        :returns: dummy function
        :rtype: dictionary
        """
        return self.last_measurement