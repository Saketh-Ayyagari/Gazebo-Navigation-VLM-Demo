import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2 as cv
from ultralytics import YOLO
import modules_to_import.opencv_utils as cv_utils
from custom_msgs_and_srvs.msg import CustomMessage

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.br = CvBridge()
        self.model = YOLO('yolov8n.pt')  # Load a pre-trained YOLOv8 model

        self.subscription = self.create_subscription(
            CustomMessage,
            '/rgb_d_odom',
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
    def camera_callback(self, msg: CustomMessage):
        rgb_frame = self.br.imgmsg_to_cv2(msg.rgb, desired_encoding="rgb8")
        depth_frame = self.br.imgmsg_to_cv2(msg.depth, desired_encoding="passthrough")
        odom = msg.odom


        results = self.model(rgb_frame) # running YOLO model for instance segmentation

        if results != None:
            # For each detected object, get bounding box coordinates and calculate approximate "center".
            detections = []
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                box_cx = int((x1 + x2) // 2)
                box_cy = int((y1 + y2) // 2)
                self.get_logger().info(f"CENTER: ({box_cy}, {box_cx})")
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'center': (box_cx, box_cy),
                    'class': box.cls[0],
                    'confidence': box.conf[0]
                })
            
            # now use specific coordinate to get approximate depth value to object.
            for detection in detections:
                box_cx, box_cy = detection['center']
                Z = depth_frame[box_cy][box_cx]
                detection['depth'] = Z

            # Given depth values, pixel coordinates (u, v), and camera instrinsics, calculate (X, Y, Z)
            # Assuming camera intrinsics like focal length (fx, fy) and principal point (cx, cy) are known. 
            fx, fy, cx, cy = 394.6, 394.6, 320.0, 240.0  # Hardcoded intrinsics, update with actual values
            
            for detection in detections:
                box_cx, box_cy = detection['center']
                Z = detection['depth']
                
                # Pinhole camera model: X = (u - cx) * Z / fx, Y = (v - cy) * Z / fy, Z = Z
                X = (box_cx - cx) * Z / fx
                Y = (box_cy - cy) * Z / fy
                
                detection['3d_position'] = (X, Y, Z) # this is relative to the base_link!
            
        self.get_logger().info(f"Detections: {detection}")
        cv_utils.show_image(results[0].plot())


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