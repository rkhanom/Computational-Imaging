#!/usr/bin/python
""" This is a module for hdr imaging homework (15-463/663/862, Computational Photography, Fall 2020, CMU).

Modified by cmetzler on 9/13/2022

You can import necessary functions into your code as follows:
from HDR_helperfiles import *

Depends on OpenCV to read/write HDR files"""

import numpy as np
import cv2
import exifread

def writeHDR(name, data):
    #flip from rgb to bgr for cv2
    cv2.imwrite(name, 255*data[:, :, ::-1].astype(np.float32))
        
def readHDR(name):
    raw_in = cv2.imread(name, flags=cv2.IMREAD_UNCHANGED)
    #flip from bgr to rgb
    return raw_in[:, :, ::-1]

def get_exposure(filename):
    f=open(filename,'rb')
    exposure=exifread.process_file(f)['EXIF ExposureTime'].values[0].decimal()
    return exposure
