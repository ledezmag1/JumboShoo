import matplotlib.pyplot as plt
from cv2 import MEDIA_FORMAT_GRAY, fastNlMeansDenoising
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

        self.disp = Display()
        # self.disp.start()

    def __del__(self):
        self.collecting = False
        self.collection_thread.join()

    def _sample_adc(self):
        while self.collecting:
            self.the_voltage_array += [self.chan.voltage]

            if len(self.the_voltage_array) > self.data_points:
                self.the_voltage_array.pop(0)
            time.sleep(1/self.sample_rate)

    def plot_fft(self):
        n = len(self.the_voltage_array)
        if n == 0:
            return 0.00

        the_voltage_array_copy = pad_to_nearest_power_of_two(self.the_voltage_array.copy())

        fft_values = np.fft.fft(the_voltage_array_copy)
        magnitude = np.abs(fft_values)**2

        freq = np.fft.fftfreq(n, d=1/self.sample_rate)
        idx = np.argsort(freq)

        plt.plot(freq[idx], magnitude[idx])

    def get_instant_frequency(self) -> float:
        n = len(self.the_voltage_array)
        if n == 0:
            return 0.00

        the_voltage_array_copy = pad_to_nearest_power_of_two(self.the_voltage_array.copy())
        
        fft_values = np.fft.fft(the_voltage_array_copy)
        magnitude = np.abs(fft_values)**2

        freq = np.fft.fftfreq(n, d=1/self.sample_rate)

        peaks, _ = find_peaks(magnitude[:n//2])

        if len(peaks) == 0:
            print_warning_message("LongProximity: No peak found")
            return 0.00

        max = 0.00
        predominant_frequency = 0.00
        for peak in peaks:
            if magnitude[peak] > max:
                predominant_frequency = freq[peak]
                max = magnitude[peak]

        max_str = "%0.2f" % max
        predominant_frequency_str = "%02f" % predominant_frequency
        print_info_message(f"Highest amplitude: {max_str} Predominant frequency: {predominant_frequency_str}")
        
        return float(predominant_frequency)

def pad_to_nearest_power_of_two(array):
    # Calculate the original length of the array
    original_length = len(array)
    
    # Calculate the nearest power of two
    nearest_power_of_two = 2**np.ceil(np.log2(original_length)).astype(int)
    
    # Calculate the total amount of padding needed
    total_padding = nearest_power_of_two - original_length
    
    # Calculate padding for both sides
    padding_left = total_padding // 2
    padding_right = total_padding - padding_left
    
    # Pad the array with zeros on both sides
    padded_array = np.pad(array, (padding_left, padding_right), mode='constant')
    
    return padded_array
