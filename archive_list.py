"""archive_list -
the workhorse of the Splitter Backup System
"""

import os
import os.path
import stat
import string
import tarfile

import config
import utils


class archive:
    """archive
    data type used by archive_list
    """
    def __init__(self, name):
        self.name = name
        self.files = []
        self.size = 0
    
    
    def __str__(self):
        return "archive '%s', %d files, %s" % (self.name,
                                               len(self.files),
                                               utils.translate_size(self.size))
    
    
    def info(self):
        retval = []
        retval.append("--- archive ---")
        retval.append("name: %s" % self.name)
        retval.append("files: %d" % len(self.files))
        retval.append("size: %s" % utils.translate_size(self.size))
        retval.append("listing:")
        for x in self.files:
            retval.append("  %s" % x)
        retval.append("---------------")
        return string.join(retval, "\n")


    def create(self):
        """create()
        this function actually creates the archive file on disk
        """
        if not os.path.isdir(config.WRITE_DIR):
            os.makedirs(config.WRITE_DIR)

        name = os.path.join(config.WRITE_DIR,
                            "splitter-%s.tar" % self.name)
        
        print "creating: %s" % name
        f = tarfile.open(name, "w")
        f.posix = False

        for x in self.files:
            utils.vprint("  adding: %s" % x)
            f.add(x, recursive=False)

        f.close()


class archive_list:
    """archive_list
    this class creates a list of archives no bigger than 'maxsize' from the
    provided 'node_list'.
    """
    def __init__(self, node_list, maxsize):
        self.node_list = node_list
        self.maxsize = maxsize
        self.list = [archive("1")]
        for x in node_list:
            self.splitter(x)
    
    
    def __str__(self):
        retval = []
        retval.append("----- archive_list -----")
        retval.append("node_list: %s" % self.node_list)
        retval.append("maxsize: %d bytes" % self.maxsize)
        retval.append("archives: %d" % len(self.list))
        for x in self.list:
            retval.append("%s" % x)
            retval[-1] += ", %s remaining" % (utils.translate_size(self.maxsize
                                                                   - x.size))
        retval.append("------------------------")
        return string.join(retval, "\n")
    

    def __getitem__(self, i):
        return self.list[i]

    
    def splitter(self, node):
        """splitter(node)
        this function traverses the provided filesystem node, adding
        encountered files to the current archive.  when it encounters a file
        that is bigger than 'maxsize', a warning message is displayed and the
        file is ignored.  also, files lacking read permission are ignored with
        a warning.  when it encounters a file that would make the archive
        bigger than 'maxsize', the current archive is finalized and a new
        archive is created.
        """
        #print "splitter(node=%s)" % (node)
        
        # check for read permission
        if not os.access(node, os.R_OK):
            print "WARNING: file not readable: %s" % node
            return
        
        if os.path.isdir(node):
            #print "** dir **"
            for x in os.listdir(node):
                self.splitter(os.path.join(node, x))

        # size in a tar file is actually:
        #  512 header + size, rounded up to nearest mult of 512
        s = 512
        s += os.lstat(node)[stat.ST_SIZE]
        s += 512 - (s % 512)
        #print "s: %d" % s
        if s > self.maxsize:
            print "WARNING: file bigger than maxsize: %s" % node
            return
        elif self.list[-1].size + s > self.maxsize:
            self.list.append(archive(int(self.list[-1].name) + 1))
        self.list[-1].files.append(node)
        self.list[-1].size += s


    def create(self):
        """create()
        this function iterates over the list of archives, calling the create()
        member function of each.  it waits, if necesary, according to the
        config.WAIT variable.
        """
        counter = config.WAIT
        for x in self.list:
            if counter == 0 != config.WAIT:
                raw_input("press Enter to continue...")
                counter = config.WAIT
            x.create()
            counter -= 1
