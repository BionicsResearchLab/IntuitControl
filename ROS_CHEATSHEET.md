
// rqt_graph
// Installation
> sudo apt install -y 'ros-humble-rqt*'
// Run rqt_graph
> ros2 run rqt_gui rqt_gui

// Important Steps: Build Workspace
> cd /opt/ros/humble/setup.bash
// Ensure chown owndership
> sudo chown -R $USER:$USER /home/ws
> colcon build --symlink-install

