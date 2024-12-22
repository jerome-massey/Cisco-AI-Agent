
def discover_devices(testbed_path: str):
    """
    Discover devices from a testbed file.

    :param testbed_path: Path to the PyATS testbed YAML file.
    :return: List of devices discovered.
    """
    from pyats.topology import loader

    testbed = loader.load(testbed_path)
    devices = [device.name for device in testbed.devices.values()]
    return devices

# 3. Data Collection
# Use PyATS libraries to collect data from devices.
# Example: Collect interface information from a device.
def collect_data(device_name: str, commands: list, testbed_path: str):
    """
    Connect to a device and execute multiple commands to collect data.

    :param device_name: The name of the device to connect to.
    :param commands: A list of commands to execute.
    :param testbed_path: Path to the PyATS testbed YAML file.
    :return: Dictionary with command outputs.
    """
    from pyats.topology import loader
    from genie.libs.conf.base import Device

    testbed = loader.load(testbed_path)
    device = testbed.devices[device_name]

    device.connect()
    output = {}
    for command in commands:
        output[command] = device.execute(command)
    device.disconnect()
    return output