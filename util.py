import os
import random

import pygame
from PIL import Image
import cv2
import matplotlib.pyplot as plt

import numpy as np

def alpha_proc(image):
    # get the numpy array of the image so we can see our alpha channel
    im_np = np.array(image)
    return None