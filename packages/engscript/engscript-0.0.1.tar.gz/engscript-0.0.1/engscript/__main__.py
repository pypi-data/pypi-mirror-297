'''
This module holds entrypoints for comand line utilities. Currently
the only command line utility provided is engscript-doc.

For more information on engscript-doc see `engscript.doc`
'''

import sys
import argparse

from engscript import doc


def get_doc_parser() -> argparse.ArgumentParser:
    """
    Return the argument parser for the engscript-doc CLI.

    :returns: An `argparse.ArgumentParser` for parsing the engscript-doc CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="Automatically generate images for your EngScript API docs. "
        "This only generates the images you need to use an program "
        "such as pdoc to generate the final documentation.")
    parser.add_argument(
        "modules",
        type=str,
        default=[],
        metavar="module",
        nargs="*",
        help="Python module names. These may be importable Python module names "
        "(e.g `engscript.engscript`) or file paths (`./engscript/engscript.py`). "
        "Exclude submodules by specifying a negative !regex pattern, e.g. "
        "`engscript-doc engscript '!engscript.doc'`")
    return parser


def doc_cli(args: list[str] | None = None) -> None:
    """
    Entry point for engscript-docs
    """
    parser = get_doc_parser()
    opts = parser.parse_args(args)
    if not opts.modules:
        parser.print_help()
        print("\n\nError: Please specify which files or modules you want to document.")
        sys.exit(1)

    if doc.generate(opts.modules) > 0:
        # Generate returns the number of warnings.
        # Exit with error code if this is non-zero
        sys.exit(2)
