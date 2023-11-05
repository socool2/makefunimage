import sys
import os
import cv2
from cv2 import dnn_superres
import numpy as np


#
# sharpening_mask1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
# sharpening_mask2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
#
# argument = sys.argv
#
# rfile = argument[1]
# smodel = argument[2].upper()
# scale = int(argument[3])
#
# idx = rfile.rfind('.')
# rfile_cut = rfile[0:idx]
#
# wfile = rfile_cut + "_" + smodel + "_x" + str(scale) + ".png"
#
# # Create an SR object - only function that differs from c++ code
# sr = dnn_superres.DnnSuperResImpl_create()
# # Read image
# image = cv2.imread(rfile)
# # Read the desired model
# path = "models/" + smodel + "_x" + str(scale) + ".pb"
#
# if os.path.isfile(path) :
#     #path = "models/EDSR_x4.pb"
#     sr.readModel(path)
#     # Set the desired model and scale to get correct pre- and post-processing
#     sr.setModel(smodel.lower(), scale)
#     # Upscale the image
#     result = sr.upsample(image)
#
#     sharpening_out = cv2.filter2D(result, -1, sharpening_mask1)
#
#     # Save the image
#     cv2.imwrite(wfile, result)
#     #cv2.imwrite(wfile, sharpening_out)
#
# else :
#     result = cv2.resize(image, dsize=(0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
#     # Save the image
#     cv2.imwrite(wfile, result)
#

def make_upscale_image(makefile, alg, scale):
    sharpening_mask1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpening_mask2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    scale = int(scale.replace('x', ''))

    idx = makefile.rfind('.')
    rfile_cut = makefile[0:idx]

    wfile = rfile_cut + "_" + alg + "_x" + str(scale) + ".png"

    # Create an SR object - only function that differs from c++ code
    sr = dnn_superres.DnnSuperResImpl_create()
    # Read image
    image = cv2.imread(makefile)
    # Read the desired model
    path = "models/" + alg + "_x" + str(scale) + ".pb"

    if os.path.isfile(path):
        # path = "models/EDSR_x4.pb"
        sr.readModel(path)
        # Set the desired model and scale to get correct pre- and post-processing
        sr.setModel(alg.lower(), scale)
        # Upscale the image
        result = sr.upsample(image)

        sharpening_out = cv2.filter2D(result, -1, sharpening_mask1)

        # Save the image
        cv2.imwrite(wfile, result)
        # cv2.imwrite(wfile, sharpening_out)

    else:
        result = cv2.resize(image, dsize=(0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        # Save the image
        cv2.imwrite(wfile, result)

    return wfile.split('/')[1]