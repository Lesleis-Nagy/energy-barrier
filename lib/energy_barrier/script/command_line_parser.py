r"""
Command line argument parameters.
"""

from argparse import ArgumentParser

def command_line_parser():
    r"""
    Create a command line parser object.
    :return: a command line parser object.
    """
    parser = ArgumentParser()

    parser.add_argument("path_file", help="the tecplot file containing paths/domain structures.")
    parser.add_argument("applied_x", help="the applied field x-direction")
    parser.add_argument("applied_y", help="the applied field y-direction")
    parser.add_argument("applied_z", help="the applied field z-direction")
    parser.add_argument("strength", help="the applied field strength")
    parser.add_argument("unit", help="the applied field unit", choices=["T", "mT", "uT", "nT"])

    return parser
