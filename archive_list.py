class archive:
    """archive
    data type used by archive_list
    """
    def __init__(self):
        self.files = []
        self.size = 0
    
    
    def __str__(self):
        return "archive, %d files, %s" % (len(self.files),
                                          translate_size(self.size))
    
    
    def info(self):
        retval = []
        retval.append("--- archive ---")
        retval.append("files: %s" % self.files)
        retval.append("size: %s" % translate_size(self.size))
        retval.append("---------------")
        return string.join(retval, "\n")
        


class archive_list:
    """archive_list
    this class creates a list of archives no bigger than 'maxsize' from the
    provided 'node_list'.
    """
    def __init__(self, node_list, maxsize):
        self.node_list = node_list
        self.maxsize = maxsize
        self.list = [archive()]
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
            retval[-1] += ", %s remaining" % (translate_size(self.maxsize
                                                             - x.size))
        retval.append("------------------------")
        return string.join(retval, "\n")
    
    
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
        
        if os.path.islink(node):
            #print "** link **"
            self.list[-1].files.append(node)
            # don't increase size
            return
        elif os.path.isdir(node):
            #print "** dir **"
            for x in os.listdir(node):
                self.splitter(os.path.join(node, x))
        #else:
        #    print "** file **"
        
        s = os.path.getsize(node)
        #print "s: %d" % s
        if s > self.maxsize:
            print "WARNING: file bigger than maxsize: %s" % node
            return
        elif self.list[-1].size + s > self.maxsize:
            self.list.append(archive())
        self.list[-1].files.append(node)
        self.list[-1].size += s
