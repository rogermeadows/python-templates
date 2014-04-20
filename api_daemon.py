import sys, os, time, atexit
import argparse
import logging

from signal import SIGTERM

from bottle import route, run

class Daemon(object):
        """
        A generic daemon class.

        Usage: subclass the Daemon class and override the run() method
        """
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile

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
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.pidfile)
                        sys.exit(1)

                # Start the daemon
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
                        message = "pidfile %s does not exist. Daemon not running?\n"
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

        def restart(self):
                """
                Restart the daemon
                """
                self.stop()
                self.start()

        def run(self):
                """
                You should override this method when you subclass Daemon. It will be called after the process has been
                daemonized by start() or restart().
                """

class ApiDaemon(Daemon):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        super(ApiDaemon, self).__init__(pidfile, stdin=stdin, stdout=stdout, stderr=stderr)

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


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', help='command (start/stop/restart)')
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
    print 'loglevel = {}({:d}) for {}'.format(opts.loglevel, numeric_level,
        __file__)
    logger.info('{} starting'.format(__file__))
    apid = ApiDaemon('/tmp/api_daemon_pid', stdout='/tmp/api_daemon.stdout', stderr='/tmp/api_daemon.stderr')
    if opts.cmd == 'start':
        apid.start()
    elif opts.cmd == 'stop':
        apid.stop()
    elif opts.cmd == 'restart':
        apid.restart()


if __name__ == '__main__':
    sys.exit(main())
