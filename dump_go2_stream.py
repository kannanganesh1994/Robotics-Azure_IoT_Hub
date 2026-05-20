import rclpy
from rclpy.node import Node
from unitree_go.msg import Go2FrontVideoData


class VideoDumper(Node):
    def __init__(self):
        super().__init__('video_dumper')

        # ✅ create output file
        self.file = open("go2_stream.h264", "wb")

        self.subscription = self.create_subscription(
            Go2FrontVideoData,
            '/frontvideostream',
            self.callback,
            10
        )

    def callback(self, msg):
        data = msg.video360p   # try 360p first

        if len(data) == 0:
            return

        # ✅ write raw bytes directly
        self.file.write(bytes(data))

        print("written:", len(data))


def main():
    rclpy.init()
    node = VideoDumper()
    rclpy.spin(node)

    node.file.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
