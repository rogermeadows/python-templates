#!/usr/bin/env python
"""
Template for a python program that runs from command line and may process command line arguments
"""
import os
import sys


if __name__ == '__main__':
    DEFAULT_OUTPUT_FILENAME = "default.out"
    from optparse               import OptionParser

    # Parse command-line options
    usage = "%prog [options] argument-1 argument-2"

    parser = OptionParser(usage)

    parser.add_option('-o', '--output',
                      dest    = 'filename',
                      default = DEFAULT_OUTPUT_FILENAME,
                      help    = 'Specify the name of the output file (default: default.out)')

    parser.add_option('-v', '--verbose',
                      default = False,
                      action  = 'store_true',
                      dest    = 'verbose',
                      help    = 'Print more information.')

    parser.add_option('-d', '--dry-run',
                      default = False,
                      action  = 'store_true',
                      dest    = 'dry_run',
                      help    = 'Process input, but do not make any changes.')

    (options, args) = parser.parse_args()

    # check that both arguments are provided
    if len(args) < 2:
        parser.print_help()
        exit()
    # process the arguments and print arguments and options if verbose is true
    argument1 = args[0]
    argument2 = args[1]

    if options.verbose:
        print 'cmd_line_util_template.py (v0.1):'
        print '  options:'
        print '    (verbose              ) = %s' % ('true' if options.verbose else 'false')
        print '    (dry run              ) = %s' % ('true' if options.dry_run else 'false')
        print '    (output               ) = %s' % options.filename
        print '  arguments:'
        print '    (argument 1) = %s' % argument1
        print '    (argument 2) = %s' % argument2

    print "cmd_line_util_template.py: ending"

