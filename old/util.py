#!/usr/bin/env python

''' <about this module> '''

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
#  walk_topdown.py
#
# DESCRIPTION:
#  This script finds files in a local Mercurial repository working copy
#  ignoring all files in the .hg directory.
#
# AUTHOR:
#  Roger Meadows
#
# CREATION DATE:
#  6/20/2012
#
#*******************************************************************************

import os
import sys
import shutil
import shlex
import pprint

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


###############################################################################
###############################################################################
if __name__ == '__main__':

    # =========================================================================
    # Parse command-line arguments
    # =========================================================================
    (opts, args) = parse_args()

    exit_code = 0

    sys.exit(exit_code)
