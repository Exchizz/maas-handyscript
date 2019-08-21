#!/usr/bin/env python3

import asyncio

from maas.client import connect
from maas.client.enum import NodeStatus, LinkMode
from maas.client.viscera.pods import Pods

from pprint import pprint

from time import sleep

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--action', dest='action', nargs='?',
                    help='What action to execute')

args = parser.parse_args()

action = args.action
print("action: ", args.action)


client = connect( "http://maas01:5240/MAAS/", apikey='WNVd3fggHxGnDZZs6a:fQsArAqV5tzAFSp9wu:wTZZGyXWP62hrzcq56Peq2bf3KgGUysQ')


if action == "commission":
	all_machines = client.machines.list()
	
	filter_pool = "EnergyHosts"
	
	# Filter based on pool name
	new_machines = [
	    machine for machine in all_machines if machine.pool.name == filter_pool and machine.status == NodeStatus.NEW 
	]
	
	
	for machine in new_machines:
		machine.power_type = "manual"
		machine.save()
	
	
	# Commision all of the hosts in the pool
	for machine in new_machines:
		print("[+] Commission hostname:", machine.hostname)
		machine.commission()
	
	while len(new_machines) > 0:
		for machine in new_machines:
			machine.refresh()
			if machine.status == NodeStatus.READY:
				print("[+] Machine {} is commissioned".format(machine.hostname))
				new_machines.remove(machine) 
			else:
				print("[-] Machine {} is in status: {}".format(machine.hostname, machine.status))
		sleep(1)
	
	print("All hosts in pool {} are commissioned".format(filter_pool))




elif action == "deploy":
	all_machines = client.machines.list()
	
	filter_pool = "EnergyHosts"
	
	# Filter based on pool name
	ready_machines = [
	    machine for machine in all_machines if machine.pool.name == filter_pool and machine.status == NodeStatus.READY
	]
	
	for machine in ready_machines:
		for iface in machine.interfaces:
			if iface.name == "enp55s9":
				print("[+] Set mode to dhcp on {}".format(machine.hostname))
				iface.links[0].delete()
				iface.links.create( LinkMode.DHCP )



	for machine in machines;
		machine.deploy(distro_series="bionic", kvm_install=True)


	while len(ready_machines) > 0:
		for machine in ready_machines:
			machine.refresh()
			if machine.status == NodeStatus.DEPLOYED:
				print("[+] Machine {} is deployed".format(machine.hostname))
				ready_machines.remove(machine) 
			else:
				print("[-] Machine {} is in status: {}".format(machine.hostname, machine.status))
		sleep(1)
	
	print("All hosts in pool {} are deployed".format(filter_pool))



#interfaces = []
#pods = client.pods.list()
#system_ids = []
#for pod in pods:
#	retval = pod.compose(cores=1, memory=2048, hostname = "vm11",  interfaces= interfaces)
#	system_ids.append(retval)
#	#print(retval)
#	#retval = pod.compose(cores=1, memory=2048, hostname = "vm12",  interfaces= interfaces)
#	#system_ids.append(retval)
#	#print(pod.name)
#	#print(retval)
#
#
#
## Get all machines that are in the NEW status.
#all_machines = client.machines.list()
#new_machines = [
#    machine
#    for machine in all_machines
#    if machine.status -= NodeStatus.NEW
#]
#
## Wait until all machines are ready.
#completed_machines = []
#while len(new_machines) > 0:
#    await asyncio.sleep(5)
#    for machine in list(new_machines):
#        await machine.refresh()
#        if machine.status in [
#                NodeStatus.COMMISSIONING, NodeStatus.TESTING]:
#            # Machine is still commissioning or testing.
#            continue
#        elif machine.status == NodeStatus.READY:
#            # Machine is complete.
#            completed_machines.append(machine)
#            new_machines.remove(machine)
#        else:
#            # Machine has failed commissioning.
#            failed_machines.append(machine)
#            new_machines.remove(machine)
#
#
#system_id
#
#
#
#
#
#
#
#for system_id in system_ids:
#	machine = client.machines.get(system_id=system_id["system_id"])
#










#for pc in all_machines:
#	pprint(pc.status)
#	
#	ready_machines = [
#		machine
#		for machine in all_machines
#		if machine.status == NodeStatus.READY
#	]

#	ready_machines[0].deploy(distro_series="bionic")
#	help(all_machines[0])
exit(1)

#    # Run commissioning with a custom commissioning script on all new machines.
#    for machine in new_machines:
#        machine.commission(
#            commissioning_scripts=['clear_hardware_raid'], wait=False)
#
#    # Wait until all machines are ready.
#    failed_machines = []
#    completed_machines = []
#    while len(new_machines) > 0:
#        await asyncio.sleep(5)
#        for machine in list(new_machines):
#            await machine.refresh()
#            if machine.status in [
#                    NodeStatus.COMMISSIONING, NodeStatus.TESTING]:
#                # Machine is still commissioning or testing.
#                continue
#            elif machine.status == NodeStatus.READY:
#                # Machine is complete.
#                completed_machines.append(machine)
#                new_machines.remove(machine)
#            else:
#                # Machine has failed commissioning.
#                failed_machines.append(machine)
#                new_machines.remove(machine)
#
#    # Print message if any machines failed to commission.
#    if len(failed_machines) > 0:
#        for machine in failed_machines:
#            print("%s: transitioned to unexpected status - %s" % (
#                machine.hostname, machine.status_name))
#    else:
#        print("Successfully commissioned %d machines." % len(
#            completed_machines))
#

#commission_all_machines()
