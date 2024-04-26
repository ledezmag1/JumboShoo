import click
import time

# Package imports
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message
from jumboshoo.proximity import CloseProximity
from jumboshoo.proximity import LongProximity
from jumboshoo.clidisplay import Display

@click.group()
def cli():
    pass

@click.command()
@click.option('--seismograph-sample-rate', help='The rate that jumboshoo should sample the seismograph [Hz]', default='25')
def close_proximity(**kwargs):
    disp = Display()
    disp.start()

    close_proximity = CloseProximity(disp, **kwargs)

    while True:
        close_proximity.get_instant_frequency()
        time.sleep(0.010)

@click.command()
@click.option('--model-path', help='Path to the model that should be used', default='/home/jumboshoo1/dev/jumboshoo/models/yolov8n.pt')
@click.option('--display', is_flag=True, help='Start with a display')
def long_proximity(**kwargs):
    long_proximity = LongProximity(**kwargs)
    disp = Display()

    disp.start()
    time.sleep(10)
    disp.stop()
    
    

cli.add_command(close_proximity)
cli.add_command(long_proximity)

if __name__ == '__main__':
    cli()

