# -*- coding: utf-8 -*-
"""Gaussian_HDR_Tonnmapper_Gamma_correction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fZWV0-t4Iaqg7f18ae0UQZPVQ3W7FJS9
"""

#The first program is for Gaussian weight function which is going to produce the Gaussian HDR image, Gaussian Tonned mapped image and Gaussian gamma-correctedmimage
import os

import numpy as np
import skimage.exposure as exposure
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import exifread


def writeHDR(name, data):
    # flip from rgb to bgr for cv2
    cv2.imwrite(name, 255 * data[:, :, ::-1].astype(np.float32))


def readHDR(name):
    raw_in = cv2.imread(name, flags=cv2.IMREAD_UNCHANGED)
    # flip from bgr to rgb
    return raw_in[:, :, ::-1]


def get_exposure(filename):
    images = open(filename, 'rb')
    exposure = exifread.process_file(images)['EXIF ExposureTime'].values[0].decimal()
    return exposure

def wuniform(images, zmin, zmax):
    return np.where((images >= zmin) & (images <= zmax), 1, 0)

def wtent(images, zmin, zmax):
    return np.where((images >= zmin) & (images <= zmax), np.minimum(images, 1 - images) ,0)

def wGaussian(images, zmin, zmax):
    return np.where((images >= zmin) & (images <= zmax), np.exp(-4 * ((images - 0.5) ** 2) / (0.5 ** 2)), 0)

def wphoton(images, zmin, zmax, tk):
    return np.where((images >= zmin) & (images <= zmax), tk, 0)

def main(weight_indx):



    tiff_files = ["/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure1.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure2.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure3.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure4.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure5.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure6.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure7.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure8.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure9.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure10.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure11.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure12.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure13.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure14.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure15.tiff",
                  "/Users/rk/Downloads/HDRProject/nef_images/tiff_images/tiff-new_16_feb/exposure16.tiff"]


    ldr_images = [readHDR(images) / 65535 for images in tiff_files]

    exposures = [get_exposure(images) for images in tiff_files]

    Z_MIN = 0.05  # fixed value
    Z_MAX = 0.95 # fixed value

# calculating the weights
    weight_name= ["wUniform", "wTent", "wGaussian", "wPhoton"]

    if weight_indx == 0:
        weights_arr = [wuniform(ldr_images[i], Z_MIN, Z_MAX) for i in range(len(ldr_images))]
    elif weight_indx == 1:
        weights_arr = [wtent(ldr_images[i], Z_MIN, Z_MAX) for i in range(len(ldr_images))]
    elif weight_indx == 2:
        weights_arr = [wGaussian(ldr_images[i], Z_MIN, Z_MAX) for i in range(len(ldr_images))]
    elif weight_indx == 3:
        weights_arr = [wphoton(ldr_images[i], Z_MIN, Z_MAX, exposures[i]) for i in range(len(ldr_images))]


    # generation of scaled image
    # scaled image= images[i]/exposure[i]
    print("HDR image generation")
    epsilon= 1e-6 # to avoid the zero divisoin
    weights_arr = np.array(weights_arr)

    scaled_image = [ldr_images[i] / exposures[i] for i in range(len(ldr_images))]

    gaussian_hdr = np.sum(weights_arr * scaled_image, axis=0) / (np.sum(weights_arr, axis=0) + epsilon)



    writeHDR("/Users/rk/Downloads/HDRProject/nef_images/tiff_images/results/{}_hdr_0.05_0.95.PNG".format(weight_name[weight_indx]), gaussian_hdr)



    print("Part3:Tonemapping")

    # Tone_mapping only for gaussian image

    h, w, ch= gaussian_hdr.shape

    tonemapp_gaussian_hdr= np.zeros_like(gaussian_hdr )

    K= 0.01
    B= 0.95
    # We will tone-mapusing the operator proposed by Reinhard

    I_m = np.exp(np.mean(np.log(gaussian_hdr[:, :, :] + epsilon)))
    I_tild_hdr = K * gaussian_hdr[:, :, :] / I_m
    I_tild_white = B * np.max(I_tild_hdr)
    tonemapp_gaussian_hdr[:, :, :] = (I_tild_hdr * (1 + I_tild_hdr / (I_tild_white ** 2))) / (1 + I_tild_hdr)


    writeHDR("/Users/rk/Downloads/HDRProject/nef_images/tiff_images/results/{}_hdr_tm_K_{}_B_{}.PNG".format(weight_name[weight_indx], K, B), tonemapp_gaussian_hdr)
    #cv2.imshow("tm",tonemapp_gaussian_hdr)
    #cv2.waitKey()
    Print("Part:4 Gamma Correction of Gaussion HDR")


    # Gamma correction
    gamma_gaussian_hdr= np.where(tonemapp_gaussian_hdr <= 0.0031308, 12.92 * tonemapp_gaussian_hdr, 1.055 * (tonemapp_gaussian_hdr ** (1/2.5)) - 0.055)

    writeHDR("/Users/rk/Downloads/HDRProject/nef_images/tiff_images/results/{}_hdr_tm_gamma_K_{}_B_{}.PNG".format(weight_name[weight_indx],K, B), gamma_gaussian_hdr)
    #cv2.imshow("gamma",photon_hdr_tm_gamma)
    #cv2.imwrite("/Users/rk/Downloads/HDRProject/nef_images/tiff_images",abc,Gaussian_hdr_tm_gamma)
    #cv2.waitKey()

if __name__ == '__main__':

    # weight function choosing options 0,1,2,3 is for uniform, tent, gaussioan and photon respectively
    #here I choose 2 that means the program is only going to generate the HDR, ToneHDR and GammaHDR for Gaussian
    #inorder to choose the other function select the other value
    weight_indx= 2
    main(weight_indx)
    # Tone_mapping()