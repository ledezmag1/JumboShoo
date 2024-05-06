import time
from jumboshoo.proximity import CloseProximity
from jumboshoo.proximity import LongProximity
from jumboshoo.clidisplay import Display
from jumboshoo.thump import Thump
from jumboshoo.utils import print_info_message

class TheStateMachine:
    def __init__(self, **kwargs):
        # Initialize the peripherals

        # Debug monitor
        self.disp = Display()
        # Long Range Detect (seismograph)
        self.long_proximity = LongProximity(**kwargs)
        # Short Range Detect (picam + nn)
        self.short_proximity = CloseProximity(**kwargs)
        # Thumper
        self.thump = Thump(**kwargs)

        # Globals 
        self.headless: bool = bool(kwargs.get('headless', True))
        self.jumbo_thump_freq_threshold_hz: float = float(kwargs.get('long_range_freq_threshold', '35.00'))
          # The number of seconds we should check for an elephant using short range detect before kicking back
          # into long range detect. If an elephant is detected we reset the timer.
        self.short_range_on_duration_sec: int = int(kwargs.get('short_range_on_duration', '10'))

        # State
        self.long_range_on = True
        self.short_range_on = False
        self.thump_on = False
        
        # Timers
        self.short_range_collection_start_time: float = 0.00

        if not self.headless:
            self.disp.start()
        self.run()

    def __str__(self) -> str:
        def bool_2_str(val: bool) -> str:
            if val:
                return "on"
            return "off"

        return f"Long Range: {bool_2_str(self.long_range_on)} Short Range: {bool_2_str(self.short_range_on)} Thumper: {bool_2_str(self.thump_on)} "

    def run(self):
        # State machine
        while True:
            if self.long_range_on:
                self.update_long_range_state()

            if self.short_range_on:
                self.update_short_range_state()

            self.disp.string1 = str(self)


    def update_long_range_state(self):
        instant_freq = self.long_proximity.get_instant_frequency()
        if instant_freq >= self.jumbo_thump_freq_threshold_hz:
            # Disable long range detect and transition to short range detect
            freq_str = "%0.2f" % instant_freq
            self.state_debug_message(f"Elephant detection possible - Instant freq {freq_str} >= {self.jumbo_thump_freq_threshold_hz}")

            self.long_range_on = False
            self.short_range_on = True
            self.thump_on = False

            if not self.short_proximity.camera_on:
                # This blocks until the camera is on
                self.short_proximity.start()

            self.short_range_collection_start_time = time.perf_counter()
        else:
            self.long_range_on = True
            self.short_range_on = False
            self.thump_on = False

    def update_short_range_state(self):
        now = time.perf_counter()
        if now - self.short_range_collection_start_time > self.short_range_on_duration_sec:
            # If we've been looking for an elephant for too long, kick back into long range detect and turn the camera off
            elapsed = "%0.2f" % (now - self.short_range_collection_start_time)
            self.state_debug_message(f"SRD: Didn't see an elephant after {elapsed}")
        
            self.long_range_on = True
            self.short_range_on = False
            self.thump_on = False

            if self.thump.thumping:
                self.thump.stop()

            self.short_proximity.stop()
            self.short_range_collection_start_time = 0.00

            return
            
        if self.short_proximity.is_elephant():
            self.state_debug_message("SRD: Elephant detected - thumping")
            # Oh shit there's an elephant. Time 4 JumboShoo
            self.short_range_collection_start_time = time.perf_counter()

            # Blocking start the thumper
            if not self.thump.thumping:
                self.thump.start()
            
            self.long_range_on = False
            self.short_range_on = True
            self.thump_on = True
            return

        # If there was no elephant, we stay in this state until the short_range_collection timer elapses

    def state_debug_message(self, message: str):
        print_info_message(f"TSM: {message}")

        

