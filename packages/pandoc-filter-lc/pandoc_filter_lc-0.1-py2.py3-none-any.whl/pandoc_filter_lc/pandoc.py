

#!/usr/bin/python
from __future__ import print_function
import argparse

import utillc

__version__ = "0.1"
utillc_version = __version__
__all__ = ( 'EKOX', 'EKON', 'STACK', 'EKO', 'TYPE', 'EKOI', 'EKOT', 'EKOH', 'EKOF', 'test', 'Bool', 'ntimes', 'LINE', 'resizeImage', 'count_parameters', 'parse_args', 'Counter', 'ENV', 'print_nothing', 'print_everything', 'noeko', 'NS', 'WARNING', 'INFO', 'ERROR', 'LOG', 'EKOIT', 'yeseko', 'ekostream', 'to_file', 'TIME')
#__all__ = ('listp', 'dump', 'parse')

#import pymf
from datetime import datetime
import platform
python3Running = platform.python_version() == 3
#print (platform.python_version()[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--test", type=utillc.Bool)
    args = parser.parse_known_args()[0]
    if args.test :
        test()
        EKOX("aa")
        inctest.f()
    print(__version__)

