import nengo
import rospy

from geometry_msgs.msg import Twist

class TwistSubscriber(object):

    def __init__(self, topic='/my_topic', disable_signals=True):

        #NOTE: the publisher already initialized the rospy node, can't do it twice
        #rospy.init_node('twist_subscriber', anonymous=True,
        #                disable_signals=disable_signals)

        self.lin_vel = 0
        self.ang_vel = 0

        self.sub_twist = rospy.Subscriber(topic, Twist, self.twist_callback)

    def twist_callback(self, data):

        self.lin_vel = data.linear.x
        self.ang_vel = data.angular.z

    #NOTE: this node has no input from nengo, so no 'x' parameter is used here
    def __call__(self, t):

        return self.lin_vel, self.ang_vel

model = nengo.Network('Environment', seed=13)
with model:
    velocity = nengo.Ensemble(n_neurons=100, dimensions=2)

    ros_subscriber = nengo.Node(TwistSubscriber(),
                               size_in=0,
                               size_out=2
                              )

    nengo.Connection(ros_subscriber, velocity)
