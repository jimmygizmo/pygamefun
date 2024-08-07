# resizer.py

# REASON FOR THIS NEW MODULE (in progress):
# Problem: getting a black background which should be transparent after resizing PNGs using pygame.transform.smoothscale()
# Initial searches do not offer a solution in pygame and I would like to explore not only a good solution for the
# accepted challenge of resizing images with alpha channels while also exploring ALL of the other extreme power of the
# Open CV libraries. I am looking to merge PyGame with other interesting areas, so this is a fantastic reason to take
# a shot at this idea for a little utility module.

# I understand the poster's point that a single algorithm is not going to treat RGB vs Alpha Channel information with
# respect to neighboring pixels (and depending on upscaling vs downscaling) .. and do the best job for both. There
# are literally "edge case" problems. So this poster is making a logical suggestion to apply the best algorithm to each
# the RBG channels vs the Alpha Channel separately and with the best algorith and parameters for the purpose, then
# re-combining those layers back into the desired image format (PNG in the current case.) Sounds like the correct
# strategy to me and although useful in this game for the early image-transformation-upon-load features I have started
# putting in, the area in general would be VERY useful. Scaling and transparency are ubiquititious factors in almost
# every area I am interested in .. or some mathematical equivalent of powerful image processing, used on raw data as
# part of machine learning. Point is, this is a small hook into something extremely powerful and this is a nice place
# to throw it in. It can be branched off into it's own thing or my first all-CV project soon enough.

import cv2
import numpy


def alphonic_resize(img_data: bytes, width: int, height: int) -> bytes:
    # TODO: Adapt this to pass image binary data in and out of the func
    # NOTE: Using numpy in this intermediate step and the var name img_numpy is initial/temporary. Tips to get bytes into
    # cv2 image came from: https://stackoverflow.com/questions/54922372/opencv-cv2-cv-load-image-color
    numpy_array = numpy.fromstring(img_data, numpy.uint8)  # Decode bytes as UInt8 thanks to numpy utility.
    # img_numpy = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)  # TODO: Get details on this option.
    img_numpy = cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)  # TODO: Get details on this option.
    # *************** All fixed! now we get the alpha channel by using IMREAD_UNCHANGED.
    print(f"alphonic_resize INFO: img_numpy.shape: {img_numpy.shape}")
    new_size = (width, height)

    # # Resize the rgb and alpha layers separately and with the optimal algorithm for each.
    rgb = cv2.resize(img_numpy[:,:,:3], new_size, interpolation=cv2.INTER_AREA)
    alpha = cv2.resize(img_numpy[:,:,3], new_size, interpolation=cv2.INTER_NEAREST)
    # Confirmed the same slice as above in an unrelated GitHub project:
    # https://github.com/opencv/opencv/issues/20780
    # UPDATE: About our error here that "index 3 is out of bounds for axis 2 with size 3" This is because we expect
    # there to be 4 layers 0, 1, 2, and 3 (3 is the index of the fourth, ALPHA layer.)
    # Well, when we print the img_numpy.shape() we see that we do not have an alpha channel, only RGB.
    # So the problem is happening earlier. We are not getting our alpha channel into the numpy array.
    # This may very well be because we found that the option constant was deprecated. We had to use IMREAD_COLOR,
    # but that is just to make the read work. We need to find the new option to specify which will get you the
    # alhpa channel. No bug here. Simply our option was deprecated and there must be a new equivalent and I just need
    # to find it. By the way, the one that no longer works is called: cv2.IMREAD_UNCHANGED

    # # Merge the layers back together again.
    rgba = cv2.cvtColor(rgb, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = alpha

    # # Save - TOTAL HACK. I still don't have a clean way to get the bytes, so before I modify cv2.imwrite() itself,
    # I am actually writing a temp file and reading the bytes again as a hack. I'll fix this soon. What I need is a
    # method like cv2.imwrite() or something similar but which will give me the raw PNG file bytes.
    # This is all experimental an not part of an important feature for the game code. Just a nice-to-have and a doorway
    # into some increidbly-powerful possibilities.
    cv2.imwrite('alphonic-resize-temp-png.png', rgba)
    with open('alphonic-resize-temp-png.png', 'rb') as fh:
        img_bytes_out: bytes = fh.read()
    return img_bytes_out


##
#


# OpenCV Docs:
# https://pypi.org/project/opencv-python/

# Posting with suggestion to use Cv2 and different algorithms for the alpha channel vs the RGB channels:
# https://stackoverflow.com/questions/77517041/pygame-smoothscale-png-image-with-alpha-transparency-channels-black-edges

# NOTE: I'm on Windows using WSL/Ubuntu, Pyenv Virtualenv and PyCharm for my dev env.
#    I chose to install opencv-contrib-python for all the interesting extras over just opencv-python.


# Original snippet:
#
# import cv2
#
# path_in = "input.png"
# path_out = "output.png"
# img = cv2.imread(path_in, cv2.IMREAD_UNCHANGED)
# new_size = (640, 480)
#
# # Compute alpha and rgb separately
# rgb = cv2.resize(img[:,:,:3], new_size, interpolation=cv2.INTER_AREA)
# alpha = cv2.resize(img[:,:,3], new_size, interpolation=cv2.INTER_NEAREST)
#
# # Merge back alpha with rgb
# rgba = cv2.cvtColor(rgb, cv2.COLOR_RGB2RGBA)
# rgba[:, :, 3] = alpha
#
# # Save
# cv2.imwrite(path_out, rgba)

# RELEVANT INFO ABOUT USING NUMPY ARRAYS TO HOLD AND PROCESS IMAGE DATA AND HOW MANY LIBRARIES USE
# NUMPY ARRAYS AS A BASIC FORMAT IN THIS AREA. DATA-SCIENCE, MACHINE-LEARNING, ETC.
# https://scikit-image.org/skimage-tutorials/lectures/00_images_are_arrays.html

# Great articles on image processing with OpenCV and Numpy:
# https://note.nkmk.me/en/python-opencv-numpy-alpha-blend-mask/
# Also:
# https://note.nkmk.me/en/python-numpy-image-processing/

# Numpy Array Slicing:
# https://www.turing.com/kb/guide-to-numpy-array-slicing



##
#
