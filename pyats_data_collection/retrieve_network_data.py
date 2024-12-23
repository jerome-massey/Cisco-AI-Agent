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
        raw_output = device.execute(command)
        json_output = device.parse(command)
        output[command] = {
            'raw': raw_output,
            'json': json_output
        }
    device.disconnect()
    return output

def save_output_to_s3(output: dict, s3_bucket: str, s3_key_prefix: str):
    """
    Save the collected data to S3.

    :param output: Dictionary with device names as keys and command outputs as values.
    :param s3_bucket: The name of the S3 bucket to store the output.
    :param s3_key_prefix: The prefix for the S3 key.
    """
    import boto3
    import json
    from datetime import datetime

    s3_client = boto3.client('s3')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    for device_name, commands_output in output.items():
        # Save all raw outputs to a single file
        raw_outputs = "\n".join([f"Command: {command}\n{data['raw']}" for command, data in commands_output.items()])
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=f"{s3_key_prefix}/{device_name}_raw_{timestamp}.txt",
            Body=raw_outputs
        )

        # Save all JSON outputs to a single file
        json_outputs = {command: data['json'] for command, data in commands_output.items()}
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=f"{s3_key_prefix}/{device_name}_output_{timestamp}.json",
            Body=json.dumps(json_outputs)
        )