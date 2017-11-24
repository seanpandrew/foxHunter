from scapy.all import *
import scapyEssentials as SE

class Main(object):
    """Handles Main logging aspect"""

    def __init__(self, dbInstance, unity):
        self.unity = unity
        self.cap = dbInstance
        self.cap.db.execute('CREATE TABLE IF NOT EXISTS\
                                deauths(pid INTEGER,\
                                epoch INTEGER,\
                                date TEXT,\
                                time TEXT,\
                                addr1 TEXT,\
                                addr2 TEXT,\
                                addr3 TEXT,\
                                reason TEXT,\
                                rssi INTEGER,\
                                channel INTEGER,\
                                frequency INTEGER)')

    def aFinder(self):
        """Listen for and notate when deauth is found"""
        def snarf(packet):
            if packet.haslayer(Dot11Deauth):
                return True
            else:
                return
        return snarf


    def macFound(self, packet):

        self.trigger(packet)

    def trigger(self, packet):
        """Trigger mechanism for main entries"""
        notDecoded = hexstr(str(packet.notdecoded), onlyhex = 1).split(' ')
        try:
            fChannel = SE.chanFreq.twoFour(int(notDecoded[self.unity.offset] + notDecoded[self.unity.offset - 1], 16))
        except:
            fChannel = 'Unknown'
        try:
            fFreq = int(notDecoded[self.unity.offset] + notDecoded[self.unity.offset - 1], 16)
        except:
            fFreq = 'Unknown'
        try:
            fSig = -(256 - int(notDecoded[self.unity.offset + 3], 16))
        except IndexError:
            fSig = 'Unknown'
        reason = SE.conv.symString(packet[Dot11Deauth], 'reason')
        print 'Deauthentication Detected! -- %s -- %s' % (fSig, reason)

        ## Values for DB entry
        epoch, lDate, lTime = self.unity.times()
        count = self.unity.logDict.get('total')
        
        ## DB entry
        self.cap.db.execute('INSERT INTO deauths VALUES(?,\
                                                        ?,\
                                                        ?,\
                                                        ?,\
                                                        ?,\
                                                        ?,\
                                                        ?,\
                                                        ?,\
                                                        ?,\
                                                        ?,\
                                                        ?);',\
                                                            (count,\
                                                             epoch,\
                                                             lDate,\
                                                             lTime,\
                                                             packet.addr1,\
                                                             packet.addr2,\
                                                             packet.addr3,\
                                                             reason,\
                                                             fSig,\
                                                             fChannel,\
                                                             fFreq))
        self.cap.con.commit()
        self.unity.logDict.update({'total': count + 1})
