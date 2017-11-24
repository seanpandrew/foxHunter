#!/usr/bin/python

import argparse, logging, signal, sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import scapyEssentials as SE
from lib import dbControl
from lib import auth

def crtlC(cap, unity):
    """Handle CTRL+C."""
    def tmp(signal, frame):
        print '\n\nStopping gracefully'
        cap.con.commit()
        print '\nTotal packets logged:'
        for k, v in unity.logDict.items():
            print '%s -- %s\n' % (k, str(v - 1))
        sys.exit(0)
    return tmp


def main(args):
    ## Notate the environment
    iFace = sys.argv[1]
    
    ## Notate the driver in use
    if args.i is not None:
        iFace = args.i[0]
    if args.d is not None:
        iwDriver = args.d
    else:
        try:
            iwDriver = control.iwDriver()
        except:
            iwDriver = 'unknown'
        

    ## Setup Unity & main
    SEU = SE.Unify(iwDriver)
    SEU.logDict = {'total': 1}
    
    ## Instantiate the DB
    cap = dbControl.Builder()
    
    ## Handle interrupts
    signal_handler = crtlC(cap, SEU)
    signal.signal(signal.SIGINT, signal_handler)
    
    ## Run Main
    dCatch = auth.Main(cap, SEU) 
    
    ## Setup deauth filter
    pFilter = dCatch.aFinder()
    
    sniff(iface = iFace, prn = dCatch.trigger, lfilter = pFilter)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'foxHunter - DeAuth Finder',
                                     prog = 'foxHunter')
    parser.add_argument('-d',
                        choices = ['ath9k', 'ath9k_htc', 'rt2800usb', 'unknown', 'wl12xx'],
                        help = 'driver choice',
                        required = True)
    parser.add_argument('-i',
                        help = 'interface',
                        nargs = 1,
                        required = True)
    args = parser.parse_args()
    main(args)
