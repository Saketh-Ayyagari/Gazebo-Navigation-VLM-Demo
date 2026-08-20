import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2 as cv
from ultralytics import YOLO
import modules_to_import.opencv_utils as cv_utils


class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.br = CvBridge()
        self.model = YOLO('yolov8n.pt')  # Load a pre-trained YOLOv8 model

        self.subscription = self.create_subscription(
            Image,
            '/camera/depth_image',
            self.camera_callback,
            10)
                

    '''
    Runs pipeline for object detection

    1. Given RGB-D images and odometry data, first segments RGB image into different objects using YOLOv8
    (can be replaced with a VLM/other image segmentation model of some sort). Uses the bounding boxes to
    get the approximate center of the object in the RGB image. 
    2. Uses depth image to get the distance to the object in the RGB image. 
    3. Uses pinhole camera model to get 3D position of any object relative to the camera.
    4. Combines the 3D position of the object with the odometry data to get the position of the object 
    in the world frame.
    5. Stores results in JSON file. Results include
        - Object category.
        - Estimated position of the object in world frame.

    @params

    RGB Image for image segmentation.
    Depth image for calculating distances to objects in RGB image.
    Odometry message containing robot's current pose.
    '''
    def camera_callback(self, img):
        depth_frame = self.br.imgmsg_to_cv2(img, desired_encoding="passthrough") # use "passthrough" to get the raw depth image, and "rgb8" for color images

        # self.get_logger().info('Receiving video frame')
        # As pointed in comments below modify the following to use bgr encoding
        # current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')

        results = self.model(current_frame) # running YOLO model for instance segmentation
        cv_utils.show_image(results[0].plot())

        # given bounding box coordinates, calculate center of the bounding box and use it to get the depth value from the depth image.

        # storing results in a JSON file. Results consist of instance of a category and the estimated
        # position of the object. The estimated position is calculated using the depth image and the.
    
def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()