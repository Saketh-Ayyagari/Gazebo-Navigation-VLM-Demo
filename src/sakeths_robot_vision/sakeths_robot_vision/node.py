import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2 as cv
import modules_to_import.opencv_utils as cv_utils

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/depth_image',
            self.listener_callback,
            10)
        self.br = CvBridge()
    
    def listener_callback(self, data):
        # self.get_logger().info('Receiving video frame')
        # As pointed in comments below modify the following to use bgr encoding
        # current_frame = self.br.imgmsg_to_cv2(data)
        current_frame = self.br.imgmsg_to_cv2(data, desired_encoding="passthrough") # use "passthrough" to get the raw depth image, and "rgb8" for color images
        cv_utils.show_image(current_frame)

    
def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()