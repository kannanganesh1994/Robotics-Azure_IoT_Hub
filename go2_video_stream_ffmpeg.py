import rclpy
from rclpy.node import Node
from unitree_go.msg import Go2FrontVideoData
import subprocess
import numpy as np
import cv2


class Go2CameraViewer(Node):
    def __init__(self):
        super().__init__('go2_camera_viewer')

        self.proc = subprocess.Popen(
            [
                'ffmpeg',
                '-fflags', 'nobuffer',         # ✅ low latency
                '-flags', 'low_delay',
                '-f', 'h264',                 # ✅ specify input format
                '-i', '-',                    # stdin
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

        self.subscription = self.create_subscription(
            Go2FrontVideoData,
            '/frontvideostream',
            self.callback,
            10
        )

    def callback(self, msg):
        data = msg.video720p

        if len(data) == 0:
            return

        try:
            self.proc.stdin.write(bytes(data))

            frame_size = self.width * self.height * 3

            # ✅ NON-BLOCKING SAFE READ
            raw_frame = self.proc.stdout.read(frame_size)

            if len(raw_frame) == frame_size:
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




# import rclpy
# from rclpy.node import Node
# from unitree_go.msg import Go2FrontVideoData
# import subprocess
# import numpy as np
# import cv2


# class Go2CameraViewer(Node):
#     def __init__(self):
#         super().__init__('go2_camera_viewer')

#         self.proc = subprocess.Popen(
#             [
#                 'ffmpeg',
#                 '-i', '-',
#                 '-f', 'rawvideo',
#                 '-pix_fmt', 'bgr24',
#                 '-'
#             ],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.DEVNULL,
#             bufsize=10**8
#         )

#         # ✅ 720p resolution
#         self.width = 1280
#         self.height = 720

#         self.subscription = self.create_subscription(
#             Go2FrontVideoData,
#             '/frontvideostream',
#             self.callback,
#             10
#         )

#     def callback(self, msg):
#         data = msg.video720p  # ✅ switch here

#         if len(data) == 0:
#             return

#         try:
#             self.proc.stdin.write(bytes(data))

#             frame_size = self.width * self.height * 3
#             raw_frame = self.proc.stdout.read(frame_size)

#             if len(raw_frame) == frame_size:
#                 frame = np.frombuffer(raw_frame, dtype=np.uint8)
#                 frame = frame.reshape((self.height, self.width, 3))

#                 cv2.imshow("Go2 Camera 720p", frame)
#                 cv2.waitKey(1)

#         except Exception:
#             pass


# def main():
#     rclpy.init()
#     node = Go2CameraViewer()
#     rclpy.spin(node)

#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()





# import rclpy
# from rclpy.node import Node
# from unitree_go.msg import Go2FrontVideoData
# import subprocess
# import numpy as np
# import cv2


# class Go2CameraViewer(Node):
#     def __init__(self):
#         super().__init__('go2_camera_viewer')

#         # ✅ Start FFmpeg process
#         self.proc = subprocess.Popen(
#             [
#                 'ffmpeg',
#                 '-i', '-',          # input from pipe
#                 '-f', 'rawvideo',
#                 '-pix_fmt', 'bgr24',
#                 '-'
#             ],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.DEVNULL,
#             bufsize=10**8
#         )

#         self.width = 640  # adjust if needed
#         self.height = 360

#         self.subscription = self.create_subscription(
#             Go2FrontVideoData,
#             '/frontvideostream',
#             self.callback,
#             10
#         )

#     def callback(self, msg):
#         data = msg.video360p

#         if len(data) == 0:
#             return

#         try:
#             # ✅ send raw stream to ffmpeg
#             self.proc.stdin.write(bytes(data))

#             # ✅ read decoded frame
#             frame_size = self.width * self.height * 3
#             raw_frame = self.proc.stdout.read(frame_size)

#             if len(raw_frame) == frame_size:
#                 frame = np.frombuffer(raw_frame, dtype=np.uint8)
#                 frame = frame.reshape((self.height, self.width, 3))

#                 cv2.imshow("Go2 Camera", frame)
#                 cv2.waitKey(1)

#         except Exception:
#             pass


# def main():
#     rclpy.init()
#     node = Go2CameraViewer()
#     rclpy.spin(node)

#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
