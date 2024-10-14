import sys
import time
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

# =======================
# Functions
# =======================

# Function to read holding registers from Diris A-40
def read_register(register, unit=1, count=2):
    """
    Reads registers from the Diris A-40 Modbus device.
    Args:
        register (int): The register to read from.
        unit (int): The Modbus unit ID (default is 1).
        count (int): The number of registers to read (default is 2 for 32-bit values).
    Returns:
        float: The value retrieved from the registers after decoding.
    """
    result = client.read_holding_registers(register, count, unit=unit)
    if result.isError():
        print(f"Error reading register {register}")
        return None
    return result.registers

# Function to decode and return the 32-bit floating point value
def decode_32bit_float(registers):
    decoder = BinaryPayloadDecoder.fromRegisters(registers, byteorder=Endian.Big, wordorder=Endian.Big)
    return decoder.decode_32bit_float()

# Function to read voltage, current, and power from Diris A-40
def read_diris_data():
    print("Reading data from Diris A-40...")

    # Define Modbus registers (example register addresses)
    registers = {
        'voltage_phase_1': 51284,  # Placeholder register
        'voltage_phase_2': 51285,  # Placeholder register
        'voltage_phase_3': 51286,  # Placeholder register
        'frequency': 51287,        # Placeholder register
        'active_power': 50536,     # Placeholder register
        'reactive_power': 50538    # Placeholder register
    }

    # Reading voltage phase 1 (example)
    voltage_1_registers = read_register(registers['voltage_phase_1'])
    if voltage_1_registers:
        voltage_1 = decode_32bit_float(voltage_1_registers)
        print(f"Voltage Phase 1: {voltage_1} V")

    # Reading frequency
    frequency_registers = read_register(registers['frequency'])
    if frequency_registers:
        frequency = decode_32bit_float(frequency_registers)
        print(f"Frequency: {frequency} Hz")

    # Reading active power
    active_power_registers = read_register(registers['active_power'])
    if active_power_registers:
        active_power = decode_32bit_float(active_power_registers)
        print(f"Active Power: {active_power} W")

    # Add more reads for reactive power, voltage phase 2/3, and others as needed.

# =======================
# Initialization
# =======================

# Device connection information
socomec_ip = '192.168.1.100'  # Replace with actual IP of your Diris A-40
modbus_port = 502  # Default Modbus TCP port

# Initialize Modbus client
client = ModbusTcpClient(socomec_ip, port=modbus_port)
connection_status = client.connect()

if connection_status:
    print("Connected to Diris A-40.")
else:
    print("Failed to connect to Diris A-40.")
    sys.exit(1)

# =======================
# Main Loop (Retrieve Data)
# =======================
try:
    while True:
        read_diris_data()
        time.sleep(10)  # Retrieve data every 10 seconds (adjust as needed)
except KeyboardInterrupt:
    print("Script interrupted. Exiting...")

# Close the client connection when done
client.close()
