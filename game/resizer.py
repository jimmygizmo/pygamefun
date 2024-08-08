# resizer.py

import sys
# import config as cfg  # TODO: Implement use of cfg.DEBUG flag.
import cv2
import numpy

# Takes the raw bytes of a PNG image with alpha channel and optimally resizes it, preserving transparency properly.
# Returns the raw bytes of a PNG image with alpha channel, now at the new size. (Shape of third dimension is always 4.)
def alphonic_resize(img_data: bytes, width: int, height: int) -> bytes:
    numpy_array = numpy.fromstring(img_data, dtype=numpy.uint8, sep='')  # Decode bytes as UInt8 thanks to numpy utility.
    img_numpy = cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)
    # print(f"alphonic_resize - after numpy.fromstring AND cv2.imdecode - original size: img_numpy.shape: {img_numpy.shape}")
    new_size = (width, height)

    # # Resize the rgb and alpha layers separately and with the optimal algorithm for each.
    # rgb = cv2.resize(img_numpy[:,:,:3], new_size, interpolation=cv2.INTER_AREA)  # ORIGINAL
    rgb = cv2.resize(img_numpy[:,:,:3], new_size, interpolation=cv2.INTER_LINEAR)
    # alpha = cv2.resize(img_numpy[:,:,3], new_size, interpolation=cv2.INTER_NEAREST)  # ORIGINAL
    alpha = cv2.resize(img_numpy[:,:,3], new_size, interpolation=cv2.INTER_LINEAR)

    # For resizing larger (grumpy cat test) INTER_LINEAR works well. INTER_CUBIC works similarly.
    # TODO: Add a sharpen (unsharp mask) step if possible. Ususally an improvement after resizing which tends to add fuzziness.

    # # Merge the layers back together again.
    rgba = cv2.cvtColor(rgb, cv2.COLOR_RGB2RGBA)
    rgba[:, :, 3] = alpha

    # Using this temp file hack until I can more cleanly get the raw image (PNG file) bytes out of the cv2 image.
    cv2.imwrite('alphonic-resize-temp-png.png', rgba)
    with open('alphonic-resize-temp-png.png', 'rb') as fh:
        img_bytes_out: bytes = fh.read()


    out_numpy_array = numpy.fromstring(img_bytes_out, dtype=numpy.uint8, sep='')  # For debug logging only for now.
    out_img_numpy = cv2.imdecode(out_numpy_array, cv2.IMREAD_UNCHANGED)  # For debug logging only for now.
    # print(f"alphonic_resize - after resize - returned size: out_img_numpy.shape: {out_img_numpy.shape}")
    return img_bytes_out

    # Everything works but looks like we might have a black line around the very edgy (somewhat known issue.)


if __name__ == '__main__':
    print("WARNING: PyGameFun resizer.py has been run directly, however it is only meant to be imported.")
    sys.exit(1)


##
#
