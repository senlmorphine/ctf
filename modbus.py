import time
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

# Initialize Modbus client
client = ModbusTcpClient('192.168.101.44')  # Replace with the correct IP

# Connect to the device
if client.connect():
    print("Connected to Socomec.")
else:
    print("Connection to Socomec failed.")
    exit()

# Function to read U32 register (2 words)
def read_u32_register(register, unit_id):
    result = client.read_holding_registers(register, 2, slave=unit_id)
    if result.isError():
        print(f"Error reading register {register} with unit ID {unit_id}")
        return None

    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.BIG)
    value = decoder.decode_32bit_uint()
    return value

# Function to read relevant registers (Frequency, Voltage, Intensity)
def read_relevant_registers(unit_id):
    # Define registers, scaling factors, and units
    registers = {
        'Voltage Phase 1 (V1)': (36867, 10**-2, "V"),  # Register, scaling factor, unit
        'Frequency': (36871, 10**-3, "Hz"),  # Corrected scaling factor for frequency
        'Current Phase 1 (I1)': (50540, 10**-2, "A"),  # Placeholder register for intensity, update as needed
    }

    # Loop through the registers, read, and print the values
    for description, (register, scale, unit) in registers.items():
        value = read_u32_register(register, unit_id)
        if value is not None:
            value = value * scale  # Apply scaling factor
            print(f"{description}: {value} {unit}")
        else:
            print(f"Failed to read {description}")

# Main loop to continuously read the relevant registers
unit_id = 5  # Modbus address set to 005 after reset

try:
    while True:
        print("\nReading SOCOMEC DIRIS A-40 Data (Frequency, Voltage, and Intensity):")
        read_relevant_registers(unit_id)
        print("====================================")
        time.sleep(5)  # Wait for 5 seconds before reading again (adjust as needed)

except KeyboardInterrupt:
    print("\nScript interrupted by user. Exiting...")

finally:
    client.close()
