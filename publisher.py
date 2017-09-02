import nengo
import rospy

from geometry_msgs.msg import Twist

class TwistPublisher(object):

    def __init__(self, topic='/my_topic', queue_size=10, disable_signals=True):

        rospy.init_node('twist_publisher', anonymous=True,
                        disable_signals=disable_signals)

        self.twist_msg = Twist()

        self.pub_twist = rospy.Publisher(topic, Twist, queue_size=queue_size)

    def __call__(self, t, x):

        # Forward Velocity
        self.twist_msg.linear.x = x[0]

        # Angular Velocity
        self.twist_msg.angular.z = x[1]

        self.pub_twist.publish(self.twist_msg)

model = nengo.Network('Main Control', seed=13)
with model:
    twist_input = nengo.Node([0,0])

    ros_publisher = nengo.Node(TwistPublisher(),
                               size_in=2,
                               size_out=0
                              )

    nengo.Connection(twist_input, ros_publisher)
