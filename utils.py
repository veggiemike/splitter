"""utils -
convenience routines for splitter
"""

import os
import os.path

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
