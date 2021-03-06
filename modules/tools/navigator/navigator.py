#!/usr/bin/env python

###############################################################################
# Copyright 2017 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import rospy
import sys
import json
from modules.map.relative_map.proto import navigation_pb2

if __name__ == '__main__':
    fdata = sys.argv[1]
    rospy.init_node("navigator3", anonymous=True)
    navigation_pub = rospy.Publisher(
        "/apollo/navigation", navigation_pb2.NavigationInfo, queue_size=1)

    navigation_info = navigation_pb2.NavigationInfo()
    navigation_path = navigation_info.navigation_path.add()
    navigation_path.path_priority = 0
    navigation_path.path.name = "navigation"
    f = open(fdata, 'r')
    for line in f:
        json_point = json.loads(line)
        point = navigation_path.path.path_point.add()
        point.x = json_point['x']
        point.y = json_point['y']
        point.s = json_point['s']
        point.theta = json_point['theta']
        point.kappa = json_point['kappa']
        point.dkappa = json_point['dkappa']
    f.close()
    print navigation_info
    r = rospy.Rate(1)  # 1hz
    while not rospy.is_shutdown():
        r.sleep()
        navigation_pub.publish(navigation_info)
        break
