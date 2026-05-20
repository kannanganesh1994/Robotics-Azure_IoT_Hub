import rclpy
from rclpy.node import Node
from unitree_go.msg import Go2FrontVideoData
import subprocess


class VideoDumper(Node):
    def __init__(self):
        super().__init__('video_dumper')

        # ✅ Start FFmpeg process
        self.proc = subprocess.Popen(
            [
                'ffmpeg',
                '-fflags', 'nobuffer',
                '-flags', 'low_delay',
                '-f', 'h264',     # assume H264 input
                '-i', '-',
                '-c:v', 'copy',   # no re-encode
                '-f', 'mp4',
                'go2_output.mp4'
            ],
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

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

        try:
            self.proc.stdin.write(bytes(data))
            print("written:", len(data))
        except Exception:
            pass


def main():
    rclpy.init()
    node = VideoDumper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.proc.stdin.close()
    node.proc.wait()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
