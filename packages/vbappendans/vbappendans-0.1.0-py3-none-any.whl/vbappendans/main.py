import click
from .gptvision import imgtojson
from .appendfromjson import appendfromjson

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'],
                        auto_envvar_prefix='VBAPPENDANS')


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


main.add_command(imgtojson)
main.add_command(appendfromjson)
