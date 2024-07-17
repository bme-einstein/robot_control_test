import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf2_msgs.msg import TFMessage

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('Current_pose')
        self.subscription = self.create_subscription(
            PoseStamped,
            '/cartesian_motion_controller/current_pose',
            self.listener_callback,
            10)
        self.subscription 

    def listener_callback(self, m_target_frame):
        self.get_logger().info('I heard: "%f"' % m_target_frame.pose.position.x)


def main(args=None):
    rclpy.init(args=args)

    Current_pose = MinimalSubscriber()

    rclpy.spin(Current_pose)

    Current_pose.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()