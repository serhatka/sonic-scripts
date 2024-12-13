# sonic-scripts
various python scripts for SONIC NOS

config-backup.py

Creates ssh session towards Dell switches running Enterprise SONIC Operating system, gets running configurations and creates and saves an output file per each switch.

Script is tested successfully on Ubuntu version 20.04. 

General Requirements:
ip connectivity between the server and switches

Ubuntu server requirements:
apt update
apt upgrade
apt install python3-pip
pip install paramiko

How to use:
Edit the switches section in the script with IP addresses, usernames and passowrd against each switch.
make the script executable with chmod +x 
run the script with ./config-backup.py



