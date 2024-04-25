
import numpy as np
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message

class CloseProximity:
    def __init__(self):
        self.data_points = 100

        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1015(i2c)
        self.chan = AnalogIn(ads, ADS.P0)
        self.the_voltage_array = []

    def step(self):

        self.the_voltage_array += [self.chan.voltage]

        if len(self.the_voltage_array) > self.data_points:
            self.the_voltage_array.pop(0)

        # print_info_message("{:>5}\t{:>5.3f}".format(self.chan.value, self.chan.voltage))

    def get_instant_frequency(self):

        if len(self.the_voltage_array) != self.data_points:
            return
            
        # Generate random data
        time = np.linspace(0, 10, self.data_points)  # Time array

        fft_result = np.fft.fft(self.the_voltage_array)
        frequencies = np.fft.fftfreq(self.data_points, d=(time[1] - time[0]))
        for freq, magnitude in zip(frequencies[:self.data_points//2], np.abs(fft_result)[:self.data_points//2]):
            if freq >= 0: # positive frequencies
                print_info_message("Frequency: {:.2f} Hz, Magnitude: {:.2f}".format(freq, magnitude))



        

