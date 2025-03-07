#!/usr/bin/env python3
import os
import subprocess
import time
import syslog
import re

TARGET_CPU_TEMP = 80  # Target CPU temperature in degrees Celsius

MIN_FAN_SPEED = 10  # Minimum fan speed in percentage
MAX_FAN_SPEED = 30  # Maximum fan speed in percentage

current_fan_speed = 0


# Get the current CPU temperature
def get_cpu_temperature():
    sensors_output = subprocess.check_output("sensors").decode()
    package_line = [
        line for line in sensors_output.split("\n") if "Package id 0" in line
    ][0]
    if package_line:
        match = re.search(r"\+\d+\.\d+", package_line)
        if match:
            package_temperature = float(match.group())
            return package_temperature
        else:
            print("No temperature found")
    else:
        print("No CPU temperature lines found")


def set_fan_speed(speed):
    if speed > MAX_FAN_SPEED or speed < MIN_FAN_SPEED:
        return

    global current_fan_speed
    current_fan_speed = speed

    # Convert the speed percentage to a hex value
    hex_speed = format(speed * 255 // 100, "02x")

    # Set the fan speed
    os.system(f"ipmitool raw 0x30 0x70 0x66 0x01 0x00 0x{hex_speed}")

    log = f"Fan speed adjusted to {speed}% - {hex_speed}"
    print(log)
    syslog.syslog(syslog.LOG_INFO, log)


def main():
    # IPMI tool command to set the fan control mode to manual (Full)
    os.system("ipmitool raw 0x30 0x45 0x01 0x01")
    time.sleep(2)

    global current_fan_speed

    while True:
        cpu_temp = get_cpu_temperature()
        print(f"Current CPU temperature: {cpu_temp}°C")

        if cpu_temp > TARGET_CPU_TEMP:
            target_fan_speed = MAX_FAN_SPEED
        else:
            target_fan_speed = MIN_FAN_SPEED

        if target_fan_speed != current_fan_speed:
            set_fan_speed(target_fan_speed)

        time.sleep(3)


if __name__ == "__main__":
    main()
