import rclpy
from rclpy.node import Node
from unitree_go.msg import Go2FrontVideoData

import subprocess
import numpy as np
import cv2
import threading


class Go2CameraViewer(Node):
    def __init__(self):
        super().__init__('go2_camera_viewer')

        self.proc = subprocess.Popen(
            [
                'ffmpeg',
                '-fflags', 'nobuffer',
                '-flags', 'low_delay',
                '-f', 'h264',
                '-i', '-',
                '-f', 'rawvideo',
                '-pix_fmt', 'bgr24',
                '-'
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=10**8
        )

        self.width = 1280
        self.height = 720

        # ✅ Start frame reader thread
        self.thread = threading.Thread(target=self.read_frames, daemon=True)
        self.thread.start()

        self.subscription = self.create_subscription(
            Go2FrontVideoData,
            '/frontvideostream',
            self.callback,
            10
        )

    # ✅ ROS callback → only write input
    def callback(self, msg):
        data = msg.video720p

        if len(data) == 0:
            return

        try:
            self.proc.stdin.write(bytes(data))
        except Exception:
            pass

    # ✅ Dedicated thread → read decoded frames
    def read_frames(self):
        frame_size = self.width * self.height * 3

        while True:
            try:
                raw_frame = self.proc.stdout.read(frame_size)

                if len(raw_frame) != frame_size:
                    continue

                frame = np.frombuffer(raw_frame, dtype=np.uint8)
                frame = frame.reshape((self.height, self.width, 3))

                cv2.imshow("Go2 Camera", frame)
                cv2.waitKey(1)

            except Exception:
                pass


def main():
    rclpy.init()
    node = Go2CameraViewer()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
