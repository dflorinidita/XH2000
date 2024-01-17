#!/usr/bin/python3
import re
import sys
import subprocess

def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def get_rack_power_consumption(rack_number):
    command = f"/opt/PMSM/bin/pmsmRack.py monitor -r {rack_number} --power --module --consumption"

    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        print(f"Error for command: {e}")
        return
    clean_stderr = clean_ansi_codes(result.stderr)
    if result.returncode != 0:
        if "rack" in clean_stderr and "not defined" in clean_stderr:
            print(f"Error: {clean_stderr.strip()}")
        else:
            print(f"Error: {result.stderr}")
        return

    watt_values = re.findall(r': (\d+) Watts', result.stdout)
    watt_values = [int(value) for value in watt_values]

    print(f"Rack {rack_number}: {watt_values}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: power_module.py <rack>")
        sys.exit(1)

    rack_number = sys.argv[1]
    get_rack_power_consumption(rack_number)
