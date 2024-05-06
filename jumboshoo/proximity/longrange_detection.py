from cv2 import fastNlMeansDenoising
import numpy as np
import time
import board
import busio
import threading
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message, print_context_message
from scipy.signal import find_peaks
from scipy.fft import fft
from jumboshoo.clidisplay import Display

# 
class LongProximity:
    def __init__(self, **kwargs):
        print_context_message("Initializing Long Proximity (seismograph)")
        self.sample_rate: int = int(kwargs.get('seismograph_sample_rate', 100))
        self.data_points: int = self.sample_rate

        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1015(i2c)
        self.chan = AnalogIn(ads, ADS.P0)
        self.the_voltage_array = []

        self.collecting = True
        self.collection_thread = threading.Thread(target=self._sample_adc)
        self.collection_thread.start()
        print_info_message("Sampling ADC in the background")

    def __del__(self):
        self.collecting = False
        self.collection_thread.join()

    def _sample_adc(self):
        while self.collecting:
            self.the_voltage_array += [self.chan.voltage]

            if len(self.the_voltage_array) > self.data_points:
                self.the_voltage_array.pop(0)
            time.sleep(1/self.sample_rate)

    def get_instant_frequency(self) -> float:
        n = len(self.the_voltage_array)
        if n == 0:
            return 0.00

        freq = np.fft.fftfreq(n, d=1/self.sample_rate)
        fft_values = fft(self.the_voltage_array)
        magnitude = np.abs(fft_values)

        peaks, _ = find_peaks(magnitude[:n//2])

        if len(peaks) == 0:
            print_warning_message("LongProximity: No peak found")
            return 0.00

        frequencies = []
        for peak in peaks:
            frequencies += [freq[peak]]

        return(max(frequencies))
