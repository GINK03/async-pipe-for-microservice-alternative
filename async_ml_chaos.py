#!/usr/bin/env python3
import time
from subprocess import Popen
from subprocess import PIPE
from concurrent.futures import ProcessPoolExecutor as PPE
from concurrent.futures import ThreadPoolExecutor as TPE
import sys
import os

def reader(fd):
    tmp = b''
    while True:
        bc = os.read(fd, 1)
        if not bc:
            break
        if bc != bytes('\n', 'utf8'):
            tmp += bc
        else:
            print('scanned', tmp.decode('utf8').strip(), end='\n', flush=True)
            tmp = b''

def writer(fd):
    crypt_shakespear = open('./crypt_shakespear.txt').read()
    for i in range(0, len(crypt_shakespear), 128):
        for ch in crypt_shakespear[i:i+128]:
            os.write(fd, bytes(ch, 'utf8'))
        os.write(fd, bytes('\n', 'utf8'))
        #print('input', crypt_shakespear[i:i+128])
        os.sync()
        time.sleep(0.1)

def driver(arg):
    func, fd = arg
    r = func(fd)
    return r

def main():
    proc = Popen(['docker', 'run', '-i', 'pipe_api'],
               stdin=PIPE,
               stdout=PIPE)
    stdout = proc.stdout
    stdin = proc.stdin
    
    with PPE(max_workers=16) as exe:
        for r in exe.map(driver, [(writer, stdin.fileno()), (reader, stdout.fileno())]):
            r
        stdin.close()    
main()
