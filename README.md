# csr1000v-validation
This repository contains two folders **ansible** and **napalm**. Each one does the same thing but using different frameworks for network automation. What is that thing? Deploying & validating Jinja2 based interface and bgp configuration to three different Cisco CSR1000v routers.

### Using Napalm
The project in the napalm directory is intended to be run from a python3 virtualenv. It requires napalm and j2cli.

#### Manually generating configurations
1. Generate interface configurations for each CSR device by editing interfaces.j2 and changing the node to be either csr1, csr2, or csr3. 
2. Then run `j2 -f yaml interfaces.j2 challenge.yml > csr1_intf.cfg` and change csr1 to csr2, or csr3 as needed depending upon what you have set in interfaces.j2
3. Do the same thing for bgp.j2

#### Generating configurations using gen_configs.sh
I've included a script called gen_configs.sh that when run will do all of the above manual work for you. `chmod +x gen_configs.sh && ./gen_configs.sh`

##### Running config.py
Once the configurations have been generated you can edit config.py to change the device (ie. csr1, csr2, or csr3) and run it using `python3 config.py`. You should expect to run it 6 times. 3 times for each L2 configuration deployment and another 3 for each BGP deployment.

### Using Ansible
Run: `ansible-playbook -i hosts config.yml`
