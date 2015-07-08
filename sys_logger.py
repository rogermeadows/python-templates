#!/usr/bin/env python
"""
A standard logging interface that writes to syslog.

File: sys_logger.py
"""

DARWIN = 'Darwin'
LINUX = 'Linux'

import logging
import platform
from logging.handlers import SysLogHandler


def get_sys_logger(log_id):
    """ return a python logger that writes to syslog """
    sys_log = logging.getLogger(log_id)
    sys_log.setLevel(logging.DEBUG)
    if platform.system() == LINUX:
        handler = SysLogHandler(address='/dev/log')
    elif platform.system() == DARWIN:
        handler = SysLogHandler(facility=SysLogHandler.LOG_DAEMON)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    sys_log.addHandler(handler)
    return sys_log
