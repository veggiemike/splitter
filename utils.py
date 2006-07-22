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


def getsize(node):
    """getsize(node)
    returns the size in bytes of the provided fs node.  this version of getsize
    ignores symlinks and is recursive
    """
    #print "getsize(node=%s)" % (node)
    if os.path.islink(node):
        #print "** link **"
        return 0
    elif os.path.isdir(node):
        #print "** dir **"
        retval = 0
        for x in os.listdir(node):
            retval += getsize(os.path.join(node, x))
        retval += os.path.getsize(node)
        return retval
    else:
        #print "** file **"
        return os.path.getsize(node)


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
