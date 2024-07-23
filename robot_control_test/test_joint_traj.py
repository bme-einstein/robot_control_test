# Verificar nome das variáveis
# Criar um rate

import time
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Duration
import rclpy.parameter
import numpy as np

class JointControllerNode(Node): 
    def __init__(self):
        super().__init__('test_joint_controller_node')
        #Defining the publisher and the subscriber
        self.subs_joints = self.create_subscription(JointState, '/joint_states', self.listener_callback, 1)
        self.pub_joints = self.create_publisher(JointTrajectory, '/scaled_joint_trajectory_controller/joint_trajectory', 1)
        self.joint_states_ = {
            'shoulder_pan_joint': 0.0,
            'shoulder_lift_joint': 0.0,
            'elbow_joint': 0.0,
            'wrist_1_joint': 0.0,
            'wrist_2_joint': 0.0,
            'wrist_3_joint': 0.0,
        }

    def listener_callback(self, joint_states):
        for joint_name, joint_pos in zip(joint_states.name, joint_states.position):
            self.joint_states_[joint_name] = joint_pos
    
    def publish_desired_joint(self, desired_joint_pose):
        joint_traj = JointTrajectory()
        joint_traj.joint_names = self.joint_states_.keys()
        joint_traj.points.append(JointTrajectoryPoint())
        joint_traj.points[0].positions = desired_joint_pose.tolist()
        duration = Duration()
        duration.sec = 1
        duration.nanosec = 0
        joint_traj.points[0].time_from_start = duration
        self.pub_joints.publish(joint_traj)
          

def main(args=None):
    rclpy.init(args=args)
    joint_node = JointControllerNode()
    #rate = joint_node.create_rate(0.5)
    while rclpy.ok():
        rclpy.spin_once(joint_node)
        desired_joints = np.array(list(joint_node.joint_states_.values())) + (np.random.rand(6)-0.5)/10
        joint_node.publish_desired_joint(desired_joints)
        time.sleep(1.5)
        #rate.sleep()
        print([[key, joint_node.joint_states_[key]] for key in joint_node.joint_states_])
        # print(publisher_position_node.ret_val_x)

    joint_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()