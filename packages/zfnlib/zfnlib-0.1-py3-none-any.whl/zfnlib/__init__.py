from pwn import *
from pipe import *

@Pipe
def to_list(iterable):
    return list(iterable)