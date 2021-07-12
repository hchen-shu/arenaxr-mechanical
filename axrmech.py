import sys
import util

if sys.argv[1] == '--disassemble':
    util.makeParts(sys.argv[2])
elif sys.argv[1] == '--upload':
    util.uploadParts(sys.argv[2])
elif sys.argv[1] == '--activate':
    util.activateParts(sys.argv[2])
else:
    print('arguments other than "--disassemble", "--upload" or "--activate" are not supported')