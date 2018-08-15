from __future__ import absolute_import, division, print_function

import logging
from sytpy.devices.General.validators import truncated_range, strict_range
from sytpy.devices.General.Instrument import Instrument

from time import sleep

FSUP50_RESET = "*RST\n"
FSUP50_WAIT_TO_COMPLETE = "*OPC?\n"
FSUP50_START_FREQUENCY_SET  = "FREQ:STAR %f"
FSUP50_START_FREQUENCY_GET  = "FREQ:STAR?"
FSUP50_STOP_FREQUENCY_SET   = "FREQ:STOP %f"
FSUP50_STOP_FREQUENCY_GET   = "FREQ:STOP?"
FSUP50_VIDEO_BW_SET         = "BAND:VID %fHz"
FSUP50_VIDEO_BW_GET         = "BAND:VID?"
FSUP50_RESOLUTION_BW_SET    = "BAND:AUTO OFF"
FSUP50_RESOLUTION_BW_GET    = "BAND?"
FSUP50_CENTER_FREQUENCY_SET = "FREQ:CENT %f"
FSUP50_SPAN_FREQUENCY_SET   = "FREQ:SPAN %f"
FSUP50_MARKER_FREQUENCY_GET = "CALC:MARK:COUN ON"
FSUP50_MARKER_AMPLITUDE_GET = "CALC:MARK:Y?"
FSUP50_SWEEPTIME_GET    = "SWE:TIME?"
FSUP50_SWEEP_SINGLE_SET = "INIT:CONT OFF"
FSUP50_MOVE_MARKER_PEAK = "CALC:MARK:MAX"


class FSUP50(Instrument):
    """ Represents the R&S FSUP Signal Source Analyzer
    and provides a high-level interface for taking scans.
    """

    def __init__(self, resourceName, **kwargs):
        logger = logging.getLogger(__name__)

        super(FSUP50, self).__init__(
            resourceName,
            "R&S FSUP Signal Source Analyzer",
            **kwargs
        )

        self.model = self.id.split(",")[1]
        self.vendor = self.id.split(",")[0]
        self.serial = self.id.split(",")[2]
        self.fw = self.id.split(",")[3]

    def rst(self):
        """
        Send a \*rst to the osa and check for opc.

        :return: answer from opc, 0 = no failure

        """
        cmd = FSUP50_RESET
        self.write(cmd)
        sleep(FSUP50_WAIT_TO_COMPLETE)

        # check for opc
        ret_value = self.wait_to_complete()
        return (ret_value)

    def wait_to_complete(self):
        """
         Function to instruct the device to finish the current command

        """
        cmdstr = FSUP50_WAIT_TO_COMPLETE
        self.write(cmdstr)
        return

    start_frequency = Instrument.control(
        FSUP50_START_FREQUENCY_GET,
        FSUP50_START_FREQUENCY_SET,
        """
        Start frequency property.
        
        The allowed range of values for the start frequency is:
        
            0 Hz <= fstart <= fmax - minspan
            
        with:
            * fstart the start frequency
            * minispan the smallest selectable span (10 Hz) 
            * fmax the max. frequency
        
        A floating point property that represents the start frequency.
        Specifies the minimum frequency for the x-axis.
        
        This property can be set or get.
        Unit for get and set is Hz.
        Allowed range ?
        """,
        validator = strict_range, values = [0, 50e9 ],
        set_wait=True,
    )
    def set_start_frequency(self, freq):
        self.start_frequency = freq
    set_start_frequency.__doc__ = start_frequency.__doc__

    def get_start_frequency(self):
        return self.start_frequency
    get_start_frequency.__doc__ = start_frequency.__doc__

    stop_frequency = Instrument.control(
        FSUP50_STOP_FREQUENCY_GET,
        FSUP50_STOP_FREQUENCY_SET,
        """
        A floating point property that represents the start frequency.
        Specifies the minimum frequency for the x-axis.
        
        This property can be set and get.
        Unit for get and set is Hz.
        Allowed range ?
        """,
        validator = strict_range, values = [ ],
        set_wait=True,
    )

    def set_stop_frequency(self, freq):
        self.stop_frequency = freq
    set_stop_frequency.__doc__ = stop_frequency.__doc__

    def get_stop_frequency(self):
        return self.stop_frequency
    get_stop_frequency.__doc__ = stop_frequency.__doc__

    video_bw = Instrument.control(
        FSUP50_VIDEO_BW_GET,
        FSUP50_VIDEO_BW_SET,
        """
        video bandwidth property. 
        
        The video bandwidths are available in 
        1, 2, 3, 5, 10 steps between 1 Hz and 10 MHz.
        
        They can be set in accordance with the resolution bandwidth.
        
        This property can be set and get .        
        """,
        validator = strict_range, values = [1, 10],
        set_wait=True,
    )
    def set_video_bw(self, bw):
        self.video_bw = bw
    set_video_bw.__doc__ = video_bw.__doc__

    def get_video_bw(self):
        return self.video_bw
    get_video_bw.__doc__ = video_bw.__doc__

    resolution_bw = Instrument.control(
        FSUP50_RESOLUTION_BW_GET,
        FSUP50_RESOLUTION_BW_SET,
        """
        Resoultion bandwith property.
        
        The R&S FSUP offers resolution bandwidths from 10 Hz to 20 MHz 
        in 1, 2, 3, 5, 10 steps and additionally 50 MHz as maximum bandwidth.
        """,
        validator = strict_range, values = [10, 50],
        set_wait=True,
    )

    def set_resolution_bw(self, resolution_bw):
        self.resolution_bw = resolution_bw
    set_resolution_bw.__doc__ = resolution_bw.__doc__

    def get_resolution_bw(self):
        return self.resolution_bw
    get_resolution_bw.__doc__ = resolution_bw.__doc__

    def set_center_frequency(self, freq):
        """
        Set the center frequency

        :return: center frequency in Hz
        """
        cmd= FSUP50_CENTER_FREQUENCY_SET % freq
        self.write(cmd)

    def set_span_frequency(self, span):
        """
        Set the span frequency

        :return: span frequency in Hz
        """
        cmd = FSUP50_SPAN_FREQUENCY_SET % span
        self.write(cmd)

    def get_marker_frequency(self):
        """
        Returns the marker frequency

        :return: frequency in Hz
        """
        return self.ask(FSUP50_MARKER_FREQUENCY_GET)

    def get_marker_amplitude(self):
        """
        Returns the marker amplitude

        :return: amplitude
        """
        return self.ask(FSUP50_MARKER_AMPLITUDE_GET)

    def get_sweeptime(self):
        """
        Returns the sweep time

        :return: sweeptime in sec
        """
        return self.ask(FSUP50_SWEEPTIME_GET)

    def set_sweep_single(self):
        """
        Sets the sweep single on the device

        :return: sweep single set
        """
        cmd = FSUP50_SWEEP_SINGLE_SET
        self.write(cmd)

    def set_move_marker_peak(self):
        """
        Set the marker to peak

        :return: success
        """
        cmd = FSUP50_MOVE_MARKER_PEAK
        self.write(cmd)