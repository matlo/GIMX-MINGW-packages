# License: GPLv3

# This tool is supposed to send a sequence of set report and get report commands
# that appears to be a challenge-response authentication
# if successful, the final get_report should be populated with the response bytes
# By Frank Zhao, http://eleccelerator.com/
# You may need to install a filter driver before libusb can access the device, use "install-filter-win.exe" from libusb-win32

# Modified by Matlo, http://gimx.fr
# The size of the challenge (0xf0 reports) and response (0xf1 reports) packets must be 64 bytes (the last 4 bytes are the CRC32 of the first 60).
# The response is ready when the third byte of the 0xf2 report changes from 0x10 to 0x00.
# Get report 0x02 and set report 0x03 do not seem to be necessary.
# On linux the kernel driver has to be detached.

import sys, time, getopt, select
import usb.core, usb.util
from netaddr import *

def main(argv):
    verbose = True
    interface = 0

    try:
       opts, args = getopt.getopt(argv,"hvra:",[])
    except getopt.GetoptError:
        print 'Error: GetoptError'
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt in ("-v"):
            verbose = True

    if verbose:
        print 'Searching for USB device with VID 0x054C and PID 0x05C4'

    dev = usb.core.find(idVendor = 0x054C, idProduct = 0x05C4)
    if dev == None or dev == False or dev == 0:
        print 'Unable to find DualShock 4'
        print 'You may need to install a filter driver before libusb can access the device, use "install-filter-win.exe" from libusb-win32'
        quit()

    if verbose:
        print 'Found DualShock 4 in USB port'

    if sys.platform == 'linux2':
        if dev.is_kernel_driver_active(interface):
            dev.detach_kernel_driver(interface)
            if verbose:
                print 'USB device detach kernel driver'

    dev.set_configuration()
    if verbose:
        print 'USB device set configuration'

    usb.util.claim_interface(dev, interface)
    if verbose:
        print 'USB device claim interface'

#    if verbose:
#        print 'About to get report 0x02'
#    try:
#        repId = 0x0302
#        repLen = 0x26
#        msg = dev.ctrl_transfer(0xA1, 0x01, repId, 0x0000, repLen)
#        print 'Read report 0x02: ', len(msg), ', : [ ', printHexArray(msg), ']'
#    except:
#        print "Unexpected error:", sys.exc_info()[0]

    challenge1 = [ 0xf0, 0x01, 0x00, 0x00, 0x5f, 0x3b, 0x74, 0x00, 0xc0, 0xa0, 0xc4, 0xd5, 0xfe, 0x05, 0x17, 0x5a, 0x02, 0x41, 0xf2, 0xf3, 0x73, 0x4f, 0x88, 0x76, 0x56, 0xa5, 0xf4, 0x1e, 0xac, 0xc1, 0x29, 0x92, 0xbc, 0xa7, 0x3d, 0x80, 0xfc, 0x9c, 0x97, 0xf0, 0x56, 0xa5, 0x4f, 0xab, 0x5b, 0x44, 0xf7, 0x8d, 0xbd, 0xb6, 0x7d, 0x4b, 0x40, 0xca, 0x49, 0xd3, 0x85, 0xf7, 0xba, 0xff, 0x6b, 0xb0, 0x73, 0x41 ]

    challenge2 = [ 0xf0, 0x01, 0x01, 0x00, 0x21, 0x6b, 0x0d, 0x0d, 0x8d, 0x6f, 0x82, 0x2c, 0x48, 0x56, 0x79, 0xa7, 0x97, 0x0c, 0xf7, 0x1e, 0xc1, 0xab, 0xec, 0x19, 0x45, 0x3a, 0xbc, 0x95, 0x08, 0x4d, 0x43, 0x77, 0xf6, 0xdc, 0x43, 0x1c, 0x88, 0x26, 0x82, 0x35, 0x7b, 0xbf, 0xeb, 0xbb, 0x87, 0xd2, 0x1e, 0x40, 0xcd, 0x27, 0xed, 0xbf, 0x5c, 0xea, 0x8c, 0xea, 0x5c, 0xbe, 0x94, 0x81, 0xe4, 0x49, 0xdc, 0x18 ]

    challenge3 = [ 0xf0, 0x01, 0x02, 0x00, 0x74, 0xb0, 0xd1, 0x28, 0x49, 0xb4, 0x62, 0x5d, 0x7c, 0x64, 0xa3, 0x21, 0xaa, 0xbc, 0xee, 0x10, 0x9f, 0x64, 0xe2, 0xa6, 0xa9, 0xd2, 0xf7, 0xbe, 0x9d, 0x77, 0x4d, 0x1f, 0x79, 0xca, 0xf4, 0x8e, 0xaa, 0x8f, 0x91, 0x4e, 0x76, 0x85, 0x94, 0x0a, 0x45, 0xbd, 0x05, 0x22, 0x5c, 0x6d, 0xcf, 0x8f, 0x5f, 0x0a, 0xaf, 0x97, 0x1f, 0xdd, 0x7f, 0x2a, 0xdd, 0x7c, 0xc0, 0x61 ]

    challenge4 = [ 0xf0, 0x01, 0x03, 0x00, 0xe7, 0x2e, 0xe9, 0xe2, 0xa8, 0x8d, 0x98, 0xa3, 0x81, 0xe7, 0x3a, 0xe5, 0xdc, 0x02, 0x2d, 0xa0, 0xad, 0x2e, 0xbd, 0x15, 0x4d, 0x16, 0x45, 0x76, 0x99, 0x2d, 0x81, 0xac, 0x3e, 0xb9, 0xd6, 0x38, 0xd8, 0xb3, 0x25, 0x2d, 0x9e, 0x8b, 0xdc, 0x73, 0x06, 0xa8, 0xc2, 0xc1, 0x27, 0x6d, 0x18, 0xec, 0x19, 0xe4, 0xca, 0x50, 0xd7, 0x19, 0x38, 0x6c, 0xc2, 0x01, 0x16, 0xbd ]

    challenge5 = [ 0xf0, 0x01, 0x04, 0x00, 0x49, 0xb1, 0x03, 0xfd, 0x06, 0x7d, 0x2f, 0x6f, 0xe6, 0x4e, 0x55, 0x6d, 0xe2, 0x9e, 0x68, 0x3a, 0x9b, 0x90, 0xd9, 0x7a, 0x79, 0x6c, 0x16, 0x66, 0x01, 0xd3, 0x95, 0x4f, 0xaf, 0xc5, 0x2f, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaa, 0xd0, 0xc0, 0x1a ]

    repId = 0x03F0

    try:
        if verbose:
            print 'About to send challenge 1'
        ret = dev.ctrl_transfer(0x21, 0x09, repId, 0x0000, challenge1)
        if verbose:
            print 'Sent challenge 1, ret = ', ret
    except:
        print "Unexpected error:", sys.exc_info()[0]

    try:
        if verbose:
            print 'About to send challenge 2'
        ret = dev.ctrl_transfer(0x21, 0x09, repId, 0x0000, challenge2)
        if verbose:
            print 'Sent challenge 2, ret = ', ret
    except:
        print "Unexpected error:", sys.exc_info()[0]

    try:
        if verbose:
            print 'About to send challenge 3'
        ret = dev.ctrl_transfer(0x21, 0x09, repId, 0x0000, challenge3)
        if verbose:
            print 'Sent challenge 3, ret = ', ret
    except:
        print "Unexpected error:", sys.exc_info()[0]

    try:
        if verbose:
            print 'About to send challenge 4'
        ret = dev.ctrl_transfer(0x21, 0x09, repId, 0x0000, challenge4)
        if verbose:
            print 'Sent challenge 4, ret = ', ret
    except:
        print "Unexpected error:", sys.exc_info()[0]

    try:
        if verbose:
            print 'About to send challenge 5'
        ret = dev.ctrl_transfer(0x21, 0x09, repId, 0x0000, challenge5)
        if verbose:
            print 'Sent challenge 5, ret = ', ret
    except:
        print "Unexpected error:", sys.exc_info()[0]

