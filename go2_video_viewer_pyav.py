import rclpy
from rclpy.node import Node
from unitree_go.msg import Go2FrontVideoData

import av
import cv2


class Go2CameraViewer(Node):
    def __init__(self):
        super().__init__('go2_camera_viewer')

        # ✅ H264 decoder
        self.codec = av.CodecContext.create('h264', 'r')
        self.codec.options = {'flags': 'low_delay'}

        self.subscription = self.create_subscription(
            Go2FrontVideoData,
            '/frontvideostream',
            self.callback,
            10
        )
    
    def callback(self, msg):
            # Using 720p as specified in your code
            data = msg.video720p
            
            # Skip empty payloads
            if not data or len(data) < 100:
                return
    
            try:
                # ✅ FIX: Parse the raw bitstream into valid packets first
                packets = self.codec.parse(bytes(data))
                
                for packet in packets:
                    # Decode the properly parsed packet
                    frames = self.codec.decode(packet)
    
                    for frame in frames:
                        try:
                            # Convert to BGR for OpenCV
                            rgb = frame.to_ndarray(format='rgb24')
                            img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    
                            h, w, _ = img.shape
    
                            # Filter out invalid or tiny frames
                            if h > 100 and w > 100:
                                cv2.imshow("Go2 Camera", img)
                                cv2.waitKey(1)
    
                        except Exception as e:
                            pass # Handle individual frame conversion errors
    
            except Exception as e:
                pass # Handle parsing/decoding errors

    # def callback(self, msg):
    #     # ✅ Start with 360p (more stable)
    #     data = msg.video360p

    #     if len(data) < 100:   # ✅ skip tiny fragments
    #         return

    #     try:
    #         packet = av.Packet(bytes(data))
    #         frames = self.codec.decode(packet)

    #         for frame in frames:
    #             try:
    #                 # ✅ Correct conversion (fix green issue)
    #                 rgb = frame.to_ndarray(format='rgb24')
    #                 img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    #                 h, w, _ = img.shape

    #                 # ✅ filter invalid frames
    #                 if h > 100 and w > 100:
    #                     cv2.imshow("Go2 Camera", img)
    #                     cv2.waitKey(1)

    #             except Exception:
    #                 pass

    #     except Exception:
    #         pass


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

# import av
# import cv2


# class Go2CameraViewer(Node):
#     def __init__(self):
#         super().__init__('go2_camera_viewer')

#         # ✅ H264 decoder
#         self.codec = av.CodecContext.create('h264', 'r')
#         self.codec.options = {'flags': 'low_delay'}

#         self.subscription = self.create_subscription(
#             Go2FrontVideoData,
#             '/frontvideostream',
#             self.callback,
#             10
#         )

#     def callback(self, msg):
#         # ✅ Start with 360p (more stable)
#         data = msg.video360p

#         if len(data) < 100:   # ✅ skip tiny fragments
#             return

#         try:
#             packet = av.Packet(bytes(data))
#             frames = self.codec.decode(packet)

#             for frame in frames:
            
#                 # ✅ Skip non-keyframes initially
#                 if not frame.key_frame:
#                     continue
            
#                 rgb = frame.to_ndarray(format='rgb24')
#                 img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            
#                 cv2.imshow("Go2 Camera", img)
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

# import av
# import cv2


# class Go2CameraViewer(Node):
#     def __init__(self):
#         super().__init__('go2_camera_viewer')

#         # ✅ H264 decoder
#         self.codec = av.CodecContext.create('h264', 'r')
#         self.codec.options = {'flags': 'low_delay'}

#         self.subscription = self.create_subscription(
#             Go2FrontVideoData,
#             '/frontvideostream',
#             self.callback,
#             10
#         )

#     def callback(self, msg):
#         # ✅ Start with 360p (more stable)
#         data = msg.video360p

#         if len(data) < 100:   # ✅ skip tiny fragments
#             return

#         try:
#             packet = av.Packet(bytes(data))
#             frames = self.codec.decode(packet)

#             for frame in frames:
#                 try:
#                     # ✅ Correct conversion (fix green issue)
#                     rgb = frame.to_ndarray(format='rgb24')
#                     img = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

#                     h, w, _ = img.shape

#                     # ✅ filter invalid frames
#                     if h > 100 and w > 100:
#                         cv2.imshow("Go2 Camera", img)
#                         cv2.waitKey(1)

#                 except Exception:
#                     pass

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

# import av
# import numpy as np
# import cv2


# class Go2CameraViewer(Node):
#     def __init__(self):
#         super().__init__('go2_camera_viewer')

#         self.codec = av.CodecContext.create('h264', 'r')

#         self.subscription = self.create_subscription(
#             Go2FrontVideoData,
#             '/frontvideostream',
#             self.callback,
#             10
#         )

#     def callback(self, msg):
#         data = msg.video720p

#         if len(data) == 0:
#             return

#         try:
#             packet = av.Packet(bytes(data))

#             frames = self.codec.decode(packet)

#             for frame in frames:
#                 img = frame.to_ndarray(format='bgr24')

#                 if img is not None:
#                     cv2.imshow("Go2 Camera", img)
#                     cv2.waitKey(1)

#         except Exception:
#             # ✅ Ignore partial packet errors
#             pass


# def main():
#     rclpy.init()
#     node = Go2CameraViewer()
#     rclpy.spin(node)

#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
