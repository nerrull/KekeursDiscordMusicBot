import os
import random

def get_rand_file(base_uri):
    flist = list(os.scandir(base_uri))
    r = random.randrange(0, len(flist))
    return flist[r].path