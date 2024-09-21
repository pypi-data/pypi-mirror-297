"""
Python Bash Script Helper Utilties

Shell commands require *nix with bash shell'/bin/bash'
"""
import sys, os, time
import subprocess as sp
from typing import Union, Tuple
from threading import Thread

# handy constants for formatting strings
SP = ' '
TAB2 = SP * 2
TAB = TAB4 = SP * 4
LF = '\n'
CRLF = '\r\n'

class Shell:
    '''Override Shell.shell if required
    
    Shell.shell = '/bin/bash' (default)
    '''
    shell = '/bin/bash'


def joinlines(lines:list) -> str:
    """Join lines in list with line feeds
    
    This is the inverse of str.splitlines()
    """
    return LF.join(lines)
    

def arg(n:int) -> str:
    """Retrieve command line arg by index

    Args:
        n (int): arg index

    Returns:
        str: arg value or null string
    """
    return sys.argv[n] if len(sys.argv) >= n+1 else ''

def nargs(n:int) -> list:
    """Retrieve remaining command line args starting at index

    Args:
        n (int): beginning arg index

    Returns:
        list: arg values or []
    """
    return sys.argv[n:]


def shift(n:int=1) -> str:
    """Shift command line args by n, preserving sys.argv[0]

    Args:
        n (int): number of args to remove from sys.argv
    
    Returns: list of args removed
    """
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    removed = args[:n]
    
    sys.argv = [sys.argv[0]] + args[n:]
    
    return removed
        
def exit(return_code:int=0):
    """Ext the script with return code

    Args:
        code (int, optional): return code. Defaults to 0.
    """
    sys.exit(return_code)


def env(var:str) -> str:
    """Retrieve OS environment variable by name

    Args:
        var (str): Env variable name

    Returns:
        str: Env variable value or null string
    """
    return os.environ.get(var, '')

def kill(pid:int, signal:int=9):
    """Kill the process for this pid

    Args:
        pid (int): process-id to kill
        signal (int, optional): signal used to kill the process. Defaults to 9.
    """
    os.kill(pid, signal)
    

