"""
"""

from sysconfig import get_scheme_names
import clr
clr.AddReference("System")

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import random  # only used for dummy data
import os

# adding relative path to the directory with all the DLLs that are now build into the repository
path = os.path.abspath(__file__)
head,tail = os.path.split(path)
sys.path.append(os.path.join(head,'ThorLabsDLLs'))

from System import String
from System import Decimal
from System.Collections import *

# constants

serial = '45252134'

clr.AddReference("Thorlabs.MotionControl.Controls")
import Thorlabs.MotionControl.Controls

clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.IntegratedStepperMotorsCLI")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.IntegratedStepperMotorsCLI import *

POLLING_INTERVAL = 250
ENABLE_SLEEP_TIME = 0.1
INIT_TIMEOUT = 5000


class LongTravelStage():

    def __init__(self):
        pass

    def init(self, serial):
        self.device = self.initialize_device(serial)

    def kill(self):
        self.device.StopPolling()
        self.device.StopImmediate()
        self.device.Disconnect()
        del self

        
    def initialize_device(self,serial):
        from Thorlabs.MotionControl import IntegratedStepperMotorsCLI
        clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
        from time import sleep
        # the request to build the device list is critical to operation of this code
        device_list_result = DeviceManagerCLI.BuildDeviceList()
        device = Thorlabs.MotionControl.IntegratedStepperMotorsCLI.LongTravelStage.CreateLongTravelStage(serial)
        device.Connect(serial)
        device.WaitForSettingsInitialized(INIT_TIMEOUT) #I think this is a crucial step in the initializatio
        device.EnableDevice()
        config = device.LoadMotorConfiguration(serial)
        deviceInfo = device.GetDeviceInfo()
        device.StartPolling(0)
        return device

    def print_positions(device):
        self.device.RequestPosition()

        return Decimal.ToDouble(self.device.DevicePosition)

    def home(self):
        """
        """
        self.device.Home(0)

    def is_homed(self):
        return device.device.Status.IsHomed

    def move_to(self,pos, stop_first = False):
        """
        moves to specifid position
        """
        if stop_first:
            self.stop_immediate()
        if not self.is_busy:
            self.device.MoveTo(Decimal(pos),0)

    def get_position(self):
        """
        returns current position
        """
        clr.AddReference("System")
        from System import Decimal
        return  Decimal.ToDouble(self.device.DevicePosition)

    def set_position(self, value):
        """
        sets new position.
        If stage is moving, stage is stopped and new position is set.
        """
        self.move_to(pos = value)

    position = property(get_position, set_position)

    def get_backlash(self):
        """
        returns current backlash settings
        """
        return Decimal.ToDouble(device.device.GetBacklash())

    def get_is_busy(self):
        """
        """
        return self.device.IsDeviceBusy
    is_busy = property(get_is_busy)

    def stop_immediate(self):
        """
        stops any motion immediately 
        """
        self.device.StopImmediate()

    def disconnect(self):
        """
        """
        self.device.Disconnect()


if __name__ is "__main__":
    # for testing and debuging
    device = LongTravelStage()
    device.init(serial = '45252134')
    print('device.home()')
    print('device.move_to(100)')
