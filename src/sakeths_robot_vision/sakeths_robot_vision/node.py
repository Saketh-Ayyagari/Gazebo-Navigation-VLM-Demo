import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2 as cv
from ultralytics import YOLO
import modules_to_import.opencv_utils as cv_utils

FRAME_RATE = 10  # frames per second

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.timer_callback,
            10)
        self.br = CvBridge()
        self.model = YOLO('yolov8n.pt')  # Load a pre-trained YOLOv8 model
        
        timer_period = 1 / FRAME_RATE # runs this node based on the frame rate (can be customized)
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self, msg):
        self.get_logger().info('Receiving video frame')
        self.camera_callback(msg)
    '''
    Runs YOLO model on specific frame and displays results. Converts ROS2 image message to OpenCV format 
    using CvBridge, then runs YOLO model on the frame and displays the results using OpenCV.

    @params
    img: ROS2 image message.
    '''
    def camera_callback(self, img):
        current_frame = self.br.imgmsg_to_cv2(img, desired_encoding="passthrough") # use "passthrough" to get the raw depth image, and "rgb8" for color images

        # self.get_logger().info('Receiving video frame')
        # As pointed in comments below modify the following to use bgr encoding
        # current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')

        results = self.model(current_frame)
        cv_utils.show_image(results[0].plot())
    
def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()