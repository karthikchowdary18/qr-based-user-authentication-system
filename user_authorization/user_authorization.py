#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import Bool, String

from cv_bridge import CvBridge
from pyzbar.pyzbar import ZBarSymbol, decode


class UserAuthorization(Node):
    """
    User authorization using:
      - Server-approved login ID (/auth/login_id)
      - Manual input fallback (/auth/user_input)
      - QR code from RealSense RGB stream (/robot1/D455_1/color/image_raw)
    """

    def __init__(self):
        super().__init__('user_authorization')

        self.server_login_id = None
        self.last_state = None
        self.bridge = CvBridge()

        # Login ID from server
        self.create_subscription(
            String,
            '/auth/login_id',
            self.on_login_id,
            10,
        )

        # Manual input fallback
        self.create_subscription(
            String,
            '/auth/user_input',
            self.on_user_input,
            10,
        )

        # RealSense RGB image stream
        self.create_subscription(
            Image,
            '/robot1/D455_1/color/image_raw',
            self.on_image,
            10,
        )

        self.pub_auth_done = self.create_publisher(
            Bool,
            '/user_auth_done',
            10,
        )

        self.get_logger().info('User Authorization node started')

    def on_login_id(self, msg):
        """Receive approved login ID from server."""
        self.server_login_id = msg.data.strip()
        self.last_state = None
        self.get_logger().info(f'[SERVER LOGIN ID] {self.server_login_id}')

    def on_user_input(self, msg):
        """Handle manual user input as a fallback path."""
        if not self.server_login_id:
            return

        entered_id = msg.data.strip()
        self.get_logger().info(f'[MANUAL INPUT] {entered_id}')
        self.check_match(entered_id)

    def on_image(self, msg: Image):
        """Decode QR codes from the RealSense RGB stream."""
        if not self.server_login_id:
            return

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as exc:
            self.get_logger().error(f'cv_bridge error: {exc}')
            return

        decoded_objects = decode(frame, symbols=[ZBarSymbol.QRCODE])

        if not decoded_objects:
            return

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            self.get_logger().info(f'[QR FOUND] {qr_data}')

            if not qr_data.startswith('ELDRIVE:'):
                self.get_logger().warn(f'Invalid QR detected: {qr_data}')
                continue

            scanned_id = qr_data.split(':', 1)[1].strip()
            self.get_logger().info(f'[QR SCANNED] {scanned_id}')
            self.check_match(scanned_id)

    def check_match(self, received_id):
        """Compare a received ID with the server-approved login ID."""
        matched = received_id == self.server_login_id

        if matched == self.last_state:
            return

        self.last_state = matched

        if matched:
            self.get_logger().info('AUTH SUCCESS - DOOR UNLOCKED')
            self.pub_auth_done.publish(Bool(data=True))
        else:
            self.get_logger().warn('AUTH FAILED - WRONG USER')
            self.pub_auth_done.publish(Bool(data=False))


def main(args=None):
    rclpy.init(args=args)
    node = UserAuthorization()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