def sh(cmd:str, shell=Shell.shell, **kwargs) -> str:
    """Return captured result from bash shell command as stripped stdout+stderr

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        str: stripped stdout + stderr
    """
    cp = sp.run(cmd, shell=True, executable=shell, 
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    result = cp.stdout + cp.stderr
    return result.strip()

def shl(cmd:str, shell=Shell.shell, **kwargs) -> Tuple[int, str, str]:
    """Return list from bash shell command as [returncode, stdout, stderr]

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        int: returncode
        str: stdout (raw)
        str: stderr (raw)
    """
    cp = sp.run(cmd, shell=True, executable=shell, 
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    return cp.returncode, cp.stdout, cp.stderr

def shk(cmd:str, shell=Shell.shell, **kwargs) -> Tuple[bool, int, str, str]:
    """Return list from bash shell command as [is_ok, returncode, stdout, stderr]

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        bool: is_ok: True if returncode == 0
        int: returncode
        str: stdout (raw)
        str: stderr (raw)
    """
    cp = sp.run(cmd, shell=True, executable=shell,  
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    is_ok = cp.returncode == 0
    return is_ok, cp.returncode, cp.stdout, cp.stderr

def sho(cmd:str, shell=Shell.shell, **kwargs) -> sp.CompletedProcess:
    """Return CompletedProcess object from bash shell command

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        CompletedProcess object:
        - cp.is_ok: True if cp.rc == 0
        - cp.rc or cp.returncode
        - cp.stdout
        - cp.stderr
    """
    cp = sp.run(cmd, shell=True, executable=shell, 
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    # set alias cp.rc and cp.is_ok
    cp.rc = cp.returncode
    cp.is_ok = cp.returncode == 0
    return cp

def shx(cmd:str, shell=Shell.shell, **kwargs) -> None:
    """Run command via bash shell with no return but real-time results spill to the terminal

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()
    """
    # let the command run and spill to the screen
    sp.run(cmd, shell=True, executable=shell, **kwargs)
    return None

def shb(cmd:str, shell=Shell.shell, **kwargs) -> int:
    """Run command via bash shell in the background returning the pid
    
    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.Popen()
    """
    # run this command in bash in the background returning the pid
    p = sp.Popen(cmd, shell=True, executable=shell, close_fds=True, **kwargs)
    return p.pid

def shp(cmd:str, shell=Shell.shell, **kwargs) -> sp.Popen:
    """Run command via bash shell in the background, returning a Popen object
    
    Args:
        cmd (str): Command string
        shell (str): shell to use, default is Shell.shell
        **kwargs: additional args for subprocess.Popen()

    Returns:
        Popen object:
        - p.pid
        - p.stdout
        - p.stderr
    """
    return sp.Popen(cmd, shell=True, executable=shell, text=True, 
                    stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)


class BackgroundProcess:
    def __init__(self, cmd: str, shell=Shell.shell, **kwargs):
        """Run command via bash shell in the background, creating a BackgroundProcess object.
        
        Args:
            cmd (str): Command string
            **kwargs: additional args for subprocess.Popen()
        """
        self.proc = sp.Popen(cmd, shell=True, executable=shell, text=True, 
                             stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
        self.thread = None
        self.stdout = []

    def get_stdout(self, sentinel: str | None = None) -> None:
        """Reads stdout from the background process in a separate thread.
        - Optionally, thread returns immediately when a specific sentinel string is found.
        
        Args:
            sentinel (str|None): sentinel string or None for no sentinel

        Returns: None -- thread runs in background reading stdout and appending to self.stdout
        """
        def read_stdout():
            '''Read stdout from the process and optionally wait for a sentinel string
            - Appends lines to self.stdout
            - Exits loop early when sentinel string is found
            '''
            for line in iter(self.proc.stdout.readline, ''):
                self.stdout.append(line)
                if sentinel and sentinel in line:
                    break
        
        self.stdout = []
        self.thread = Thread(target=read_stdout)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(.1)  # allow thread to start
        return None

    def join_stdout(self, timeout: int | None = None) -> str:
        """Joins the thread and terminates the process returning the stdout string
        
        Args:
            timeout (int|None): timeout in seconds or block for no timeout

        Returns:
            str: stdout
        """
        if self.thread:
            self.thread.join(timeout=timeout)  # Wait for up to N seconds or block until thread completes
        stdout_str = ''.join(self.stdout)  # join the stdout lines into a single string
        self.proc.terminate()
        return stdout_str


def shbg(cmd: str, shell=Shell.shell, **kwargs) -> BackgroundProcess:
    """Run command via bash shell in the background, returning a BackgroundProcess object.
    - See Usage below
    
    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.Popen()
    
    Returns:
        BackgroundProcess: object representing the background process
    
    Usage:
    ```python
        bg = shbg('echo -n "hello\\nfrom\\nbackground\\nprocess"; sleep 3')
        bg.get_stdout(sentinel='back') 
        print('waiting for sentinel ...')
        stdout = bg.join_stdout(timeout=1)
        print(stdout) 
    ```
    """
    return BackgroundProcess(cmd, shell, **kwargs)

def humanize(seconds:Union[int, float], style='compact', days='days', day='day', *, zerodays=True):
    """Format humanized elapsed seconds as
        - compact style: 'DD days HH:MM:SS'
        - full style: 'DDd HHh MMm SSs'

    Args:
        seconds (int|float): seconds to humanize -- float subseconds are truncated to int
        style (str):         'compact' => default compact format, 'full' => full format 
        days (str):          days label => default 'days' 
        day (str):           day label => default 'day' if DD == 1
        zerodays (bool):     show zero days in compact style => default True, False => suppress zero days

    Returns:
        str: human formatted string 'compact'=>`'05 days 03:59:27'` or 'full'=>`'05d 03h 59m 27s'`
    """
    # parse the seconds
    dd = int(seconds / 86400)
    hh = int(seconds % 86400 / 3600)
    mm = int(seconds % 3600 / 60)
    ss = int(seconds % 60)    

    if style == 'compact':
        days = day if dd == 1 else days
        dds = f'{dd:02d} {days} ' 
        if not zerodays and dd == 0:
            dds = ''
        return f'{dds}{hh:02d}:{mm:02d}:{ss:02d}'
    elif style == 'full':
        return f'{dd:02d}{days[0]} {hh:02d}h {mm:02d}m {ss:02d}s'
    else:
        return f'{seconds} seconds'
    

def test():
    import time
    sys.argv += ['arg1', 'arg2']
    print(f'{arg(1) = }  {arg(2) = }')
    print(f'{shift(1) = }  {arg(1) = }')
    print(f'{shift(2) = }  {arg(1) = }')
    
    print(f"{sh('ls') = }")
    print(f"{shl('ls') = }")
    print(f"{shk('ls') = }")
    
    cp = sho('ls')
    print(f"sho('ls'): {cp.args = } {cp.is_ok = } {cp.rc = }  {cp.stdout = }  {cp.stderr = }")

    cp = sho('ls xxx')
    print(f"sho('ls xxx'): {cp.args = } {cp.is_ok = } {cp.rc = }  {cp.stdout = }  {cp.stderr = }")

    print(f"shx(ls -alh)")
    shx('ls -alh')

    pid = shb('sleep 200')
    print(f"pid = shb('sleep 200'); {pid = }")
    time.sleep(1)
    print(f"{kill(pid) = }")

    print('test shbg()')
    bg = shbg('echo -n "hello\nfrom\nbackground\nprocess"; sleep 3')
    bg.get_stdout(sentinel='back') 
    print('waiting for sentinel ...')
    stdout = bg.join_stdout(timeout=3)
    print(stdout) 

    print()
    print(f"{humanize(time.time()) = }")
    print(f"{humanize(time.time(), 'full') = }")
    print(f"{humanize(time.time(), 'full', zerodays=False) = }")
    
    day = 24 * 60 * 60
    for dd in range(0,3):
        days = day*dd
        print(f"{humanize(days) = }")
        print(f"{humanize(days, zerodays=False) = }")
        print(f"{humanize(days, 'full') = }")
        print(f"{humanize(days, 'full', zerodays=False) = }")

    print('\nexit(1)')
    exit(1)
    
if __name__ == '__main__':
    test()
