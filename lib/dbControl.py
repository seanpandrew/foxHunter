import logging, os, time
import sqlite3 as lite
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
#from parser import Names
from scapy.all import *

class Builder(object):
    """This class builds or adds on to a pre-existing sqlite3 database"""

    def __init__(self):
        
        ## Create Base directory
        self.bDir = os.getcwd()

        ## Declare the Logging directory
        self.dDir = raw_input('Logging Directory? [%s/logs]\n' % self.bDir)
        if not self.dDir:
            self.dDir = '%s/logs' % self.bDir
        else:
            print ''
        if not os.path.isdir(self.dDir):
            os.makedirs(self.dDir)

        ## Create directory list for dDir
        self.dList = os.listdir(self.dDir)

        ## Create DB
        tStamp = time.strftime('%Y%m%d_%H%M', time.localtime()) + '.sqlite'
        self.dbName = raw_input('Desired name for DB? [%s/%s]\n' % (self.dDir, tStamp))
        if not self.dbName:
            self.dbName = '%s/%s' % (self.dDir, tStamp)
        else:
            print ''

        ## Check to make sure we want to continue
        if os.path.isfile(self.dbName):
            self.dFile = raw_input('%s already exists\nUpdate and continue? [y/N]\n' % self.dbName)
            if not self.dFile:
                exit(1)
            elif self.dFile == 'n':
                exit(1)
            elif self.dFile == 'N':
                exit(1)
            else:
                print '\nUpdating %s and continuing' % self.dbName

        ## Build the DB if not already created
        print 'Proceeding to build %s\n' % self.dbName
        self.con = lite.connect(self.dbName)
        self.con.text_factory = str
        self.db = self.con.cursor()
