#!/usr/bin/env python3

import paramiko
from datetime import datetime

# Define a list of switches with their connection parameters
switches = [
    {
        "hostname": "10.0.0.11",
        "port": 22,
        "username": "admin",
        "password": "Admin_123!",
    },
	{
        "hostname": "10.0.0.12",
        "port": 22,
        "username": "admin",
        "password": "Admin_123!",
    },
    {
        "hostname": "10.0.0.21",
        "port": 22,
        "username": "admin",
        "password": "Admin_123!",
    },
	{
        "hostname": "10.0.0.22",
        "port": 22,
        "username": "admin",
        "password": "Admin_123!",
    },
    {
        "hostname": "10.0.0.23",
        "port": 22,
        "username": "admin",
        "password": "Admin_123!",
    },
	{
        "hostname": "10.0.0.24",
        "port": 22,
        "username": "admin",
        "password": "Admin_123!",
    },
    # Add more switches as needed
]

# Create a function to execute SSH commands for a switch
def execute_ssh_commands(hostname, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the switch
        ssh_client.connect(hostname, port, username, password)

        # Create an SSH session
        ssh_session = ssh_client.invoke_shell()

        # Send the "sonic-cli" command
        command = "sonic-cli\n"
        ssh_session.send(command)

        # Wait for a specific prompt or signal that indicates that the "sonic-cli" command is complete
        while not ssh_session.recv_ready():
            pass

        # Send the "show run" command
        command = "show running-configuration | no-more\n"
        ssh_session.send(command)

        # Set a timeout for waiting for command completion (adjust the timeout as needed)
        timeout = 5  # 5 seconds
        start_time = datetime.now()

        # Generate the output file name with the switch IP and current date
        switch_ip = hostname.replace(".", "-")
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_file_name = f"ssh_output_{switch_ip}_{current_date}.txt"

        with open(output_file_name, "a") as output_file:
            while True:
                if ssh_session.recv_ready():
                    output = ssh_session.recv(2048).decode("utf-8")
                    output_file.write(output)
                    output_file.flush()
                    start_time = datetime.now()  # Reset the timeout
                elif (datetime.now() - start_time).seconds > timeout:
                    break  # Break the loop if the timeout is reached

    except paramiko.SSHException as e:
        print(f"SSHException for {hostname}: {str(e)}")

    finally:
        # Close the SSH session and the connection
        ssh_session.close()
        ssh_client.close()

# Iterate through the list of switches and execute SSH commands for each one
for switch in switches:
    execute_ssh_commands(**switch)

