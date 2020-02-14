#!/bin/bash
echo "Generating configurations for all CSR devices from Jinja2 templates"
j2 -f yaml interfaces.j2 challenge.yml > csr1_intf.cfg
sed -i.bak 's/csr1/csr2/g' interfaces.j2
j2 -f yaml interfaces.j2 challenge.yml > csr2_intf.cfg
sed -i.bak 's/csr2/csr3/g' interfaces.j2
j2 -f yaml interfaces.j2 challenge.yml > csr3_intf.cfg
sed -i.bak 's/csr3/csr1/g' interfaces.j2

j2 -f yaml bgp.j2 challenge.yml > csr1_bgp.cfg
sed -i.bak 's/csr1/csr2/g' interfaces.j2
j2 -f yaml bgp.j2 challenge.yml > csr2_bgp.cfg
sed -i.bak 's/csr2/csr3/g' interfaces.j2
j2 -f yaml bgp.j2 challenge.yml > csr3_bgp.cfg
sed -i.bak 's/csr3/csr1/g' interfaces.j2
echo "Done, please verify configurations were generated properly"