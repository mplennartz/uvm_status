"""Placehold doc string for imports"""
from argparse import ArgumentParser
from os import environ


# -------------------------------------------------------------------------------------
# simple command line parser for 2 inputl
# -------------------------------------------------------------------------------------
class BaseParser(ArgumentParser):
    """Placeholder doc string for BaseParser Class"""

    def __init__(self):

        super(BaseParser, self).__init__()

        # not additional commmand line arguments beyond -a or --async_mode
        # self.add_argument(
        #    "-a", "--async_mode", action="store_true", help="Activate nice Mode."
        # )
        if environ.get("PROJECT") is not None:
            self.add_argument(
                "-d",
                "--directory",
                type=str,
                default=environ.get("PROJECT"),
                help="Set path to working directory; $PROJECT default if set",
            )
        else:
            self.add_argument(
                "-d",
                "--directory",
                type=str,
                help="REQUIRED: set path to working directory",
                required=True,
            )
        self.add_argument(
            "-i",
            "--input_file",
            type=str,
            default=None,
            help="File to load previous test results to prevent re-reading of completed tests",
        )
        self.add_argument(
            "-o",
            "--output_file",
            type=str,
            default=None,
            help="File to save off test results that can be kept for ref or loaded back in",
        )
        self.add_argument("-n", "--number", type=int, default=0, help="increase count")

    # found another way to set async_mode true without method usage but left for refg
    # example from https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    #        self.add_argument( "-a",


#                           "--async",
#                           type=self.str2bool,
#                           nargs='?',
#                           const=True,
#                           default=False,
#                           help="Activate nice Mode." )

#    def str2bool(self,v):
#        if isinstance(v, bool):
#            return v
#        if v.lower() in ('yes', 'true', 't', 'y', '1'):
#            return True
#        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
#            return False
#        else:
#            raise argparse.ArgumentTypeError('Boolean value expected.')
