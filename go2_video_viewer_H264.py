import rclpy
from rclpy.node import Node
import av
import numpy as np
import cv2

from unitree_go.msg import Go2FrontVideoData


class Go2CameraViewer(Node):
    def __init__(self):
        super().__init__('go2_camera_viewer')

        self.codec = av.CodecContext.create('h264', 'r')

        self.subscription = self.create_subscription(
            Go2FrontVideoData,
            '/frontvideostream',
            self.callback,
            10
        )

    def callback(self, msg):
        data = msg.video360p  # or video720p

        if len(data) == 0:
            return

        packet = av.Packet(bytes(data))

        try:
            frames = self.codec.decode(packet)
        except Exception as e:
            print("Decode error:", e)
            return

        for frame in frames:
            img = frame.to_ndarray(format='bgr24')
            cv2.imshow("Go2 Camera", img)
            cv2.waitKey(1)


def main():
    rclpy.init()
    node = Go2CameraViewer()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
