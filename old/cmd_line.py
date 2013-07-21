#!/usr/bin/env python

''' This is a template for a python command line interpreter  '''

#*******************************************************************************
# Copyright (C) 2012 by Cyan Inc.
# All rights reserved.
#
# 1383 N. McDowell Blvd., Suite 300
# Petaluma, CA 94954
# (707) 735-2300
#                   _____
#                 /\   _ \
#                 \ \ \/\_\  __  __     __      ___
#                  \ \ \/_/_/\ \/\ \  / __`\  /   _`\
#                   \ \ \/\ \ \ \_\ \/\ \/\.\_/\ \/\ \
#                    \ \____/\/`____ \ \__/.\_\ \_\ \_\
#                     \/___/  `/___/> \/__/\/_/\/_/\/_/
#                                /\___/
#                                \/__/
#                   _____          __
#                 /\  __ \        /\ \__  __
#                 \ \ \/\ \  _____\ \  _\/\_\     ___   ____
#                  \ \ \ \ \/\  __`\ \ \/\/\ \  / ___\ /  __\
#                   \ \ \_\ \ \ \/\ \ \ \_\ \ \/\ \__//\__, `\
#                    \ \_____\ \ ,__/\ \__\\ \_\ \____\/\____/
#                     \/_____/\ \ \/  \/__/ \/_/\/____/\/___/
#                              \ \_\
#                               \/_/
# PROPRIETARY NOTICE
# This Software consists of confidential information.
# Trade secret law and copyright law protect this Software.
# The above notice of copyright on this Software does not indicate
# any actual or intended publication of such Software.
#
# MODULE NAME:
#  cmd_line.py
#
# DESCRIPTION:
#  Template for a command line interpreter written in python.
#
# AUTHOR:
#  Roger Meadows
#
# CREATION DATE:
#  8/9/2012
#
#*******************************************************************************

import os
import inspect
import sys
import shutil
import shlex
import pprint
import logging
import cmd

def parse_args():
    from optparse import OptionParser

    usage = "./%prog [options] [arguments]"
    description =('''This script is <blah blah blah> ''')

    epilog = "Example: python %s <example argument>" % os.path.basename(sys.argv[0])

    parser = OptionParser(usage=usage, version="%prog:  0.1", description=description, epilog=epilog)

    parser_conf = (
                    [
                      (('-f', '--full'),    'full',    False, 'store_true', 
                          'Return full path'),
                      (('-l', '--log'),    'log_level',   '', 'store', 
                          'Return full path'),
                      (('-v', '--verbose'), 'verbose', False, 'store_true', 'Print (more) debug info to screen.'),
                    ]
                  )

    for option, dest, default, action, help in parser_conf:
        if type(option) is str:
            parser.add_option(option, dest = dest, action = action, default = default, help = help)
        else:
            parser.add_option(option[0], option[1], dest = dest, action = action, default = default, help = help)

    return parser.parse_args()

#******************************************************************************
def function(target, callback=None, verbose=False):
    pass


#******************************************************************************
class MyInterpreter(cmd.Cmd):
    intro = 'Welcome to a command line interpreter template. Type ? to list commands.\n'
    prompt = '(mypromt) '

    def do_cmd1(self, arg):
        cmd1(arg)

    def do_cmd2(self, arg):
        cmd2(*parse(arg))

    def do_exit(self, arg):
        self.close()

    def close(self):
        print 'closing'

    def postcmd(self, stop, line):
        print 'postcmd: stop=%s, line=%s' % (str(stop), line)
        if line == 'exit':
            return True
        else:
            return False

def parse(arg):
    print 'parse: %s --> %s' % (arg, str(arg.split()))
    return arg.split()

def cmd1(arg):
    print 'cmd1(%s): called.' % arg

def cmd2(a1, a2, a3):
    print 'cmd2(%s,%s,%s): called.' % (a1, a2, a3)


###############################################################################
###############################################################################
if __name__ == '__main__':

    # =========================================================================
    # Parse command-line arguments
    # =========================================================================
    (opts, args) = parse_args()

    if opts.log_level == '':
        opts.log_level = 'INFO'
    numeric_level = getattr(logging, opts.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        print 'ERROR: Invalid log level %s' % opts.log_level
    logging.basicConfig(filename='default.log', filemode='a', level=numeric_level, 
            format='%(asctime)s %(levelname)s %(message)s')

    script_name = inspect.getfile(inspect.currentframe())
    logging.info('%s: starting' % script_name)
    exit_code = 0

    MyInterpreter().cmdloop()

    logging.info('%s: exiting with exit code = %d' % (script_name, exit_code))
    sys.exit(exit_code)

