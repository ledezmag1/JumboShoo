debug = True

class Colors:
    _no_color = False

    @classmethod
    def set_no_color(cls, no_color):
        cls._no_color = no_color

    @classmethod
    def RED(cls):
        return '\033[91m' if not cls._no_color else ''

    @classmethod
    def GREEN(cls):
        return '\033[92m' if not cls._no_color else ''

    @classmethod
    def YELLOW(cls):
        return '\033[93m' if not cls._no_color else ''

    @classmethod
    def BLUE(cls):
        return '\033[94m' if not cls._no_color else ''

    @classmethod
    def MAGENTA(cls):
        return '\033[95m' if not cls._no_color else ''

    @classmethod
    def CYAN(cls):
        return '\033[96m' if not cls._no_color else ''

    @classmethod
    def WHITE(cls):
        return '\033[97m' if not cls._no_color else ''

    @classmethod
    def RESET(cls):
        return '\033[0m' if not cls._no_color else ''


def print_info_message(message):
    if debug:
        print(Colors.BLUE() + "INFO: " + Colors.RESET() + message)


def print_error_message(message):
    print(Colors.RED() + "ERROR: " + Colors.RESET() + message)


def print_warning_message(message: str):
    if debug:
        print(Colors.YELLOW() + "WARNING: " + Colors.RESET() + message)


def print_context_message(message):
    if debug:
        print(Colors.MAGENTA() + "CONTEXT: " + Colors.RESET() + message)

def print_trace_message(message):
    if debug:
        print(Colors.CYAN() + "TRACE: " + Colors.RESET() + message)

def get_user_input(prompt, default=None):
    prefix = Colors.GREEN() + "USER: " + Colors.RESET() + prompt
    if default is None:
        return input(prefix)
    else:
        return input(prefix + f"[{default}]: ") or default

