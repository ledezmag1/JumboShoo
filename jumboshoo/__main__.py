import click
import time

# Package imports
from jumboshoo.thump import Thump
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message
from jumboshoo.proximity import CloseProximity
from jumboshoo.proximity import LongProximity
from jumboshoo.clidisplay import Display

from jumboshoo.statemachine import TheStateMachine

@click.group()
def cli():
    pass

@click.command()
@click.option('--tone-frequency', type=int, help='Frequency of the tone to generate (Hz)', default=20)
@click.option('--audio-sample-rate', type=int, help='Sample rate for audio output (Hz)', default=44100)
@click.option('--volume', type=float, help='Volume of the tone (0.0 to 1.0)', default=0.5)
@click.option('--audio-dir', type=str, help='The path to a directory containing audio files', default='/home/jumboshoo1/dev/jumboshoo/JumboShoo/audio')
@click.option('--thumper-use-sine', is_flag=True, help='Instead of selecting a random audio file, generate a sine wave using the other thumper params')
def thump(**kwargs):
    thump = Thump(**kwargs)
    thump.start()
    while True:
        time.sleep(1)

@click.command()
@click.option('--model-path', help='Path to the model that should be used', default='/home/jumboshoo1/dev/jumboshoo/models/yolov8n.pt')
@click.option('--display', is_flag=True, help='Start with a display')
def close_proximity(**kwargs):
    short_proximity = CloseProximity(**kwargs)
    short_proximity.start()
    
    while True:
        short_proximity.is_elephant()
        time.sleep(.5)

@click.command()
@click.option('--seismograph-sample-rate', help='The rate that jumboshoo should sample the seismograph [Hz]', default='100')
def long_proximity(**kwargs):
    disp = Display()
    # disp.start()
    long_proximity = LongProximity(**kwargs)

    # time.sleep(5)
    # long_proximity.plot_fft()

    while True:
        time.sleep(1/long_proximity.sample_rate)
        freq = long_proximity.get_instant_frequency()
        freq_str = "%0.2f" % freq
        disp.string1 = f"Frequency: {freq_str}"
        

@click.command()
@click.option('--seismograph-sample-rate', help='The rate that jumboshoo should sample the seismograph [Hz]', default='100')
@click.option('--model-path', help='Path to the model that should be used', default='/home/jumboshoo1/dev/jumboshoo/models/yolov8n.pt')
@click.option('--headless', is_flag=True, help='Don\'t initialize an output of any sort and only send logs to the journal')
@click.option('--long-range-freq-threshold', help='The frequency threshold that JumboShoo should use to determine if an elephant is nearby [Hz]', default='10.00')
@click.option('--short-range-on-duration', help='The number of seconds to look for elephants using the camera and nn classifier (s)', default='10')
@click.option('--tone-frequency', type=int, help='Frequency of the tone to generate (Hz)', default=30)
@click.option('--audio-sample-rate', type=int, help='Sample rate for audio output (Hz)', default=44100)
@click.option('--volume', type=float, help='Volume of the tone (0.0 to 1.0)', default=0.5)
@click.option('--thumper-use-sine', is_flag=True, help='Instead of selecting a random audio file, generate a sine wave using the other thumper params')
def main(**kwargs):
    # Initialize and start The State Machine
    TheStateMachine(**kwargs)

cli.add_command(close_proximity)
cli.add_command(long_proximity)
cli.add_command(thump)
cli.add_command(main)

if __name__ == '__main__':
    cli()

