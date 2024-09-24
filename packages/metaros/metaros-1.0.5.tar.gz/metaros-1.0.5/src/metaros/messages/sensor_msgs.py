import numpy as np

from . import Message
from .std_msgs import Header


class LaserScan(Message):
    def __init__(self, ranges=[], intensitites=[], angles=[]):
        self.header = Header()
        self.angle_min = None
        self.angle_max = None
        self.angle_increment = None
        self.time_increment = None
        self.scan_time = None
        self.range_min = None
        self.range_max = None
        self.ranges = np.array(ranges)
        self.angles = np.array(angles)
        # Change NaNs to range_max
        if np.isnan(self.ranges).any():
            self.ranges[np.isnan(self.ranges)] = self.range_max
        self.intensities = np.array(intensitites)

    def __str__(self):
        msg = "LaserScan Message\n"
        msg += str(self.header)
        msg += "Angle Min:    " + str(self.angle_min) + "\n"
        msg += "Angle Max:    " + str(self.angle_max) + "\n"
        msg += "Angle Inc:    " + str(self.angle_increment) + "\n"
        msg += "Time Inc:     " + str(self.time_increment) + "\n"
        msg += "Scan Time:    " + str(self.scan_time) + "\n"
        msg += "Range Min:    " + str(self.range_min) + "\n"
        msg += "Range Max:    " + str(self.range_max) + "\n"
        msg += "Ranges:       " + str(self.ranges) + "\n"
        msg += "Intensities:  " + str(self.intensities) + "\n"
        msg += "Angles:       " + str(self.angles) + "\n"
        return msg

    def to_json(self):
        return {
            "header": self.header.to_json(),
            "angle_min": self.angle_min,
            "angle_max": self.angle_max,
            "angle_increment": self.angle_increment,
            "time_increment": self.time_increment,
            "scan_time": self.scan_time,
            "range_min": self.range_min,
            "range_max": self.range_max,
            "ranges": self.ranges.tolist(),
            "intensities": self.intensities.tolist(),
            "angles": self.angles.tolist(),
        }

    def from_json(self, msg):
        self.header.from_json(msg["header"])
        self.angle_min = msg["angle_min"]
        self.angle_max = msg["angle_max"]
        self.angle_increment = msg["angle_increment"]
        self.time_increment = msg["time_increment"]
        self.scan_time = msg["scan_time"]
        self.range_min = msg["range_min"]
        self.range_max = msg["range_max"]
        self.ranges = np.array(msg["ranges"])
        self.intensities = np.array(msg["intensities"])
        self.angles = np.array(msg["angles"])

class Image(Message):
    def __init__(self, height=None, width=None, encoding="", is_bigendian=0, step=0, data=[]):
        self.header = Header()  # Initialize header
        self.height = height    # Number of rows
        self.width = width      # Number of columns
        self.encoding = encoding  # Encoding of pixels (e.g., RGB8, BGR8)
        self.is_bigendian = is_bigendian  # Is the data in big-endian format?
        self.step = step  # Full row length in bytes
        self.data = np.array(data, dtype=np.uint8).reshape((height, step)) if data else np.array([])  # Actual matrix data

    def __str__(self):
        msg = "Image Message\n"
        msg += str(self.header)
        msg += "Height:       " + str(self.height) + "\n"
        msg += "Width:        " + str(self.width) + "\n"
        msg += "Encoding:     " + str(self.encoding) + "\n"
        msg += "Is Bigendian: " + str(self.is_bigendian) + "\n"
        msg += "Step:         " + str(self.step) + "\n"
        msg += "Data:         " + str(self.data) + "\n"
        return msg

    def to_json(self):
        return {
            "header": self.header.to_json(),
            "height": self.height,
            "width": self.width,
            "encoding": self.encoding,
            "is_bigendian": self.is_bigendian,
            "step": self.step,
            "data": self.data.flatten().tolist(),
        }

    def from_json(self, msg):
        self.header.from_json(msg["header"])
        self.height = msg["height"]
        self.width = msg["width"]
        self.encoding = msg["encoding"]
        self.is_bigendian = msg["is_bigendian"]
        self.step = msg["step"]
        self.data = np.array(msg["data"], dtype=np.uint8).reshape((self.height, self.step))