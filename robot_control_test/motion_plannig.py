# Caso mude o x_f, como o publisher irá calcular a nova função da melhor maneira (******)


import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import rclpy.parameter

class PublisherNode(Node):
    def __init__(self):
        super().__init__('Publisher_position_node')
        #Defining the publisher and the subscriber
        self.publisher_=self.create_publisher(PoseStamped,'/cartesian_motion_controller/target_frame', 10)
        self.timer = self.create_timer(0.01, self.Publishing_Coordinates)
        #Defining other values
        self.i=0.0
        self.x_val=0.0
        self.y_val=0.0
        #Defining initial and final positions (x):
        self.x_o=0.2
        self.x_f=1.0
        self.xd_o=0.0
        self.xd_f=0.0
        #Defining initial and final positions (y):
        self.y_o=0.2
        self.y_f=1.0
        self.yd_o=0.0
        self.yd_f=0.0
        #Defining the time lapse:
        self.T=15.0 #s
        #Solving to 3°: x
        self.a_x=np.array([[1,0, 0, 0],[0,1,0,0],[1,self.T,(self.T**2),(self.T**3)],[0,1,2*self.T,3*(self.T**2)]])
        self.b_x=np.array([[self.x_o],[self.xd_o],[self.x_f],[self.xd_f]])
        self.coe_x=np.linalg.solve(self.a_x,self.b_x)
        #Solving to 3°: y
        self.a_y=np.array([[1,0, 0, 0],[0,1,0,0],[1,self.T,(self.T**2),(self.T**3)],[0,1,2*self.T,3*(self.T**2)]])
        self.b_y=np.array([[self.y_o],[self.yd_o],[self.y_f],[self.yd_f]])
        self.coe_y=np.linalg.solve(self.a_y,self.b_y)

    def Publishing_Coordinates(self):

        self.x_val=self.coe_x[0]+self.coe_x[1]*self.i+self.coe_x[2]*(self.i**2)+self.coe_x[3]*(self.i**3)
        self.x_val=float(self.x_val)

        self.y_val=self.coe_y[0]+self.coe_y[1]*self.i+self.coe_y[2]*(self.i**2)+self.coe_y[3]*(self.i**3)
        self.y_val=float(self.y_val)        

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

        if(self.i==self.T):
            self.i=0

        self.i=1+self.i

class SubscriberNode(Node): 
    def __init__(self):
        super().__init__('Subscriber_position_node')
        #Defining the publisher and the subscriber
        self.subscription2=self.create_subscription(PoseStamped,'/cartesian_motion_controller/current_pose',self.listener_callback,10)
        #Defining other values
    def listener_callback(self, m_current_frame):
      #self.get_logger().info('I heard: "%f"' % m_current_frame.pose.position.x)
      #self.get_logger().info('I heard: "%f"' % m_current_frame.pose.position.y)
      self.retur_current_x=m_current_frame.pose.position.x
      self.retur_current_y=m_current_frame.pose.position.y

          

def main(args=None)
    rclpy.init(args=args)
    publisher_position_node=PublisherNode()
    subscriber_position_node=SubscriberNode()
    rclpy.spin_once(publisher_position_node)
    while rclpy.ok():
        rclpy.spin_once(subscriber_position_node)
        if ((abs(publisher_position_node.ret_val_x-subscriber_position_node.retur_current_x)<0.04) and (abs(publisher_position_node.ret_val_y-subscriber_position_node.retur_current_y)<0.04)):
            print('X_Current: "%f"' % subscriber_position_node.retur_current_x)
            print('Y_Current: "%f"' % subscriber_position_node.retur_current_y)
            print('Target_x: "%f"' % publisher_position_node.ret_val_x)
            print('Target_y: "%f"' % publisher_position_node.ret_val_y)

            print("Trocando para pose...")
            rclpy.spin_once(publisher_position_node)


    publisher_position_node.destroy_node()
    subscriber_position_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()