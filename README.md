# IntuitControl

Start ROS 2 development in a container
// Dockerfile and compose.yml
- Builds the container
> docker compose up -d

// Closing the container
> docker stop <container_name>

- Starts the container
> docker compose exec ros2 /bin/bash

// Execute commands inside the container
> docker compose exec ros2 /bin/bash 
> docker compose exec ros2 <command>

// Opening container terminal 
> docker exec -it <container_name> bash

// Enabling xhost to docker
@ Local machine
> xhost +local:docker 

// Disabling xhost for docker
@ Local machine
> xhost -local:docker 

// Run Command to run a container from the built ROS 2 image
> docker run -it --env="DISPLAY=$DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device /dev/snd --net=host <name_of_image> bash

// Before using ROS
> sudo apt update

// Using ROS2 With Docker
https://docs.docker.com/guides/ros2/
