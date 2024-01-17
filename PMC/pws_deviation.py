#!/bin/python3.6
import subprocess
import sys
import re

def run_pmsmRack_command(rack_number):
    # Run the pmsmRack.py script with the specified rack number
    command = f"/opt/PMSM/bin/pmsmRack.py monitor -r {rack_number} --power --module --consumption"
    result = subprocess.check_output(command, shell=True)
    return result.decode()

def parse_total_consumption(output):
    # Extracting total power consumption
    match = re.search(r'RACK\d+ RACK POWER CONSUMPTION\s+:\s+(\d+)', output)
    return int(match.group(1)) if match else 0

def parse_powershelf_data(output):
    # Extracting power consumption data for each power shelf
    pws_data = re.findall(r'> pws\d+\s+:\s+(\d+)', output)
    return [int(value) for value in pws_data]

def analyze_power_consumption(rack_number):
    try:
        # Execute the command and get the output
        output = run_pmsmRack_command(rack_number)
        total_consumption = parse_total_consumption(output)
        power_values = parse_powershelf_data(output)

        # Calculate the average consumption
        num_pws = len(power_values)
        average_consumption = total_consumption / num_pws

        # Display the number of PWS, total and average consumption
        print(f"Total number of PWS in Rack {rack_number}: {num_pws}")
        print(f"Total rack power consumption: {total_consumption} Watts")
        print(f"Average consumption per PWS: {average_consumption:.2f} Watts")

        # Calculate and display the deviation for each PWS
        for i, consumption in enumerate(power_values, start=0):
            deviation = ((consumption - average_consumption) / average_consumption) * 100
            deviation_str = f"{abs(deviation):.2f}% {'above' if deviation > 0 else 'below'} average"

            # Print in red if deviation is greater than 20%
            if abs(deviation) > 20:
                print(f"\033[91mPWS {i:02d}: {consumption} Watts, {deviation_str}\033[0m")  # Red color
            else:
                print(f"PWS {i:02d}: {consumption} Watts, {deviation_str}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <rack_number>")
    else:
        rack_number = sys.argv[1]
        analyze_power_consumption(rack_number)
