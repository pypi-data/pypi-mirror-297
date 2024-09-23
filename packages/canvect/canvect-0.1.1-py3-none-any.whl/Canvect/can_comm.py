import can
import time
from .ring_buffer import RingBuffer

class CANBusHandler:
    def __init__(self, channel, interface, bitrate):
        """
        Initializes the CAN bus with the provided channel, interface, and bitrate.

        Parameters:
        - channel: The CAN channel to use (e.g., 'PCAN_USBBUS2').
        - interface: The CAN interface (e.g., 'pcan', 'socketcan').
        - bitrate: The bitrate for CAN communication (e.g., 500000).
        """
        try:
            self.bus = can.interface.Bus(channel=channel, interface=interface, bitrate=bitrate)
        except can.CanError as e:
            print(f"Failed to initialize CAN bus: {e}")
            raise e

    def shutdown(self):
        self.bus.shutdown()

def send_acceleration_message(bus, arbitration_id, data):
    """
    Send a CAN message for vehicle speed control.
    
    Parameters:
    - bus: CAN bus object
    - arbitration_id: CAN ID to send the message
    - data: List of 8 bytes (hex) to be sent in the message
    """
    message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print(f"Acceleration Message sent: ID=0x{arbitration_id:X}, Data: {' '.join(f'{byte:02X}' for byte in data)}")
    except can.CanError as e:
        print(f"Message not sent: {e}")

def continuous_acceleration_send(arbitration_id, channel, interface, bitrate):
    """
    Continuously send acceleration CAN messages with the specified parameters.
    
    Parameters:
    - arbitration_id: CAN ID to send the message.
    - channel: The CAN channel to use.
    - interface: The CAN interface (e.g., 'pcan' or 'socketcan').
    - bitrate: The bitrate for CAN communication.
    """
    
    # Validate that none of the parameters are None or empty
    if arbitration_id is None:
        raise ValueError("Arbitration ID is required.")
    if not channel:
        raise ValueError("Channel is required.")
    if not interface:
        raise ValueError("Interface is required.")
    if not bitrate:
        raise ValueError("Bitrate is required.")

    handler = CANBusHandler(channel=channel, interface=interface, bitrate=bitrate)
    bus = handler.bus
    acc_buffer = RingBuffer(capacity=10)

    seventh_byte = 0x00

    try:
        while True:
            # Task 1: Activate speed control mode, set speed to 2 m/s
            data_accel = [0x11, 0xC8, 0x00, 0x00, 0x00, 0x00, seventh_byte, 0x00]
            
            # Calculate checksum for Byte 7
            data_accel[7] = data_accel[0] ^ data_accel[1] ^ data_accel[2] ^ data_accel[3] ^ data_accel[4] ^ data_accel[5] ^ data_accel[6]

            # Append the message to the ring buffer
            acc_buffer.append(data_accel)  

            # Send the CAN message for vehicle speed control
            send_acceleration_message(bus, arbitration_id, data_accel)

            # Increment the seventh byte from 0x00 to 0x0F
            seventh_byte = (seventh_byte + 1) % 0x10

            time.sleep(0.01)  # Send every 10 ms

    except KeyboardInterrupt:
        print("Exiting Acceleration Control...")
    finally:
        handler.shutdown()
