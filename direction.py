from machine import ADC, Pin
import time

# Set up the ADC on the GPIO pin connected to the potentiometer
pot_pin = 26  # GPIO pin number
adc = ADC(Pin(pot_pin))

# Reference voltage (3.3V)
v_ref = 3.3

# Define the threshold values for each direction
north_voltage = 1.1
east_voltage = 0.3
south_voltage = 2.8
west_voltage = 2.0

# Define the tolerance for voltage comparisons
tolerance = 0.1  # You can adjust this value as needed

def determine_direction(voltage):
    """Determine the direction based on the input voltage."""
    if abs(voltage - north_voltage) <= tolerance:
        return "North"
    elif abs(voltage - east_voltage) <= tolerance:
        return "East"
    elif abs(voltage - south_voltage) <= tolerance:
        return "South"
    elif abs(voltage - west_voltage) <= tolerance:
        return "West"
    elif voltage > west_voltage and voltage < south_voltage:
        return "South West"
    elif voltage > north_voltage and voltage < west_voltage:
        return "North West"
    elif voltage > east_voltage and voltage < north_voltage:
        return "North East"
    else:
        return "South East"

while True:
    # Read the ADC value (0 to 65535)
    adc_value = adc.read_u16()
    
    # Convert the ADC value to voltage
    voltage = adc_value / 65535 * v_ref
    
    # Determine the direction based on the voltage
    direction = determine_direction(voltage)
    
    # Print the voltage and the determined direction
    print(f"Voltage: {voltage:.2f} V, Direction: {direction}")
    
    # Wait for a short time before the next reading
    time.sleep(1)
