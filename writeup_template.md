## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/01-chessboard_calibration.png "calibration"
[image2]: ./output_images/02-undistorted_chessboard.png "undistorted_chessboard"
[image3]: ./output_images/03-undistorted_sample.png "undistorted_sample"
[image4]: ./output_images/04-unwarped.png "unwarped"
[image5]: ./output_images/05-color_space_channels.png "color_space_channels"
[image6]: ./output_images/06-sobel_x_sample.png "sobel_x"
[image7]: ./output_images/07-hls_l_threshold.png "hls_l_threshold"
[image8]: ./output_images/08-lab_b_threshold.png "lab_b_threshold"
[image9]: ./output_images/09-image_processing_pipline_samples.png "image_processing_pipline"
[image10]: ./output_images/10-sliding_window_polyfit.png "sliding_window_polyfit"
[image11]: ./output_images/11-sliding_window_histogram.png "sliding_window_histogram"
[image12]: ./output_images/12-polyfit_using_prev_fit.png "polyfit_using_prev_fit"
[image13]: ./output_images/13-draw_lane_and_data.png "draw_lane_and_data"
[video1]: ./project_video_output.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first 6 code cells of the IPython notebook located in "./project.ipynb".  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  
I also used cv2.cornerSubPix() to increase the detect accuracy as suggested in [opencv tutorial](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html)

![alt text][image1]

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result:

![alt text][image2]


### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image3]

The effect of undistort is subtle, except for the hood of the car at the bottom.

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I explored sobel x gradient thresholds and color channel thresholds in multiple color spaces. 

![alt text][image6]

The below image shows the various channels of three different color spaces for the same image:

![alt text][image5]

Finally, I chose to use the combination of HLS L-Channel & LAB B-Channel to create a threshold binary image,
since L-Channel is good for white lines and B-Channel isolates the yellow lines very well.
Below are examples of thresholds in the HLS L channel and the LAB B channel:

![alt text][image7]

![alt text][image8]

And here are the results of applying the binary thresholding pipeline to various sample images:

![alt text][image9]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `unwarp()`, which appears in the section 'Perspective Transform' of the IPython notebook).  The `unwarp()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32([(575,464),
                  (707,464), 
                  (258,682), 
                  (1049,682)])
dst = np.float32([(450,0),
                  (w-450,0),
                  (450,h),
                  (w-450,h)])
```
Considering the camera remains fix position and the road remains relatively flat, I chose to hardcode the source and desination points.
The image below demonstrates the results of the perspective transform:

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Just as taught in [Finding the Lines](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/2b62a1c3-e151-4a0e-b6b6-e424fa46ceab/lessons/40ec78ee-fb7c-4b53-94a8-028c5c60b858/concepts/c41a4b6b-9e57-44e6-9df9-7e4e74a1a49a)
First, find peaks in a Histogram:

![alt text][image11]

Then, implement the function `sliding_window_polyfit` to Sliding Windows and Fit a Polynomial for the first frame:

![alt text][image10]

And, fit polynomial to the other images based upon a previous fit  by the function `polyfit_using_prev_fit`:

![alt text][image12]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I calculated the radius of curvature of the lane based on the course [Measuring Curvature](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/2b62a1c3-e151-4a0e-b6b6-e424fa46ceab/lessons/40ec78ee-fb7c-4b53-94a8-028c5c60b858/concepts/2f928913-21f6-4611-9055-01744acc344f)

```python
left_curverad = ((1 + (2*left_fit[0]*y_eval + left_fit[1])**2)**1.5) / np.absolute(2*left_fit[0])
right_curverad = ((1 + (2*right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.absolute(2*right_fit[0])
```

The position of the vehicle with respect to the center of the lane is calculated with the following lines of code:

```python
l_fit_x_int = l_fit[0]*h**2 + l_fit[1]*h + l_fit[2]
r_fit_x_int = r_fit[0]*h**2 + r_fit[1]*h + r_fit[2]
lane_center_position = (r_fit_x_int + l_fit_x_int) /2
center_dist = (car_position - lane_center_position) * x_meters_per_pix
```
l_fit_x_int and r_fit_x_int are the x-intercepts of the right and left fits.
The car position is the difference between these intercept points and the image midpoint (assuming that the camera is mounted at the center of the vehicle).

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in the code cells titled "Draw the Detected Lane Back onto the Original Image" and "Draw Curvature Radius and Distance from Center Data onto the Original Image" in the Jupyter notebook. A polygon is generated based on plots of the left and right fits, warped back to the perspective of the original image using the inverse perspective matrix Minv and overlaid onto the original image. 
Below is an demonstration of the results of the `draw_lane` and `draw_data` function, which writes text identifying the curvature radius and vehicle position data and drawing lane area onto the original image:

![alt text][image13]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video_output.mp4)

---