#    time.sleep(2)

#    rep03 = [ 0x03, 0x02, 0x00, 0x22, 0x63, 0x1a, 0x50, 0x12, 0x12, 0xd0, 0x8c, 0x84, 0x96, 0x19, 0xee, 0x15, 0x6e, 0xa0, 0x24, 0x0f, 0xb0, 0x1e, 0xb7, 0xf7, 0xcc, 0xc8, 0xbf, 0x8a, 0x88, 0xf6, 0xb4, 0xd0, 0x32, 0x8d, 0x27, ]
#    repId = 0x0303
#    try:
#        if verbose:
#            print 'About to send set report 0x03'
#        ret = dev.ctrl_transfer(0x21, 0x09, repId, 0x0000, rep03)
#        if verbose:
#            print 'Sent set report 0x03, ret = ', ret
#    except:
#        print "Unexpected error:", sys.exc_info()[0]

#    time.sleep(2)

    ready = False

    while ready == False:
        if verbose:
            print 'About to get report 0xF2'
        try:
            repId = 0x03F2
            repLen = 16
            msg = dev.ctrl_transfer(0xA1, 0x01, repId, 0x0000, repLen)
            print 'Read report 0xF2: ', len(msg), ', : [ ', printHexArray(msg), ']'
            if 	msg[2] == 0x00:
                ready = True
            else:
                time.sleep(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]

    for respCnt in range(0, 0x13):
        if verbose:
            print 'About to read response ', '0x' + format(respCnt, '02x')
        try:
            repId = 0x03F1
            repLen = 64
            msg = dev.ctrl_transfer(0xA1, 0x01, repId, 0x0000, repLen)
            print 'Read response: ', len(msg), ', : [ ', printHexArray(msg), ']'
        except:
            print "Unexpected error:", sys.exc_info()[0]


    usb.util.release_interface(dev, interface)
    if verbose:
        print 'USB device release interface'

    if sys.platform == 'linux2':
        dev.attach_kernel_driver(0)
        if verbose:
            print 'USB device attach kernel driver'

    if verbose:
        print 'That\'s all this tool will do, goodbye'
        quit()

def printHexArray(arr):
    str = ''
    for i in range(0, len(arr)):
        str = str + '0x' + format(arr[i], '02x') + ', '
    return str

def printHelp():
    print 'command line options:'
    print '-h'
    print '    will print the help'
    print ''
    print '-v'
    print '    will enable verbose output'
    print ''
    print 'By Frank Zhao'

if __name__ == "__main__":
    main(sys.argv[1:])
