import threading
from pathlib import Path
import pygame
import numpy as np
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message, print_context_message

class Thump:
    def __init__(self, **kwargs):
        print_context_message("Initializing the Thumper")

        self.audio_dir: Path = Path(str(kwargs.get('audio_dir', '/home/jumboshoo1/dev/jumboshoo/JumboShoo/audio')))
        if self.audio_dir.is_dir():
            raise Exception(f"{kwargs.get('audio_dir', '/home/jumboshoo1/dev/jumboshoo/JumboShoo/audio')} is not a directory")

        self.tone_frequency: int = kwargs.get('tone_frequency', 440)
        self.audio_sample_rate: int = kwargs.get('audio_sample_rate', 44100)
        self.volume: float = kwargs.get('volume', 0.5)
        self.tone_duration_sec: int = 1

        self.thumping = False
        self.thump_thread: threading.Thread | None = None

    def start(self):
        print_info_message("Starting Thumper")
        pygame.mixer.init(frequency=44100, size=-16, channels=1)
        if self.thump_thread is None:
            self.thump_thread = threading.Thread(target=self._thump)
        self.thump_thread.start()
        self.thumping = True

    def stop(self):
        print_info_message("Stopping Thumper")
        self.thumping = False
        if self.thump_thread is not None:
            self.thump_thread.join()
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        self.thump_thread = None

    def _thump(self):
        # Generate the tone
        self.audio_dir.
        pygame.mixer.music.load()
        # t = np.linspace(0, self.tone_duration_sec, int(self.audio_sample_rate * self.tone_duration_sec), False)
        # tone = np.sin(self.tone_frequency * 2 * np.pi * t)
        # sound = pygame.sndarray.make_sound((32767 * self.volume * tone).astype(np.int16))
        # while self.thumping:
        #     sound.play(-1)  # The '-1' argument makes the sound play indefinitely
        #     pygame.time.wait(int(self.tone_duration_sec * 1000))  # Wait for the duration of the tone in milliseconds
        #     sound.stop()

