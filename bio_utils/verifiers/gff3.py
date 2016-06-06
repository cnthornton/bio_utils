#! /usr/bin/env python

from __future__ import print_function

"""Verifies a GFF3 file

Usage:

    gff3_verifier <GFF3 file> [--quiet]

Copyright:

    gff3.py verify validity of a GFF3 file
    Copyright (C) 2015  William Brazelton, Alex Hyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
from bio_utils.iterators import gff3_iter
from bio_utils.verifiers import entry_verifier
from bio_utils.verifiers import FormatError
import os
import sys

__author__ = 'Alex Hyer'
__email__ = 'theonehyer@gmail.com'
__license__ = 'GPLv3'
__maintainer__ = 'Alex Hyer'
__status__ = 'Alpha'
__version__ = '1.2.2'


# noinspection PyTypeChecker
def gff3_verifier(entries, line=None):
    """Raises error if invalid GFF3 format detected

    Args:
        entries (list): A list of GFF3Entry objects

        line (int): Line number of first entry

    Raises:
        FormatError: Error when GFF3 format incorrect with descriptive message
    """

    regex = r'^[a-zA-Z0-9.:^*$@!+_?-|]+\t.+\t.+\t\d+\t\d+\t' \
            + r'\d*\.?\d*\t[+-.]\t[.0-2]\t.+{0}$'.format(os.linesep)
    delimiter = r'\t'

    for entry in entries:
        try:
            entry_verifier([entry.write()])
        except FormatError as error:
            # Format info on what entry error came from
            if line:
                intro = 'Line {0}'.format(str(line))
            elif error.part == 0:
                intro = 'Entry with source {0}'.format(entry.subject)
            else:
                intro = 'Entry with Sequence ID {0}'.format(entry.query)

            # Generate error
            if error.part == 0:
                msg = '{0} has no Sequence ID'.format(intro)
            elif error.part == 1:
                msg = '{0} has no source data'.format(intro)
            elif error.part == 2:
                msg = '{0} has no type data'.format(intro)
            elif error.part == 3:
                msg = '{0} has no start position'.format(intro)
            elif error.part == 4:
                msg = '{0} has no end position'.format(intro)
            elif error.part == 5:
                msg = '{0} has no score data'.format(intro)
            elif error.part == 6:
                msg = '{0} has no strand data'.format(intro)
            elif error.part == 7:
                msg = '{0} has no phase data'.format(intro)
            elif error.part == 8:
                msg = '{0} has no attributes'.format(intro)
            else:
                msg = 'Unknown Error: Likely a Bug'
            raise FormatError(message=msg)

        if line:
            line += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('gff3File',
                        help='GFF3 file to verify')
    args = parser.parse_args()

    with open(args.gff3File, 'rU') as in_handle:
        valid = gff3_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.gff3File))
    else:
        print('{} is not valid'.format(args.gff3File))


if __name__ == '__main__':
    main()
    sys.exit(0)
