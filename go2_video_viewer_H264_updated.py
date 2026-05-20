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
        self.buffer = b''

        self.subscription = self.create_subscription(
            Go2FrontVideoData,
            '/frontvideostream',
            self.callback,
            10
        )

    def callback(self, msg):
        data = msg.video360p  # ✅ use 360p first

        if len(data) == 0:
            return

        # ✅ accumulate continuously (DO NOT RESET EARLY)
        self.buffer += bytes(data)

        try:
            packet = av.Packet(self.buffer)
            frames = self.codec.decode(packet)

            # ✅ show only valid frames
            for frame in frames:
                img = frame.to_ndarray(format='bgr24')

                # ✅ Avoid green/invalid frames
                if img is not None and img.shape[0] > 0:
                    cv2.imshow("Go2 Camera", img)
                    cv2.waitKey(1)

            # ✅ ONLY trim buffer slightly (DO NOT CLEAR)
            if len(self.buffer) > 500000:   # avoid infinite growth
                self.buffer = self.buffer[-200000:]

        except Exception:
            # ✅ ignore incomplete packets silently
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
# import av
# import numpy as np
# import cv2

# from unitree_go.msg import Go2FrontVideoData


# class Go2CameraViewer(Node):
#     def __init__(self):
#         super().__init__('go2_camera_viewer')

#         self.codec = av.CodecContext.create('h264', 'r')
#         self.buffer = b''   # ✅ IMPORTANT: persistent buffer

#         self.subscription = self.create_subscription(
#             Go2FrontVideoData,
#             '/frontvideostream',
#             self.callback,
#             10
#         )

#     def callback(self, msg):
#         data = msg.video360p   # use 360p first

#         if len(data) == 0:
#             return

#         # ✅ accumulate stream
#         self.buffer += bytes(data)

#         try:
#             packet = av.Packet(self.buffer)
#             frames = self.codec.decode(packet)

#             for frame in frames:
#                 img = frame.to_ndarray(format='bgr24')
#                 cv2.imshow("Go2 Camera", img)
#                 cv2.waitKey(1)

#             # ✅ Clear buffer AFTER successful decode
#             if len(frames) > 0:
#                 self.buffer = b''

#         except Exception:
#             # ✅ DO NOT spam errors — just wait for complete frame
#             pass


# def main():
#     rclpy.init()
#     node = Go2CameraViewer()
#     rclpy.spin(node)

#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
