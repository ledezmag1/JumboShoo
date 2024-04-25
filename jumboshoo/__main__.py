import click

# Package imports
import jumboshoo.utils
from jumboshoo.utils import print_info_message, print_warning_message, print_error_message

@click.group()
def cli():
    pass

cli.add_command(generate_repository_docs)

if __name__ == '__main__':
    cli()

