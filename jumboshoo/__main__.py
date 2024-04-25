import click
import time

# Package imports
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message
from jumboshoo.proximity import CloseProximity
from jumboshoo.proximity import LongProximity

@click.group()
def cli():
    pass

@click.command()
def close_proximity(**kwargs):
    close_proximity = CloseProximity()

    while True:
        close_proximity.step()
        time.sleep(0.100)
        close_proximity.get_instant_frequency()
    

cli.add_command(close_proximity)

if __name__ == '__main__':
    cli()

