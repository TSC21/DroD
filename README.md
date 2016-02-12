# DroD
This is the ROS package for the DroD(Drowning Detection) project.

The Python scripts are all located at the [scripts](https://github.com/TSC21/DroD/tree/ROSifiet/scripts) folder.

## Setup:
### Recommends system:
- Ubuntu 14.04.3 with `3.19.*-generic` Kernel (check yours with `uname -a`)
- ROS Jade (`desktop-full` option)
- OpenCV3 ROS package (which is linked to on the `CMakeLists.txt` file)

### Install ROS
[http://wiki.ros.org/jade/Installation/Ubuntu](http://wiki.ros.org/jade/Installation/Ubuntu)

### Install Catkin Tools

```bash
sudo apt-get install python-catkin-tools
```

### Install OpenCV3 ROS package

```bash
sudo apt-get install ros-jade-opencv3
```

### Install usb-cam ROS package (optional for now - required for when we want to test it on real time stream)

```bash
sudo apt-get install ros-jade-usb-cam
```

### Setup your workspace

```bash
# Create a workspace dir on your $HOME dir - example:
mkdir -p ~/drod_ws/src
cd ~/drod_ws/src

# Clone the repository into it (for now let's keep it on my side repo)
git clone https://github.com/TSC21/DroD.git -b ROSifiet

# Init the repo
cd ~/drod_ws/src
catkin init

# Build the code
cd ~/drod_ws
catkin build
```

## Usage - just launch the node

```bash
roslaunch drod drodpy_pipeline.launch
```

### Copyright 2015-2016 © DroD team - All rights reserved
