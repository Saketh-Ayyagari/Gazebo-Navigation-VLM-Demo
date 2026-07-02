import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2 as cv
import numpy as np
import modules_to_import.opencv_utils as cv_utils
from modules_to_import.VisualOdometry import VisualOdometry

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10)
        self.br = CvBridge()

        CAMERA_WIDTH, CAMERA_HEIGHT = (640, 480)
        cx, cy = (CAMERA_WIDTH / 2, CAMERA_HEIGHT / 2)
        
        fx = (CAMERA_WIDTH / 2) / np.arctan(np.deg2rad(78) / 2)
        fy = fx
        K = np.array([[fx, 0, cx],
                      [0, fy, cy],
                      [0, 0, 1]])
        self.vo = VisualOdometry(camera_width=640, camera_height=480, K=K, show_matched_features=True)
        self.prev_frame = None

        self.pos = np.zeros(3)  # initial position of the camera in world coordinates


    def listener_callback(self, data):
        # self.get_logger().info('Receiving video frame')
        # As pointed in comments below modify the following to use bgr encoding
        # current_frame = self.br.imgmsg_to_cv2(data)
        current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')
        cv_utils.show_image(current_frame)

        if self.prev_frame:
            R, t = self.vo.get_pose_estimate(self.prev_frame, current_frame)
            if R and t:
                # now use R and t to update robot's pose estimate
                self.get_logger().info(f"Estimated Rotation:\n{R}\nEstimated Translation:\n{t}")

                # update pose estimate using p_t+1 = R*p_t + t
                self.pos = np.matmul(R, self.pos) + t.ravel()
        
        self.prev_frame = current_frame
    
def main(args=None):
    rclpy.init(args=args)
    image_subscriber = ImageSubscriber()
    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()