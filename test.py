import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6 * 9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d points in real world space
imgpoints = []  # 2d points in image plane.

# Make a list of calibration images
images = glob.glob('./camera_cal/calibration*.jpg')

fig, axs = plt.subplots(5, 4, figsize=(16, 11))
fig.subplots_adjust(hspace=.2, wspace=.001)
axs = axs.ravel()

# Step through the list and search for chessboard corners
for i, fname in enumerate(images):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

    # If found, add object points, image points
    if ret:
        objpoints.append(objp)

        # this step to refine image points was taken from:
        # http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (9, 6), corners, ret)
        # axs[i].axis('off')
        axs[i].imshow(img)


# Visualize multiple color space channels
img_unwarp_R = img_unwarp[:, :, 0]
img_unwarp_G = img_unwarp[:, :, 1]
img_unwarp_B = img_unwarp[:, :, 2]
img_unwarp_HLS = cv2.cvtColor(img_unwarp, cv2.COLOR_RGB2HLS)
img_unwarp_H = img_unwarp_HLS[:, :, 0]
img_unwarp_L = img_unwarp_HLS[:, :, 1]
img_unwarp_S = img_unwarp_HLS[:, :, 2]
img_unwarp_LAB = cv2.cvtColor(img_unwarp, cv2.COLOR_RGB2Lab)
img_unwarp_L = img_unwarp_LAB[:, :, 0]
img_unwarp_A = img_unwarp_LAB[:, :, 1]
img_unwarp_B = img_unwarp_LAB[:, :, 2]
fig, axs = plt.subplots(3, 3, figsize=(16, 12))
fig.subplots_adjust(hspace=.2, wspace=.001)
axs = axs.ravel()
axs[0].imshow(img_unwarp_R, cmap='gray')
axs[0].set_title('RGB R-channel', fontsize=30)
axs[1].imshow(img_unwarp_G, cmap='gray')
axs[1].set_title('RGB G-Channel', fontsize=30)
axs[2].imshow(img_unwarp_B, cmap='gray')
axs[2].set_title('RGB B-channel', fontsize=30)
axs[3].imshow(img_unwarp_H, cmap='gray')
axs[3].set_title('HLS H-Channel', fontsize=30)
axs[4].imshow(img_unwarp_L, cmap='gray')
axs[4].set_title('HLS L-channel', fontsize=30)
axs[5].imshow(img_unwarp_S, cmap='gray')
axs[5].set_title('HLS S-Channel', fontsize=30)
axs[6].imshow(img_unwarp_L, cmap='gray')
axs[6].set_title('LAB L-channel', fontsize=30)
axs[7].imshow(img_unwarp_A, cmap='gray')
axs[7].set_title('LAB A-Channel', fontsize=30)
axs[8].imshow(img_unwarp_B, cmap='gray')
axs[8].set_title('LAB B-Channel', fontsize=30)
