# HDR Image Fusion and Tone-Mapping Project

## Overview

This project aims to merge a stack of Low Dynamic Range (LDR) images into a single High Dynamic Range (HDR) image using Python. Additionally, it involves tone-mapping the HDR image for display and gamma-correcting the resulting LDR images. The project is divided into several tasks, each focusing on different aspects of image processing and HDR imaging techniques.

## Task 1: Merge the LDR Images into an HDR Image

### Objective
Combine a stack of LDR images with different exposures into a single HDR image.

### Method
1. Scale each image by the reciprocal of its exposure time to ensure relative brightness consistency.
2. Compute the HDR image using a weighted combination of the LDR images.
3. Apply a weighting function to average properly exposed pixels while avoiding clipped or underexposed/noisy pixels.

### Weighting Schemes
- Uniform Weighting
- Tent Weighting
- Gaussian Weighting
- Photon Weighting

## Task 2: Tone-Mapping the HDR Image

### Objective
Tone-map the HDR image into an LDR image for display using the Reinhard et al. operator.

### Method
1. Apply the tone-mapping operator to the HDR image.
2. Sweep over various values for the key (K) and burn (B) parameters to adjust brightness and contrast.
3. Tone-map all four HDR images using the chosen parameter values.

## Task 3: Gamma-Correct the LDR Image for Display

### Objective
Gamma-correct the tone-mapped LDR images to ensure accurate display on monitors.

### Method
Apply the gamma correction operator specified in the sRGB standard to the tone-mapped LDR images.

## Task 4: Lossy Compression

### Objective
Save one of the images in the compressed JPEG format and determine the lowest quality setting for indistinguishable compression from the original.

### Method
- Use OpenCV's `imwrite` command to save an image in JPEG format.
- Sweep over JPEG quality settings to find the lowest setting with indistinguishable compression from the original.
- Calculate the compression ratio with respect to PNG file sizes.



