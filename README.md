mash
====

Generate build recipes based on catkin package manifest (package.xml)  [format 2](https://www.ros.org/reps/rep-0140.html).

It is a standalone application that uses the colcon extensions to discover packages in a workspace.  It then reads the package manifest to get the metadata needed to create the [BitBake](https://docs.yoctoproject.org/bitbake/) recipe.

# Why mash?

The ROS tooling has a naming scheme based on willow trees and the OpenEmbedded tools use a cooking theme. The name matches both schemes and also makes a convenient action verb for a command-line tool.

"Poor people at one time often ate willow catkins that had been cooked to form a mash." <https://en.wikipedia.org/wiki/Willow>

# Installation

```
python3 -m venv myenv
source myenv/bin/activate
pip install ros-mash colcon-common-extensions
```

To install from source instead:

```
git clone https://github.com/robwoolley/ros-mash.git
cd ros-mash
python3 -m venv myenv
source myenv/bin/activate
pip install colcon-common-extensions
pip install .
```

# Usage

If you already have a ROS 2 environment, you may skip to step 3.

1. Use Docker to pull the official ROS 2 Humble container image.

```
docker run -it --rm amd64/ros:humble
```

2. Install the package for Python venv support:
```
apt update
apt install -y python3.10-venv
```

3. Create a workspace with mash with some demonstration examples.

```
source /opt/ros/humble/setup.bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/ros/ros_tutorials.git -b humble
git clone https://github.com/ros2/demos.git -b humble
cd ..
```

4. Install mash with venv
```
python3 -m venv myenv
source myenv/bin/activate
pip install ros-mash colcon-common-extensions
```

5. Run mash in the colcon workspace to create BitBake recipes.
```
mash --rosdistro $ROS_DISTRO
```

6. Find the generated bitbake recipes under build_mash:
```
(myenv) root@25037274df1a:~/ros2_ws# find build_mash -type f
build_mash/action_tutorials_cpp/action-tutorials-cpp_0.20.7.bb
build_mash/intra_process_demo/intra-process-demo_0.20.7.bb
build_mash/demo_nodes_cpp_native/demo-nodes-cpp-native_0.20.7.bb
build_mash/demo_nodes_py/demo-nodes-py_0.20.7.bb
build_mash/topic_statistics_demo/topic-statistics-demo_0.20.7.bb
build_mash/pendulum_msgs/pendulum-msgs_0.20.7.bb
build_mash/quality_of_service_demo_cpp/quality-of-service-demo-cpp_0.20.7.bb
build_mash/topic_monitor/topic-monitor_0.20.7.bb
build_mash/dummy_robot_bringup/dummy-robot-bringup_0.20.7.bb
build_mash/logging_demo/logging-demo_0.20.7.bb
build_mash/lifecycle_py/lifecycle-py_0.20.7.bb
build_mash/action_tutorials_py/action-tutorials-py_0.20.7.bb
build_mash/dummy_sensors/dummy-sensors_0.20.7.bb
build_mash/composition/composition_0.20.7.bb
build_mash/pendulum_control/pendulum-control_0.20.7.bb
build_mash/turtlesim/turtlesim_1.4.3.bb
build_mash/demo_nodes_cpp/demo-nodes-cpp_0.20.7.bb
build_mash/quality_of_service_demo_py/quality-of-service-demo-py_0.20.7.bb
build_mash/lifecycle/lifecycle_0.20.7.bb
build_mash/action_tutorials_interfaces/action-tutorials-interfaces_0.20.7.bb
build_mash/dummy_map_server/dummy-map-server_0.20.7.bb
build_mash/image_tools/image-tools_0.20.7.bb
```

6. (Optional) If mash fails to find any ROS packages, you may try building the colcon workspace to see if colcon can discover the packages.

```
rosdep install -i --from-path src --rosdistro humble -y
colcon build
```

# Contributing

Any contribution that you make to this repository will be under the [Apache 2.0 License](LICENSE), unless explicitly stated otherwise.

Contributors must sign-off each commit by adding a `Signed-off-by: ...` line to commit messages to certify that they have the right to submit the code they are contributing to the project according to the [Developer Certificate of Origin (DCO)](https://developercertificate.org/).

# License

The source code for this project is under the Apache 2.0 license.  Text for the license can be found in the LICENSE file in the project top level directory.  Dependencies may be under different licenses.
