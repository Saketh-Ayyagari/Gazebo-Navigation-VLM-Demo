import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from custom_msgs_and_srvs.msg import CustomMessage

"""
Given RGB-D images and odometry information, combine them into a single message "CustomMessage"
and publish it to a topic. The CustomMessage should contain the following fields:
- RGB image (sensor_msgs/Image)
- Depth image (sensor_msgs/Image)
- Odometry information (nav_msgs/Odometry)
"""
class MessageCreator(Node):
    def __init__(self):
        super().__init__('message_creator')

        self.rgb_message = None
        self.depth_message = None
        self.odom_message = None

        self.rgb_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.rgb_callback,
            10
        )
        self.depth_sub = self.create_subscription(
            Image,
            '/camera/depth_image',
            self.depth_callback,
            10
        )
        self.odom_sub = self.create_subscription(
            Odometry,
            '/wheel_odom',
            self.odom_callback,
            10
        )
        self.publisher = self.create_publisher(CustomMessage, '/rgb_d_odom', 10)

    """
    Individual callback functions for each topic. This updates fields to the specific node, and then later
    calls the subscriber_callback function to check if all three messages have been received (this 
    prevents the main callback function from being called before all messages are received). If so, it 
    publishes the CustomMessage to the topic.
    """
    def rgb_callback(self, rgb):
        self.rgb_message = rgb
        self.subscriber_callback()

    def depth_callback(self, depth):
        self.depth_message = depth
        self.subscriber_callback()

    def odom_callback(self, odom):
        self.odom_message = odom
        self.subscriber_callback()

    """
    Overall callback function that checks if all three messages have been received. 
    If so, it creates a CustomMessage.
    """
    def subscriber_callback(self):
        # terminates if any message is None, i.e. if any of the three messages have not been received yet.
        # Ensures that all messages have been received before creating and publishing CustomMessage.
        if self.rgb_message is None or self.depth_message is None or self.odom_message is None:
            return

        custom_msg = CustomMessage()
        custom_msg.rgb = self.rgb_message
        custom_msg.depth = self.depth_message
        custom_msg.odom = self.odom_message

        self.publisher.publish(custom_msg)

def main(args=None):
    rclpy.init(args=args)
    message_creator = MessageCreator()
    rclpy.spin(message_creator)
    message_creator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()