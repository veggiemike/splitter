"""config-
internal configuration library for splitter
"""

import sys
import os
import os.path


#---------- compile-time configuration ---------------------------------------#

VERSION = "__VERSION__"
SIZE_LIMIT = __SIZE_LIMIT__
LIBDIR = "__LIBDIR__"
INDEX_FILE = os.path.join(LIBDIR, "__INDEX_FILE__")
NODE_LIST = __NODE_LIST__


#---------- run-time configuration -------------------------------------------#
VERBOSE=False
WAIT=0
