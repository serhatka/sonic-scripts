import paramiko
from datetime import datetime

# Define the SSH connection parameters
hostname = "192.168.44.202"
port = 22  # Default SSH port
username = "admin"
password = "admin"

# Create an SSH client
ssh_client = paramiko.SSHClient()

# Automatically add the server's host key (this is insecure, consider adding proper host key verification)
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the server
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
    timeout = 2  # 2 seconds
    start_time = datetime.now()

    # Generate the output file name with the server IP and current date
    server_ip = hostname.replace(".", "-")
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_file_name = f"ssh_output_{server_ip}_{current_date}.txt"

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
    print(f"SSHException: {str(e)}")

finally:
    # Close the SSH session and the connection
    ssh_session.close()
    ssh_client.close()
