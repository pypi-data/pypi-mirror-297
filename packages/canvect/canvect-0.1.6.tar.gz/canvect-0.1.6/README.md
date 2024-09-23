# Canvect v0.1.5 Release Notes
Canvect is a Python package designed for sending and managing CAN (Controller Area Network) messages
# Overiew
Updated version adds advantage and seamless integration of Pcan and Socketcan as interfaces  related to Actuation control of vechile. It provides a simple yet flexible API for creating and dispatching CAN messages, making it ideal for applications in automotive and industrial systems where CAN communication is essential.

# New Features
1. Dynamic Parameter Input: Users can now input dynamic parameters for the following

- arbitration_id: Specify the CAN ID as a hexadecimal value.
- seventh_byte: Set the seventh byte for the CAN message (value between 0-15).
- channel: Define the CAN channel (e.g., 'PCAN_USBBUS2').
- interface: Choose the CAN interface (e.g., 'pcan').
- bitrate: Set the bitrate for the CAN bus communication (e.g., 500000).

This enhancement allows users to customize their CAN message sending directly from input prompts, making the package more versatile and user-friendly.

## Installation

```bash
pip install canvect==0.1.6

```

## Sample Usage Examples

1. You can now easily modify parameters like arbitration_id, bitrate, and channel to suit your specific needs:ds

```bash 
from Canvect import continuous_acceleration_send

continuous_acceleration_send(
    arbitration_id=int(input("Enter arbitration ID (hex): "), 16),  # Custom CAN ID
    seventh_byte=int(input("Enter the value for the seventh byte (0-15): ")),  # Seventh byte
    channel=input("Enter CAN channel (e.g., 'PCAN_USBBUS2'): "),  # Custom CAN channel
    interface=input("Enter CAN interface (e.g., 'pcan'): "),  # Custom interface
    bitrate=int(input("Enter bitrate (e.g., 500000): "))  # Custom bitrate
)

```


## Example with RingBuffer

```bash 
from Canvect import RingBuffer

# Create a RingBuffer with a capacity of 5 items
buffer = RingBuffer(capacity=5)

# Append items to the buffer
for i in range(10):
    buffer.append(f"message_{i}")
    print(f"Buffer after appending message_{i}: {buffer}")

# Access items by index
for i in range(len(buffer)):
    print(f"Item at index {i}: {buffer[i]}")


```
1. The buffer can hold up to 5 items. Once it reaches the maximum capacity, new items will overwrite the oldest ones.

2. You can access items using their index. If you try to access an index that is out of range, an IndexError will be raised.

Note: Here refers to above example


## Terminal SPecific Sample1 Code to Send..
```bash 
from Canvect import continuous_Canvect_message

if __name__ == "__main__":
    # User inputs (same as your original code)
    arbitration_id = int(input("Enter arbitration ID (hex): "), 16)
    seventh_byte = int(input("Enter the value for the seventh byte (0-15): "), 16)
    channel = input("Enter CAN channel (e.g., 'PCAN_USBBUS2'): ")
    interface = input("Enter CAN interface (e.g., 'pcan'): ")
    bitrate = int(input("Enter bitrate (e.g., 500000): "))
    buffer_capacity = int(input("Enter ring buffer capacity: "))
    
    data_accel = [
        int(input("Enter Byte 0: "), 16),
        int(input("Enter Byte 1: "), 16),
        int(input("Enter Byte 2: "), 16),
        int(input("Enter Byte 3: "), 16),
        int(input("Enter Byte 4: "), 16),
        int(input("Enter Byte 5: "), 16),
        seventh_byte,
        0  # Placeholder for Byte 7
    ]

    sleep_time = float(input("Enter sleep time (in seconds): "))

    continuous_Canvect_message(
        arbitration_id=arbitration_id,
        seventh_byte=seventh_byte,
        channel=channel,
        interface=interface,
        bitrate=bitrate,
        data_accel=data_accel,
        sleep_time=sleep_time,
        buffer_capacity=buffer_capacity
    )

```

## HARDCODED CAN Sample2
```bash
from Canvect import continuous_Canvect_message

if __name__ == "__main__":
    # Fixed values for the parameters
    arbitration_id = 0x123  # Replace with your desired arbitration ID
    seventh_byte = 0x0A  # Replace with your desired value for the seventh byte
    channel = 'PCAN_USBBUS2'  # Replace with your actual CAN channel
    interface = 'pcan'  # Replace with your actual CAN interface
    bitrate = 500000  # Replace with your desired bitrate
    buffer_capacity = 10  # Set your desired ring buffer capacity

    data_accel = [
        0x01,  # Byte 0
        0x02,  # Byte 1
        0x03,  # Byte 2
        0x04,  # Byte 3
        0x05,  # Byte 4
        0x06,  # Byte 5
        seventh_byte,  # Seventh byte (fixed)
        0  # Placeholder for Byte 7 (will be calculated)
    ]

    sleep_time = 1.0  # Fixed sleep time in seconds

    # Start sending CAN frames
    continuous_Canvect_message(
        arbitration_id=arbitration_id,
        seventh_byte=seventh_byte,
        channel=channel,
        interface=interface,
        bitrate=bitrate,
        data_accel=data_accel,
        sleep_time=sleep_time,
        buffer_capacity=buffer_capacity
    )


```