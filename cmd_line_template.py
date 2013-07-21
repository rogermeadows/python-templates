#!/usr/bin/env python
'''
#
# Module: xxx.py
# Descr : This module provides ... 
#
# Copyright(c) 2013, Cyan, Inc. All rights reserved.
#
'''

import os
import sys
import logging

###############################################################################
#       _                     _       __ _       _ _   _                      #
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___      #
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|     #
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \     #
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/     #
#                                                                             #
###############################################################################

class Any(object):

    ###############################################################################
    def __init__(self, arg1):
        info('Any: instance created')

    ###############################################################################
    def method1(self, arg1):
        pass


###############################################################################
#                  _                                                          #
#  _ __ ___   __ _(_)_ __                                                     #
# | '_ ` _ \ / _` | | '_  \                                                   #
# | | | | | | (_| | | | | |                                                   #
# |_| |_| |_|\__,_|_|_| |_|                                                   #
#                                                                             #
###############################################################################
def parse_args():
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

    opt_arg = parser.parse_args()
    return (opt_arg[0], opt_arg[1], program_name)

def info(msg, p=True, l=True):
    if p:
        print 'INFO: %s' % msg
    if l:
        logging.info(msg)


def main():
    # =========================================================================
    # Parse command-line arguments
    # =========================================================================
    (opts, args, program_name) = parse_args()

    if opts.log_level == '':
        opts.log_level = 'INFO'
    numeric_level = getattr(logging, opts.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        print 'ERROR: Invalid log level %s' % opts.log_level

    # set up logging
    logging.basicConfig(filename='/tmp/%s.log' % program_name,
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='a',
        level=numeric_level)

    instance = Any('xxx')

if __name__ == "__main__":      # pragma: no cover
    sys.exit(main())



