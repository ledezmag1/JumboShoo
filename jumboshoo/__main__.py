import click
import time

# Package imports
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message
from jumboshoo.proximity import CloseProximity, longrange_detection
from jumboshoo.proximity import LongProximity
from jumboshoo.clidisplay import Display

@click.group()
def cli():
    pass

@click.command()
@click.option('--model-path', help='Path to the model that should be used', default='/home/jumboshoo1/dev/jumboshoo/models/yolov8n.pt')
@click.option('--display', is_flag=True, help='Start with a display')
def close_proximity(**kwargs):
    disp = Display()
    long_proximity = CloseProximity(disp, **kwargs)
    long_proximity.start()
    
    while True:
        long_proximity.is_elephant()
        time.sleep(.5)


    disp.start()
    time.sleep(10)
    disp.stop()

@click.command()
@click.option('--seismograph-sample-rate', help='The rate that jumboshoo should sample the seismograph [Hz]', default='100')
@click.option('--seismograph-data-points', help='', default='100')
def long_proximity(**kwargs):
    
    disp = Display()
    # disp.start()

    close_proximity = LongProximity(disp, **kwargs)
    time.sleep(10)

    close_proximity.get_instant_frequency()

    # while True:
    #     time.sleep(1/close_proximity.sample_rate)
    

cli.add_command(close_proximity)
cli.add_command(long_proximity)

if __name__ == '__main__':
    cli()

