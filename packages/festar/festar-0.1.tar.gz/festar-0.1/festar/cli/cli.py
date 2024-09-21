"""
Entry Module for Festar CLI
"""
import argparse
import sys
# import click
import logging

# @click.group()
# @click.option("--debug/--no-debug", default=False, help="Enable or disable debug mode.")
# @click.pass_context
def cli(ctx, debug):
    """
    Festar command line tool.
    """
    logging_level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(
        level=logging_level, 
        stream=sys.stderr, 
        format="%(levelname)s(%(name)s): %(message)s",
    )


def main():
    """
    Main entry point for the CLI.
    Returns:
        None
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    run_task_parser = subparsers.add_parser('run', help='Create a task of a specified type')
    run_task_parser.add_argument('--submitter', help='Submitter name')
    args, unknown = parser.parse_known_args()
    if args.subcommand == 'run':
        print("running festar")

if __name__ == "__main__":
    main()