#!/usr/bin/env python

'''Verifies a M8 file

Usage:

    m8.py <m8File>
'''

__version__ = '1.0.0.0'

import argparse
from bio_utils.verifiers.line_verifier import verify_lines
from bio_utils.iterators.m8 import m8_iter
import sys

def m8_verifier(handle, log_file = None):
    '''Returns True if M8 file is valid and False if file is not valid'''

    lines = []
    for m8Entry in m8_iter(handle):
        entry = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(\
            m8Entry['queryID'], m8Entry['subjectID'], m8Entry['percIdentical'],\
            m8Entry['alignLen'], m8Entry['mismatchCount'], m8Entry['gapCount'],\
            m8Entry['queryStart'], m8Entry['queryEnd'],\
            m8Entry['subjectStart'], m8Entry['subjectEnd'], m8Entry['eValue'],\
            m8Entry['bitScore'])
        lines.append(entry)
    regex = r'^.+\t.+\t\d+\.?\d*\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t\d+\t'\
            + r'\d+\.?\d*(e-)?\d*\t\d+\.?\d*\n$'
    delimiter = r'\t'
    m8Status = verify_lines(lines, regex, delimiter, log_file = log_file)
    return m8Status

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('m8File',
                        help = 'M8 file to verify')
    args = parser.parse_args()

    with open(args.m8File, 'rU') as in_handle:
        valid = m8_verifier(in_handle)
    if valid:
        print('{} is valid'.format(args.m8File))
    else:
        print('{} is not valid'.format(args.m8File))
    sys.exit(0)
