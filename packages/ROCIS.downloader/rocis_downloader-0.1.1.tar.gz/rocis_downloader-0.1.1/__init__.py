__requires__ = ["pyserial", "humanize", "tqdm", "platformdirs"]

import datetime
import json
import os
import platform
import re
import subprocess
import sys
import time
import types

import serial.tools.list_ports
import humanize
import tqdm
import platformdirs


def get_device(name):
    return serial.Serial(
        port=name,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,  # 8 data bits
        parity=serial.PARITY_NONE,  # No parity
        stopbits=serial.STOPBITS_ONE,  # 1 stop bit
        timeout=1,
    )


def find_dylos_device():
    """
    Searches available COM ports for a Dylos device that responds to the 'Y' command.

    Returns:
        serial.Serial: The serial connection to the Dylos device if found, otherwise None.
    """

    for port in serial.tools.list_ports.comports():
        try:
            ser = get_device(port.device)
            time.sleep(2)  # Give the device some time to initialize
            ser.write(b"Y\r")  # Send 'Y' command followed by carriage return
            response = ser.readline().decode().strip()
            if response.startswith("DC1700"):
                print(f"Dylos device found on {port.device}: {response}")
                return ser
            ser.close()
        except serial.SerialException:
            pass  # Ignore ports that can't be opened or don't respond

    print("No Dylos device found.")
    return None


def read_all(ser):
    while val := ser.readline().decode().strip():
        yield val


def download_data(ser):
    """
    Downloads data from the Dylos device using the 'D' command.

    Args:
        ser (serial.Serial): The serial connection to the Dylos device.
    """

    ser.write(b"D\r")  # Send 'D' command followed by carriage return
    progress = tqdm.tqdm(read_all(ser), total=11520, unit="records")
    lines = list(progress)  # Read all available data

    if not lines:
        print("No data downloaded")
        sys.exit(2)

    data = "\n".join(lines) + "\n"
    print("Downloaded", humanize.naturalsize(len(data)))

    return lines


class Config(types.SimpleNamespace):
    data_path = platformdirs.user_data_path("downloader", "ROCIS")
    config_path = data_path / "config.json"

    @classmethod
    def load(cls):
        try:
            with cls.config_path.open() as strm:
                return cls(**json.load(strm))
        except FileNotFoundError:
            pass

    def save(self):
        self.data_path.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w") as strm:
            json.dump(vars(self), strm)

    @classmethod
    def prompt(cls):
        return cls(site=input("site ID: ").upper())

    def choose_dylos(self):
        devices = vars(self).setdefault("devices", {})
        while not (loc := input("Location (I, R, O, S)? ").upper()):
            continue
        if loc not in devices:
            while not valid_code(code := input(r"Dylos ID for {loc}? ").upper()):
                print("Invalid Dylos ID (must be like D000)")

            devices[loc] = code
        descriptions = vars(self).setdefault("descriptions", {})
        last = descriptions.get(loc, None)
        suggestion = f" [{last}]" if last else ""
        descriptions[loc] = input(f"Location description{suggestion}: ") or last
        return loc


def valid_code(code):
    return re.match(r"D\d\d\d", code)


def main(device=None):
    config = Config.load() or Config.prompt()
    loc = config.choose_dylos()
    config.save()

    dylos_device = get_device(device) if device else find_dylos_device()
    if not dylos_device:
        return

    lines = download_data(dylos_device)
    dylos_device.close()

    date = datetime.date.today().strftime(datetime.date.today().strftime("%m-%d-%y"))
    filename = (
        f"{config.site}_{loc}_{config.devices[loc]}_{date}_{config.descriptions[loc]}"
    )
    with Config.data_path.joinpath(filename).open("w") as strm:
        strm.write("\n".join(lines) + "\n")

    input("Press enter to open folders.")

    open_cmd = (
        os.startfile
        if platform.system() == "Windows"
        else lambda path: subprocess.run(["open", path])
    )
    open_cmd(Config.data_path)
