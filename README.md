
# Microservice Alternative Pipe


## Can the non-blocking communication be implemented with Linux PIPE to embody the concept of Micro Service?

When trying to build a machine learning API, it is often offered at a small efficiency and PoC level. If you do not want to wrap it in http (s) and make it REST, if it works on Linux, is PIPE good? ?

One of the difficulties especially when designing APIs for machine learning is that the APIs for models and data are quite large in image size. It's not as lightweight as a typical web service API built with golang, so it can be difficult or difficult to communicate with infrastructure people through regular API practices.

If you're trying to adapt to http microservices so far, why not do something similar with PIPE?

## Is it possible to do something like REST with PIPE in the first place?
Although it is possible to conclude from the conclusion, various ingenuity is required.

The good thing about microservices APIs is that there are REST rules to manage the state through communication and to handle them beautifully. You can do something good if you keep this, but this practice does not extend to the Linux PIPE concept.

In many cases, PIPE itself is often realized by independently moving each IO in the order of input-> output, and is often not based on the idea of ​​outputting one output immediately according to one input is. (Some hacks exist)


## the knowledge required to PIPE in Python

### subprocess.Popen and PIPE
In Python, you can launch various programs from Python and handle them.

By specifying subprocess.PIPE for the input and output of the started program, it is possible to communicate with the started Python

For example, in the following example, grep is started from Python, and the data of a, b, c, d is input, and only the data of a specific condition is filtered.

```python
from subprocess import Popen
from subprocess import PIPE
inputs = '''
a,10
b,20
c,30
'''
with Popen(['grep', 'b'], stdin=PIPE, stdout=PIPE) as proc:
    with proc.stdin as stdin:
        stdin.write(bytes(inputs+'\n', 'utf8'))
    with proc.stdout as stdout:
        print(stdout.read().decode('utf8').strip())
```

This output looks like this

```console
$ python3 sample01.py 
b,20
```

### Problems of STDIN, STDOUT, STDERR of Python
STDIN, STDOUT, etc. are expected to work synchronously in Python, and ordinary simple code cannot read and write at the same time.

I wrote it with asyncio with Python 3.7.4, but it seems that the behavior such as blocking may not be reproducible, and PIPE support does not seem to be enough yet.

There is often such a drawing in the example in PIPE, and it looks as if it can communicate in both directions, but it is incorrect.... 

<div align="center">
    <img width="500px" src="https://www.dropbox.com/s/xuyi81julg0ezv2/pip.png?raw=1">
    <div> Fig 1. common PIPE description </div>
</div>


In practice, blocking can occur (but most often) after writing in `proc.stdin`, and this is what this looks like.

<div align="center">
    <img width="100%" src="https://www.dropbox.com/s/0zqta0r0z4pquxj/pipe2.png?raw=1">
    <div> Fig 2. Actual </div>
</div>


To solve this problem, you need to write a little special.

### Handle STDIN and STDOUT asynchronously

Introducing code that performs two-way operations of reading and writing asynchronously for a child process started from the parent process Python by using the Python `os` library

```python
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
        os.sync()
        time.sleep(0.5)

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
```

What I am doing is that both need to run both to read and write stdin and stdout asynchronously, so the thread and multiprocessing libraries operate the write function and the read function, respectively. The function is invoked in parallel in the main statement.
At this time, take out the file descriptor of this pipe, as in `proc.stdin.fileno ()`, `proc.stdout.fileno ()`, and read and write with `os.write`,` os.read` And can work asynchronously.

In this example, PyTorch models that have been trained to break the code are thrown into a docker machine learning interface that has the function of inferring and breaking the code as one line, one data.

The decrypted data comes back over multiple lines.

<div align="center">
    <img width="500px" src="https://www.dropbox.com/s/i1jj67tcfktxh23/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202020-01-09%2023.12.15.png?raw=1">
    <div> Fig 3. Ciphertext used for input </div>
</div>


<div align="center">
    <img width="100%" src="https://www.dropbox.com/s/4tcqdrcp6e0kjoa/ezgif-6-6b89fe6a2013.gif?raw=1">
    <div> Fig 4. Entering a ciphertext interactively and solving it </div>
</div>
