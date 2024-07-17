# Verificar nome das variáveis
# Criar um rate

import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import rclpy.parameter

class PublisherNode(Node):
    def __init__(self):
        super().__init__('Publisher_position_node')
        #Defining the publisher and the subscriber
        self.publisher_=self.create_publisher(PoseStamped,'/cartesian_motion_controller/target_frame', 10)
        self.timer = self.create_timer(1, self.Publishing_Coordinates)
        #Defining other values
        self.i=1.0
        self.x_val=0.4
        self.y_val=0.4
        self.Error_x=0.0
        self.Erro_y=0.0
    def Publishing_Coordinates(self):
        if(self.i==2):
            self.y_val=1.0
            self.x_val=0.4
        if(self.i==3):
            self.x_val=1.0
            self.y_val=1.0
        if(self.i==4):
            self.y_val=0.4
            self.x_val=1.0
        if(self.i==5):
            self.y_val=0.4
            self.x_val=0.4
        if(self.i==5):
            self.i=1

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
        self.ret_val_x=self.x_val
        self.ret_val_y=self.y_val
        self.get_logger().info('Pose:"%f"' % self.i)

        self.i=1+self.i 
class SubscriberNode(Node): 
    def __init__(self):
        super().__init__('Subscriber_position_node')
        #Defining the publisher and the subscriber
        self.subscription2=self.create_subscription(PoseStamped,'/cartesian_motion_controller/current_pose',self.listener_callback,10)
        #Defining other values
        self.i=0.0
        self.Error_x=0.0
        self.Erro_y=0.0
    def listener_callback(self, m_current_frame):
      #self.get_logger().info('I heard: "%f"' % m_current_frame.pose.position.x)
      #self.get_logger().info('I heard: "%f"' % m_current_frame.pose.position.y)
      self.retur_current_x=m_current_frame.pose.position.x
      self.retur_current_y=m_current_frame.pose.position.y

          

def main(args=None):
    rclpy.init(args=args)
    publisher_position_node=PublisherNode()
    subscriber_position_node=SubscriberNode()
    rclpy.spin_once(publisher_position_node)
    print(publisher_position_node.ret_val_x)
    rate=publisher_position_node.create_rate(250)
    while rclpy.ok():
        rclpy.spin_once(subscriber_position_node)
        if ((abs(publisher_position_node.ret_val_x-subscriber_position_node.retur_current_x)<0.02) and ((abs(publisher_position_node.ret_val_y-subscriber_position_node.retur_current_y))<0.02)):
            print('X_Current: "%f"' % subscriber_position_node.retur_current_x)
            print('Y_Current: "%f"' % subscriber_position_node.retur_current_y)
            print('Target_x: "%f"' % publisher_position_node.ret_val_x)
            print('Target_y: "%f"' %publisher_position_node.ret_val_y)
            print("Trocando para pose...")
            rclpy.spin_once(publisher_position_node)
        #time.sleep(5)
        rate.sleep()
        print(publisher_position_node.ret_val_x)

    publisher_position_node.destroy_node()
    subscriber_position_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()