from subprocess import *

try:
    check_output
except NameError:

    def check_output(*popenargs, **kwargs):
        r"""Run command with arguments and return its output as a byte string.
        If the exit code was non-zero it raises a CalledProcessError.
        The arguments are the same as for the Popen constructor.  Example:
        >>> check_output(["ls", "-l", "/dev/null"])
        """
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = Popen(stdout=PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd, output=output)
        return output

    def check_call(*popenargs, **kwargs):
        """Run command with arguments.  Wait for command to complete.  If
        the exit code was zero then return, otherwise raise
        CalledProcessError.
        The arguments are the same as for the Popen constructor.  Example:
        check_call(["ls", "-l"])
        """
        retcode = call(*popenargs, **kwargs)
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd)
        return 0