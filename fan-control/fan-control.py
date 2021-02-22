#!/usr/bin/env python3
import json
import subprocess
import RPi.GPIO as GPIO
from time import sleep

CONFIG_FILE = "/opt/fan-control/fan-control.config.json"
CONFIG = {}


def fan_control_test():
    set_fan(False)
    sleep(4)
    set_fan(True)
    sleep(4)
    set_fan(False)
    sleep(4)


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(CONFIG["BASE_PIN"], GPIO.OUT)

    # Quick init test
    #init_test()


def set_fan(state):
    GPIO.output(CONFIG["BASE_PIN"], state)


def get_temp():
    args = ("/opt/vc/bin/vcgencmd", "measure_temp")
    cmd_out = subprocess.check_output(args)
    # Expected response format: "temp=41.3'C\n"
    str_tmp = cmd_out.partition("=")[2].partition("'")[0]
    return float(str_tmp)


def loop():
    temp = get_temp()
    #print("Temp=%.1f'C" % temp)
    if temp > CONFIG["FAN_ON_TEMP"]:
        set_fan(True)
    elif temp < CONFIG["FAN_OFF_TEMP"]:
        set_fan(False)


def load_config():
    user_config = {}
    with open(CONFIG_FILE) as config_file:
        user_config = json.load(config_file)
    CONFIG["STARTUP_TEST"] = user_config.get("startup_test", False)
    CONFIG["BASE_PIN"] = user_config.get("base_pin", 3)
    CONFIG["POLL_RATE_S"] = user_config.get("poll_rate_s", 5)
    CONFIG["FAN_ON_TEMP"] = user_config.get("high_temp_c", 55)
    CONFIG["FAN_OFF_TEMP"] = CONFIG["FAN_ON_TEMP"] - user_config.get("deadzone_c", 10)


def main():
    """Entry point"""
    try:
        # Load Config
        load_config()

        # Initialise pins
        init()

        if CONFIG["STARTUP_TEST"]:
            print("Running fan control test (4s off, 4s on, 4s off)")
            fan_control_test()
        print("Starting fan control")

        while(True):
            loop()
            sleep(CONFIG["POLL_RATE_S"])
    finally:
        GPIO.cleanup()
        print("Ending fan control")


if __name__ == '__main__':
    main()
