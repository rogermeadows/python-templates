#!/usr/bin/env python  
import sys, os, time, atexit
import argparse
import logging

from signal import SIGTERM

from bottle import route, run


HOST = '0.0.0.0'
PORT = 4001

class ServiceDaemon(object):
        """
        A generic daemon class.

        Usage: subclass the ServiceDaemon class and override the run() method
        """
        def __init__(self, name, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
            self.stdin = stdin
            self.stdout = stdout
            self.stderr = stderr
            self.pidfile = pidfile
            self.name = name

        def daemonize(self):
            """
            do the UNIX double-fork magic, see Stevens' "Advanced
            Programming in the UNIX Environment" for details (ISBN 0201563177)
            http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
            """
            try:
                pid = os.fork()
                if pid > 0:
                    # exit first parent
                    sys.exit(0)
            except OSError, e:
                sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                sys.exit(1)

            # decouple from parent environment
            os.chdir("/")
            os.setsid()
            os.umask(0)

            # do second fork
            try:
                pid = os.fork()
                if pid > 0:
                    # exit from second parent
                    sys.exit(0)
            except OSError, e:
                sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                sys.exit(1)

            # redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            se = file(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            # write pidfile
            atexit.register(self.delpid)
            pid = str(os.getpid())
            file(self.pidfile,'w+').write("%s\n" % pid)

        def delpid(self):
            os.remove(self.pidfile)

        def start(self):
            """
            Start the daemon
            """
            # Check for a pidfile to see if the daemon already runs
            try:
                pf = file(self.pidfile,'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None

            if pid:
                message = "{}: already running?, pidfile {} already exists.\n".format(self.name, self.pidfile)
                sys.stderr.write(message)
                sys.exit(1)

            # Start the daemon
            print '{}: starting.'.format(self.name)                
            self.daemonize()
            self.run()

        def stop(self):
            """
            Stop the daemon
            """
            # Get the pid from the pidfile
            try:
                pf = file(self.pidfile,'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None

            if not pid:
                message = "pidfile %s does not exist. ServiceDaemon not running?\n"
                sys.stderr.write(message % self.pidfile)
                return # not an error in a restart

            # Try killing the daemon process       
            try:
                while 1:
                        os.kill(pid, SIGTERM)
                        time.sleep(0.1)
            except OSError, err:
                err = str(err)
                if err.find("No such process") > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    print str(err)
                    sys.exit(1)
            print '{}: stopped.'.format(self.name)                

        def restart(self):
            """
            Restart the daemon
            """
            self.stop()
            self.start()

        def running(self):
            try:
                pf = open(self.pidfile, 'r')
            except IOError:
                return False
            pf.close()
            return True
        
        def status(self):
            if not self.running():
                print '{}: is NOT running'.format(self.name)
                return False
            print '{}: is running'.format(self.name)
            return True
        
        def run(self):
            """
            You should override this method when you subclass ServiceDaemon. It will be called after the process has been
            daemonized by start() or restart().
            """

class ApiDaemon(ServiceDaemon):
    def __init__(self, name, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        super(ApiDaemon, self).__init__(name, pidfile, stdin=stdin, stdout=stdout, stderr=stderr)

    def run(self):
        super(ApiDaemon, self).run()
        run(host='0.0.0.0', port=4040, debug=True)

@route('/:serv/:ver/:res')
def handle_api(serv, ver, res):
    with open('/tmp/{}.log'.format(__file__), 'a') as calls:
        calls.write('/{}/{}/{} received.\n'.format(serv, ver, res))
    print 'received: /{}/{}/{}'.format(serv, ver, res)


@route('/:serv/:ver/:res/<rest:path>')
def handle_api(serv, ver, res, rest):
    with open('/tmp/{}.log'.format(__file__), 'a') as calls:
        calls.write('/{}/{}/{}/{} received.\n'.format(serv, ver, res, rest))
    print 'received: /{}/{}/{}/{}'.format(serv, ver, res, rest)


NAME = 'api_daemon'
PIDFILE = '/tmp/api_daemon.pidfile'
STDOUT = '/tmp/api_daemon.stdout'
STDERR = '/tmp/api_daemon.stderr'

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', help='command (start/stop/restart)')
    parser.add_argument('-i', '--host', help='the host to listen on', action='store', default=HOST)
    parser.add_argument('-p', '--port', help='the port to listen on', action='store', default=PORT)
    parser.add_argument('-v', '--verbose', help='print more information', action='store_true')
    parser.add_argument('-l', '--loglevel', help='set logging level', action='store')
    opts = parser.parse_args(argv)
    if opts.verbose:
        print 'verbose is turned on'
    if opts.loglevel == '' or opts.loglevel is None:
        opts.loglevel = 'INFO'

    #setup logging
    numeric_level = getattr(logging, opts.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        print '\nERROR: invalid loglevel specified: {}\n'.format(opts.loglevel)
        return(1)
    logger = logging.getLogger(__file__)
    fh = logging.FileHandler('/tmp/{}.log'.format(__file__))
    fm = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(fm)
    logger.setLevel(numeric_level)
    logger.addHandler(fh)
    logger.info('{} starting, name={}, pidfile={}, stdin=/dev/null, stdout={}, stderr={}'.format(
        __file__, NAME, PIDFILE, STDOUT, STDERR))
    msg = 'loglevel = {}({:d}) for {}'.format(opts.loglevel, numeric_level,
        __file__)
    logger.info(msg)
    apid = ApiDaemon(NAME, PIDFILE, stdout=STDOUT, stderr=STDERR)
    if opts.cmd == 'start':
        apid.start()
    elif opts.cmd == 'stop':
        apid.stop()
    elif opts.cmd == 'restart':
        apid.restart()
    elif opts.cmd == 'status':
        apid.status()
    elif opts.cmd == 'fg':
        print 'starting in the foreground'
        run(host=opts.host, port=opts.port, debug=True)
    else:
        print '\nERROR: invalid command: {}\n'.format(opts.cmd)


if __name__ == '__main__':
    sys.exit(main())
