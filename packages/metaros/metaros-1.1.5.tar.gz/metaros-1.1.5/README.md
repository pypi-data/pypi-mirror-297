# Meta-ROS

# Zero-dependency ROS-like middleware for Python
This module acts as a middleware for communication between different processes using ZeroMQ. It consists of Publisher, Subscriber and MessageBroker classes to be able to publish and subscribe messages to a topic. The module contains different message types including string, int, float and more.

<p align="center">
    <a href="https://pypi.org/project/metaros/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/metaros">
    </a>
    <a href="https://github.com/AnshulRanjan2004/Meta-ROS/actions/workflows/python-publish.yml">
        <img alt="Wheels" src="https://github.com/AnshulRanjan2004/Meta-ROS/actions/workflows/python-publish.yml/badge.svg">
    </a>
    <a href="https://github.com/AnshulRanjan2004/Meta-ROS">
    	<img src="https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-blue.svg" alt="platforms" />
    </a>
    <a href="https://github.com/AnshulRanjan2004/Meta-ROS">
    	<img src="https://static.pepy.tech/badge/metaros" alt="Downloads" />
    </a>
    <a href="https://github.com/AnshulRanjan2004/Meta-ROS/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-BSD_3--Clause-blue.svg">
    </a>
    <br/>
</p>

## Why Meta-ROS?
A middleware solution designed for process communication, incorporating Publisher, Subscriber, and MessageBroker classes. It handles various message types, including strings, integers, and floats, facilitating seamless data exchange. This module fosters a cohesive and scalable robotics environment, driving innovation and research by enabling efficient communication and robust integration across different systems.

## Installation
To install the library, use pip:

```bash
pip install metaros
```

## Usage
The library is composed of three main classes: `Publisher`,  `Subscriber` and 
`MessageBroker`.

### MessageBroker
The `MessageBroker` class is used to create a message broker that can be used by
publishers and subscribers to communicate with each other.

```python
from metaros import MessageBroker

broker = MessageBroker()
```

### Publisher
The `Publisher` class is used to publish messages to a topic. The constructor takes two
arguments: the topic name and the message type. The topic name is a string, while the
message type is a Python class. The message type is used to serialize and deserialize
messages.

```python
from metaros import Publisher

pub = Publisher("topic_name", String)
pub.publish("Hello world!")
```

### Subscriber
The `Subscriber` class is used to subscribe to a topic and receive messages. The constructor
takes two arguments: the topic name and the message type. The topic name is a string, while
the message type is a Python class. The message type is used to serialize and deserialize
messages.

```python
import time
from metaros import Subscriber

def callback(msg):
    print(msg)

sub = Subscriber("topic_name", String, callback)
while True:
    # Do something else
    time.sleep(1)

# Stop the subscriber
sub.stop()
```

### Messages
The library comes with a few built-in messages that can be used out of the box. The
following messages are available:

* `std_msgs.String`
* `std_msgs.Int`
* `std_msgs.Float`
* `std_msgs.Bool`
* `std_msgs.Header`
* `geometry_msgs.Vector3`
* `geometry_msgs.Vector3Stamped`
* `geometry_msgs.Twist`
* `geometry_msgs.Quaternion`
* `geometry_msgs.Pose`
* `geometry_msgs.PoseStamped`
* `geometry_msgs.PoseWithCovariance`
* `geometry_msgs.TwistWithCovariance`
* `nav_msgs.Odometry`
* `nav_msgs.Path`
* `sensors_msgs.LaserScan`
* `sensors_msgs.Image`
* More to come...


