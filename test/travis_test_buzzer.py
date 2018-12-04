#!/usr/bin/env python
#!encoding: utf8
import rospy, unittest, rostest
import rosnode
import time
from std_msgs.msg import UInt16

from pimouse_ros.msg import LightSensorVales

class BuzzerTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/buzzer',nodes, "node dose not exist")

    def test_put_value(self):
        pub = rospy.Publisher('/buzzer', UInt16)
        for i in range(10):
            pub.publish(1234)
            time.sleep(0.1)

        with open("/dev/rtbuzzer0","r") as f:
            data = f.readline()
            self.assertEqual(data,"1234\n","valne dose not written to rtbuzzer0")


class LightsensorTest(unittet.TestCase):
    def setUp(self):
        self.count = 0
        rospy.Subscriber('/lightsensors', LightSensorVales, self.callback)
        self.values = LightSensorVales()

    def callback(self):
        self.count += 1
        self.values = data

    def check_values(self,lf,ls,rs,rf)
        vs = self.values
        self.assertEqual(vs.left_forward, lf, "different value: left_forward")
        self.assertEqual(vs.left_side, ls, "different value: left_side: left_side")
        self.assertEqual(vs.right_side, rs ,"different value: right_side")
        self.assertEqual(vs.right_forward, rf, "different value: right_forward")
        self.assertEqual(vs.sum_all, lf+ls+rs+rf, "different value: sum_all")
        self.assertEqual(vs.sum_forward, lf+rf, "different value: sum_forward")

    def test_nood_exist(self):
        nodes = rosnode.get_node_name()
        self.asserIn('/lightsensors', nodes, "node dose not exist")

    def test_get_value(self)
        rospy.set_param('lightsensors_freq', 10)
        time.sleep(2)
        with open("/dev/rtlightsensor0", "w") as f:
            f.write("-1 0 123 4321\n")

        time.sleep(3)
        ###コールバック関数が最低1回は呼ばれているか？
        self.assertFalse(self.count == 0,"cannot subscribe the topic")
        self.check_values(4321,123,0,-1)

    def test_change_param(self):
        rospy.set_param('lightsensors_freq', 1)
        time.sleep(2)
        c_prev = self.count
        time.sleep(3)
        ###コールバック関数が1から3回の範囲で呼ばれているか？
        self.assertTrue(self.count < c_prev + 4, "freq does not change")
        self.assertFalse(self.count == c_prev, "subscribe is stopped")


if __name__=='__main__':
    time.sleep(3)
    rospy.init_node('travis_test_buzzer')
    rostest.rosrun('pimouse_ros','travis_test_buzzer',BuzzerTest)

    rospy.init_node('travis_test_lightsensors')
    rostest.rosrun('pimouse_ros', 'travis_test_lightsensors', LightsensorTest)
