#!/usr/bin/env python
import boto3
import json
import yaml
# Initialize the AWS EC2 client
ec2 = boto3.client('ec2', region_name='ap-south-1')

# Define filters to list running instances
filters = [
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
]

# Use the describe_instances method to retrieve EC2 instance information
instances = ec2.describe_instances(Filters=filters)

# Initialize an empty inventory dictionary
inventory = {
    '_meta': {
        'hostvars': {}
    },
    '@aws_ec2': {
        'hosts': [],
        'vars': {}
    }
}

# Loop through instances and populate the inventory
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        # Extract instance private IP address
        private_ip_address = instance['PrivateIpAddress']

        # Create a host entry with private IP address
        host_entry = {
            'ansible_host': private_ip_address
        }

        # Append host entry to the '@aws_ec2' group
        inventory['@aws_ec2']['hosts'].append(private_ip_address)
        
        # Create a subgroup for the instance's 'Name' tag
        instance_name = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), None)
        if instance_name:
            subgroup_name = instance_name.replace(' ', '_')
            if subgroup_name not in inventory:
                inventory[subgroup_name] = {'hosts': [], 'vars': {}}
            inventory[subgroup_name]['hosts'].append(private_ip_address)

        # Add host entry to hostvars
        inventory['_meta']['hostvars'][private_ip_address] = host_entry

# Print the inventory in JSON format
#print(yaml.dumps(inventory, indent=4))
print(yaml.dump(inventory, default_flow_style=False))
