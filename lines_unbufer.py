#!/usr/bin/env python3

'''
There is problem read in pipe lines, shich is not terminated by newline.
E.g.:
openvpn3 log --log-level 6 --config-events --config gid-vpn-plalexeev-3.ovpn 2>&1
frequently stuck with:
+00:00:00.000078 27-10:54:47.220714 2023-02-27 10:54:47 [STATUS] Connection, Client authentication failed: Authentication failed

So, we need to catch last line pattern even if there is not following strings

Implementation by https://stackoverflow.com/questions/10756383/timeout-on-subprocess-readline-in-python/34114767#34114767
'''

import asyncio
import sys
from asyncio.subprocess import PIPE, STDOUT


async def run_command(*args, timeout=None):
    # Start child process
    process = await asyncio.create_subprocess_exec(*args, stdout=PIPE, stderr=STDOUT)

    # Read line (sequence of bytes ending with b'\n') asynchronously
    while True:
        try:
            line = (await asyncio.wait_for(process.stdout.readline(), timeout)).decode().strip()
        except asyncio.TimeoutError: # Read all present buffer as is
            line = (await process.stdout.read(10)).decode()
            print(f'Timeout; line={line}')
        else:
            if not line: # EOF
                break
            print(f'line={line}')
    return await process.wait() # Wait for the child process to exit


if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop() # For subprocess' pipes on Windows
    asyncio.set_event_loop(loop)
else:
#    loop = asyncio.get_event_loop()
    # Python 3.11 fix (see https://stackoverflow.com/a/73367187/307525):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

#returncode = loop.run_until_complete(run_command("./test1", timeout=2))
print(f'Arguments to start: {sys.argv}')
returncode = loop.run_until_complete(run_command(*sys.argv[1:], timeout=2))
loop.close()
