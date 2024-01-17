#!/bin/python3.6
import subprocess
import sys
import re

def run_seq2_psu_read_command(hmc):
    # Run the seq2_psu_read_v3.sh script with the specified HMC
    command = f"./seq2_psu_read_v3.sh {hmc} 1 1"
    result = subprocess.check_output(command, shell=True)
    return result.decode()

def parse_psu_data(output):
    # Extracting PSU consumption data for each CPSM
    cpsm_data = re.findall(r'CPSM\d+:((?:\s+\d+;)+)', output)
    psu_values = [[int(value) for value in cpsm.split(';') if value.strip()] for cpsm in cpsm_data]
    return psu_values

def calculate_deviations(psu_values):
    for i, cpsm in enumerate(psu_values):
        if not cpsm:
            continue
        average_consumption = sum(cpsm) / len(cpsm)
        print(f"CPSM{i}: ", end='')
        for j, consumption in enumerate(cpsm):
            deviation = ((consumption - average_consumption) / average_consumption) * 100
            print(f"{consumption} ({deviation:.2f}%), ", end='')
        print(f"Subtotal: {sum(cpsm)}")

def analyze_psu_consumption(hmc):
    try:
        # Execute the command and get the output
        output = run_seq2_psu_read_command(hmc)
        psu_values = parse_psu_data(output)
        calculate_deviations(psu_values)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python PSU_deviation.py <hmc>")
    else:
        hmc = sys.argv[1]
        analyze_psu_consumption(hmc)
