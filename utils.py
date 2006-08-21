"""utils -
convenience routines for splitter
"""

import os
import os.path
import stat

import config


def vprint(list):
    """vprint(list)
    takes a list of args to be printed if VERBOSE == 1
    """
    if not config.VERBOSE:
        return
    
    print list


def translate_size(bytes):
    """translate_size(bytes)
    returns human readable size (e.g., 1K, 234M, 2G)
    """
    factor_list = ["", "K", "M", "G", "T"]
    f = 0
    base = bytes
    #print "%d bytes" % bytes
    while base >= 2**10 and f < len(factor_list) - 1:
        base = base / 2**10
        f += 1
    if f > 0:
        rem = bytes % (2**10)**f
        #print "%d%s, %d bytes" % (base, factor_list[f], rem)
        rem_percent = float(rem) / (2**10)**f
        #print "%d is %f%% of 1%s" % (rem, rem_percent, factor_list[f])
        retval = "%.1f%s" % (base + rem_percent, factor_list[f])
    else:
        #print "%d bytes" % base
        retval = "%d" % base
    return retval


def round_to_nearest(num, mult):
    """round_to_nearest(num, mult)
    returns num rounded to the nearest multiple of mult
    """
    r = num % mult
    if r != 0:
        return num + mult - r
    return num


def get_size_in_tar(filename):
    """get_size_in_tar(filename)
    returns the number of bytes taken up by filename in a tar file.
    """
    # each file starts with a 512 byte header
    s = 512

    stats = os.lstat(filename)
    
    if not stat.S_ISREG(stats[stat.ST_MODE]):
        # only regular files have data stored in tar files.  symlinks,
        # directories, pipes/fifos, sockets, character special, and block
        # special files just get a 512 byte header
        return s

    # add in the size of the file on disk
    s += stats[stat.ST_SIZE]
    
    # now round it up to nearest mult of 512
    #if s % 512 != 0:
    #    s += 512 - (s % 512)
    s = round_to_nearest(s, 512)

    return s


def get_size_of_tar(size):
    """get_size_of_tar(size)
    tar files are typically written in chunks of 20 blocks.  this means that
    the size of a tar file ends up being rounded up to the nearest multiple of
    10240
    """
    # N blocks get written at once.  Default is 20
    N = 20

    # block size is 512 bytes
    bs = 512

    chunk = N * bs

    #retval = size
    
    #if retval % chunk != 0:
    #    retval += chunk - (retval % chunk)

    return round_to_nearest(size, chunk)
