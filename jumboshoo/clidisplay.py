import time
import sys
import threading

class Display:
    def __init__(self):
        self.running = False
        self.thread: threading.Thread | None = None

        self.string1 = ""
        self.string2 = ""
        self.string3 = ""

    def start(self):
        """Starts the loading animation in a separate thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.start()

    def _animate(self):
        """Private method to display the loading animation."""
        while self.running:
            sys.stdout.write('\r' + f"{self.string1} {self.string2} {self.string3}")
            sys.stdout.flush()
            time.sleep(0.1)

        return

    def stop(self):
        """Stops the loading animation and clears the screen."""
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join()
            sys.stdout.write(" Done\n")
