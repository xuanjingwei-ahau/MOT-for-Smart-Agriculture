# MOT-for-Smart-Agriculture

## MOT-for-tomatoes

### RGB-D data fusion for tracking counting and yield estimation of single fruit tomatoes



#### 1.Deep distance output

Please refer to `distance.py`.

16-bit depth data: The depth map output from Azure Kinect is usually in uint16 format, with the unit in millimeters (mm). When using cv2.imread, you must add cv2.IMREAD_UNCHANGED, otherwise OpenCV will force it into 8-bit, causing precision loss and incorrect values.

Alignment precondition:

If your rgb.png is the original 4K/1080P image and depth.png is the original 512x512 image, the above code will give an error.

You must use pyk4a.transformation.depth_image_to_color_camera() to transform the depth map into the RGB perspective at the frame extraction stage.

Handling the "black hole" (invalid depth):

The areas in the depth map where the value is 0 are usually invalid regions caused by insufficient infrared reflection or occlusion. When setting min_dist, it is generally recommended to set it to a value greater than 0 (e.g., min_dist=1), which automatically filters out these noise points.



#### 2.Dynamically demonstrate the change of depth information

Please refer to `distance.py`.





### Contact us

If you have any problems when downloading and using this code, please contact us by email:xuanjingwei@stu.ahua.edu.cn.