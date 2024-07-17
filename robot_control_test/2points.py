# sometimes a square

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('Traj_publisher')
        self.publisher_ = self.create_publisher(PoseStamped, '/cartesian_motion_controller/target_frame', 10)
        timer_period = 3  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i=0.0
        self.x_val=0.4
        self.y_val=0.4

    def timer_callback(self):
        msg=PoseStamped()
        msg.header.frame_id='base_link'
        msg.pose.position.x=self.x_val
        msg.pose.position.y=self.y_val
        msg.pose.position.z=0.6
        msg.pose.orientation.x=1.0
        msg.pose.orientation.y=0.0
        msg.pose.orientation.z=0.0
        msg.pose.orientation.w=0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Pose:"%f"' % self.i)

        if(self.i==1):
            self.y_val=1.0
            self.x_val=0.4
        if(self.i==2):
            self.x_val=1.0
            self.y_val=1.0
        if(self.i==3):
            self.y_val=0.4
            self.x_val=1.0
        if(self.i==4):
            self.y_val=0.4
            self.x_val=0.4
        if(self.i==4):
            self.i=0
        self.i=1+self.i

def main(args=None):
    rclpy.init(args=args)

    Traj_publisher = MinimalPublisher()

    rclpy.spin(Traj_publisher)

    Traj_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()