import rclpy
from rclpy.node import Node
import numpy as np
import cv2

from unitree_go.msg import Go2FrontVideoData

class Go2CameraViewer(Node):
    def __init__(self):
        super().__init__('go2_camera_viewer')

        self.subscription = self.create_subscription(
            Go2FrontVideoData,
            '/frontvideostream',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        # Convert byte array to numpy
        np_data = np.frombuffer(bytes(msg.data), dtype=np.uint8)

        # Try decoding as JPEG
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("Go2 Camera", frame)
            cv2.waitKey(1)
        else:
            print("Frame decode failed (possibly not JPEG)")


def main():
    rclpy.init()
    node = Go2CameraViewer()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
