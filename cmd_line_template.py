#!/usr/bin/env python
'''
# File: xxx.py
# Descr : This module provides ... 
#
'''

import os
import sys
import logging
from sys_logger import get_sys_logger

def parse_args(args):
    from optparse import OptionParser

    usage = './%prog [options] agr1 agr2 ...'
    description = ('''This script does ....''')

    program_name = os.path.basename(sys.argv[0])
    epilog = 'Example: python %s <arg1_info>' % program_name

    parser = OptionParser(usage=usage, version='%prog:  0.1', description=description, epilog=epilog)

    parser_conf = ( 
        [   
            (('-l', '--log'),    'log_level',   '', 'store', 'Set logging level'),
            (('-v', '--verbose'), 'verbose', False, 'store_true', 'Print (more) debug info'),
        ]   
    )   

    for option, dest, default, action, help in parser_conf:
        if type(option) is str:
            parser.add_option(option, dest = dest, action = action, default = default, help = help)
        else:
            parser.add_option(option[0], option[1], dest = dest, action = action, default = default, help = help)

    opt_arg = parser.parse_args(args)
    return (opt_arg[0], opt_arg[1], program_name)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    (opts, args, program_name) = parse_args(argv)

    # set up logging
    logger = get_sys_logger('xxx.py')
    logger.error('Testing sys_logger from xxx.py') 

    arg_count = 0
    for arg in args:
        notify('arg[%d]=%r' % (arg_count, arg))
        arg_count += 1

if __name__ == "__main__":      # pragma: no cover
    sys.exit(main())



