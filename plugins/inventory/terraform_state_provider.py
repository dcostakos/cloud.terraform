# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

DOCUMENTATION = r'''
name: terraform_state_provider
author:
  - Dave Costakos
short_description: Builds an inventory from a terraform workspace
description:
  - Builds an inventory from a terraform cli workspace
  - supports execution-environments by support git-based workspaces
  - supports configuration of remote state access external to teh repository
  - no caching support
  - Supports only CLI-driven workflos
  - For use in execution environments, use a git paht
version_added: 1.3
options:
  plugin:
    description:
      - The name of the inventory plugin
      - Always C(cloud.terraform.terraform_state_provider)
    required: true
    type: str
    choices: [ cloud.terraform.terraform_state_provider ]
  project_path:
    description:
      - a list of dictionaries describing the terraform workspace
      - a key of 'path' or 'git' must be provided
      - if 'remote_state' is configured, a supported 'type' such as 's3' must exist
      - other parameters of the list are expected to be keys for the remote state
    required: true
    type: raw
  type_list:
    description:
      - the list of Terraform Types to pull into inventory
      - this list should be known in advance so you only pull it objects you care about
      - default is an empty list with imports everything
    required: false
    default: []
    type: raw
  access_param:
    descriptioin:
      - An ordered list of parameters to get from the terraform state to use as 'ansible_host'
      - will search in order provided and assign the first one found
    required: false
    type: raw
    default: ["public_ip"]
  address_list:
    description:
      - alternate way to filter terraform state objects to only import certain items
      - this is a regex match that will be used to further filter
      - type list takes precedence, then address list will be provided
    required: false
    type: raw
    default: []
'''

EXAMPLES = r'''
# Example using an existing local terraform directory
---
plugin: cloud.terraform.terraform_state_provider
project_path:
  - path: "."
type_list:
  - aws_instance
access_param:
  - public_ip
  - private_ip

# example using a remote git repo
---
plugin: cloud.terraform.terraform_state_provider
project_path:
  - git: https://github.com/git_user/git_repo.git
    remote_state:
      type: s3
      bucket: remote_state_s3_bucket
      key: remote_state_key_name
type_list:
  - aws_instance
access_param:
  - public_ip
  - private_ip

  # ansible-inventory example
   $ ansible-inventory -i inv_tf.yml --graph --vars
@all:
  |--@ungrouped:
  |--@tag_AlwaysUp_false:
  |  |--aws_instance.dbserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 18.191.226.2}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-08b59b54dbba650d6}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-08b59b54dbba650d6}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-015955607d9f3b25b}
  |  |  |--{private_dns = ip-10-10-10-143.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.143}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 18.191.226.2}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-05d6685afecb73fb2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = dbserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = dbserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |  |--aws_instance.webserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 3.144.148.143}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-0cd95df9eb91b83db}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-0cd95df9eb91b83db}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-0b1a3a64ff9b1b4a0}
  |  |  |--{private_dns = ip-10-10-10-181.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.181}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 3.144.148.143}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-04b7c6a8cdfd983a2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = webserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = webserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |--@tag_Contact_dcostako_redhat_com:
  |  |--aws_instance.dbserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 18.191.226.2}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-08b59b54dbba650d6}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-08b59b54dbba650d6}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-015955607d9f3b25b}
  |  |  |--{private_dns = ip-10-10-10-143.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.143}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 18.191.226.2}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-05d6685afecb73fb2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = dbserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = dbserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |  |--aws_instance.webserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 3.144.148.143}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-0cd95df9eb91b83db}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-0cd95df9eb91b83db}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-0b1a3a64ff9b1b4a0}
  |  |  |--{private_dns = ip-10-10-10-181.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.181}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 3.144.148.143}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-04b7c6a8cdfd983a2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = webserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = webserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |--@tag_CreatedBy_TerraformViaAnsible:
  |  |--aws_instance.dbserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 18.191.226.2}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-08b59b54dbba650d6}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-08b59b54dbba650d6}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-015955607d9f3b25b}
  |  |  |--{private_dns = ip-10-10-10-143.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.143}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 18.191.226.2}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-05d6685afecb73fb2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = dbserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = dbserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |  |--aws_instance.webserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 3.144.148.143}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-0cd95df9eb91b83db}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-0cd95df9eb91b83db}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-0b1a3a64ff9b1b4a0}
  |  |  |--{private_dns = ip-10-10-10-181.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.181}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 3.144.148.143}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-04b7c6a8cdfd983a2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = webserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = webserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |--@tag_DeleteBy_tomorrow:
  |  |--aws_instance.dbserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 18.191.226.2}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-08b59b54dbba650d6}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-08b59b54dbba650d6}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-015955607d9f3b25b}
  |  |  |--{private_dns = ip-10-10-10-143.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.143}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 18.191.226.2}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-05d6685afecb73fb2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = dbserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = dbserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |  |--aws_instance.webserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 3.144.148.143}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-0cd95df9eb91b83db}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-0cd95df9eb91b83db}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-0b1a3a64ff9b1b4a0}
  |  |  |--{private_dns = ip-10-10-10-181.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.181}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 3.144.148.143}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-04b7c6a8cdfd983a2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = webserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = webserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |--@tag_Name_dbserver_tf:
  |  |--aws_instance.dbserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 18.191.226.2}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-08b59b54dbba650d6}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-08b59b54dbba650d6}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-015955607d9f3b25b}
  |  |  |--{private_dns = ip-10-10-10-143.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.143}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 18.191.226.2}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-05d6685afecb73fb2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = dbserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = dbserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}
  |--@tag_Name_webserver_tf:
  |  |--aws_instance.webserver
  |  |  |--{ami = ami-0d91dda6e8a311f0c}
  |  |  |--{ansible_host = 3.144.148.143}
  |  |  |--{arn = arn:aws:ec2:us-east-2:992730955111:instance/i-0cd95df9eb91b83db}
  |  |  |--{associate_public_ip_address = True}
  |  |  |--{availability_zone = us-east-2c}
  |  |  |--{capacity_reservation_specification_0_capacity_reservation_preference = open}
  |  |  |--{cpu_core_count = 1}
  |  |  |--{cpu_options_0_amd_sev_snp = }
  |  |  |--{cpu_options_0_core_count = 1}
  |  |  |--{cpu_options_0_threads_per_core = 1}
  |  |  |--{cpu_threads_per_core = 1}
  |  |  |--{credit_specification_0_cpu_credits = standard}
  |  |  |--{disable_api_stop = False}
  |  |  |--{disable_api_termination = False}
  |  |  |--{ebs_optimized = False}
  |  |  |--{enclave_options_0_enabled = False}
  |  |  |--{get_password_data = False}
  |  |  |--{hibernation = False}
  |  |  |--{host_id = }
  |  |  |--{iam_instance_profile = }
  |  |  |--{id = i-0cd95df9eb91b83db}
  |  |  |--{instance_initiated_shutdown_behavior = stop}
  |  |  |--{instance_lifecycle = }
  |  |  |--{instance_state = running}
  |  |  |--{instance_type = t2.micro}
  |  |  |--{ipv6_address_count = 0}
  |  |  |--{key_name = ssh_key_name}
  |  |  |--{maintenance_options_0_auto_recovery = default}
  |  |  |--{metadata_options_0_http_endpoint = enabled}
  |  |  |--{metadata_options_0_http_protocol_ipv6 = disabled}
  |  |  |--{metadata_options_0_http_put_response_hop_limit = 1}
  |  |  |--{metadata_options_0_http_tokens = optional}
  |  |  |--{metadata_options_0_instance_metadata_tags = disabled}
  |  |  |--{monitoring = False}
  |  |  |--{outpost_arn = }
  |  |  |--{password_data = }
  |  |  |--{placement_group = }
  |  |  |--{placement_partition_number = 0}
  |  |  |--{primary_network_interface_id = eni-0b1a3a64ff9b1b4a0}
  |  |  |--{private_dns = ip-10-10-10-181.us-east-2.compute.internal}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_a_record = False}
  |  |  |--{private_dns_name_options_0_enable_resource_name_dns_aaaa_record = False}
  |  |  |--{private_dns_name_options_0_hostname_type = ip-name}
  |  |  |--{private_ip = 10.10.10.181}
  |  |  |--{public_dns = }
  |  |  |--{public_ip = 3.144.148.143}
  |  |  |--{root_block_device_0_delete_on_termination = True}
  |  |  |--{root_block_device_0_device_name = /dev/sda1}
  |  |  |--{root_block_device_0_encrypted = False}
  |  |  |--{root_block_device_0_iops = 3000}
  |  |  |--{root_block_device_0_kms_key_id = }
  |  |  |--{root_block_device_0_throughput = 125}
  |  |  |--{root_block_device_0_volume_id = vol-04b7c6a8cdfd983a2}
  |  |  |--{root_block_device_0_volume_size = 10}
  |  |  |--{root_block_device_0_volume_type = gp3}
  |  |  |--{source_dest_check = True}
  |  |  |--{spot_instance_request_id = }
  |  |  |--{subnet_id = subnet-0f4620cf83bf2ee17}
  |  |  |--{tags_Name = webserver-tf}
  |  |  |--{tags_all_AlwaysUp = false}
  |  |  |--{tags_all_Contact = email_contact}
  |  |  |--{tags_all_CreatedBy = TerraformViaAnsible}
  |  |  |--{tags_all_DeleteBy = tomorrow}
  |  |  |--{tags_all_Name = webserver-tf}
  |  |  |--{tenancy = default}
  |  |  |--{user_data_replace_on_change = False}
  |  |  |--{vpc_security_group_ids_0 = sg-02ba887eb06a6c80c}

# Example playbook that accesses hostvars
# note the use of remote_user may be required
# and may need to be known by the playbook caller
---
- name: Configure Terraform instances
  hosts: aws_instance.*
  become: true
  remote_user: ec2-user
  gather_facts: false
  tasks:
    - name: Display a list of hostvars we got from Terraform
      ansible.builtin.debug:
        msg: |
          ID:     {{ hostvars[inventory_hostname].id }}
          AMI:    {{ hostvars[inventory_hostname].ami }}
          ARN:    {{ hostvars[inventory_hostname].arn }}
          AZ:     {{ hostvars[inventory_hostname].availability_zone }}
          Subnet: {{ hostvars[inventory_hostname].subnet_id }}

# run with
$ ansible-playbook -i inv_tf.yml config_tf_instances.yml
PLAY [Configure Terraform instances] *****************************************************************

TASK [Display a list of hostvars we got from Terraform] **********************************************
ok: [aws_instance.dbserver] => {
    "msg": "ID:     i-08b59b54dbba650d6
            AMI:    ami-0d91dda6e8a311f0c
            ARN:    arn:aws:ec2:us-east-2:992730955111:instance/i-08b59b54dbba650d6
            AZ:     us-east-2c
            Subnet: subnet-0f4620cf83bf2ee17"
}
ok: [aws_instance.webserver] => {
    "msg": "ID:     i-0cd95df9eb91b83db
            AMI:    ami-0d91dda6e8a311f0c
            ARN:    arn:aws:ec2:us-east-2:992730955111:instance/i-0cd95df9eb91b83db
            AZ:     us-east-2c
            Subnet: subnet-0f4620cf83bf2ee17"
}

PLAY RECAP *******************************************************************************************
aws_instance.dbserver      : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
aws_instance.webserver     : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0



'''


# python imports
import subprocess
import shutil
import tempfile
import re
import json

# Ansible imports
from ansible.module_utils.common import process
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

class TerraformInventoryError(Exception):
    pass

def _clean(var_str):
    return re.sub(r'\W|^(?=\d)','_', var_str)

# flatten json data to make it easier to set as variables
def flatten_json(y):
    out = {}

    def flatten(x, name=''):

        # If the Nested key-value
        # pair is of dict type
        if isinstance(x, dict):

            for a in x:
                flatten(x[a], name + a + '_')

        # If the Nested key-value
        # pair is of list type
        elif isinstance(x, list):

            i = 0

            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# resource filtering function logic
def filter_function(type_list, tag_list, address_list):
    def myfilter(x):
        if type_list is not None and len(type_list) > 0:
            if not x['type'] in type_list:
                return False

        if address_list is not None and len(address_list) > 0:
            found = False
            for taddress in address_list:
                if re.search(taddress, x['address']):
                    found = True
                    break

            if not found:
                return found

        if tag_list is not None and len(tag_list) > 0:
            found = False
            for tagset in tag_list:
                setkey = next(iter(tagset))
                setval = tagset[setkey]
                if setkey in x['values']['tags_all']:
                    if re.search(setval, x['values']['tags_all'][setkey]):
                        found = True
                        break

            if not found:
                return found

        return True

    return myfilter

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "cloud.terraform.terraform_state_provider"

    project_path = None
    terraform_binary = None
    type_list = []
    address_list = []
    tag_list = []
    ip_param = []
    remote_state = None

    attr_keys = [
        "arn", "ami",
    ]

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('tf.yaml', 'tf.yml')):
                return True
        return False


    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        cfg = self._read_config_data(path)
        self.project_path = cfg.get("project_path", None)
        self.terraform_binary = cfg.get("binary_path", None)
        self.type_list = cfg.get("type_list", [])
        self.address_list = cfg.get("address_list", [])
        self.ip_param = cfg.get("access_param", ["public_ip"])
        self.remote_state = cfg.get('remote_state', None)

        if isinstance(self.project_path, str):
            self.project_path = [self.project_path]

        if isinstance(self.type_list, str):
            self.type_list = [self.type_list]

        if isinstance(self.address_list, str):
            self.address_list = [self.address_list]

        # project_path must exist
        if self.project_path is None:
            raise TerraformInventoryError("project_path must exist")

        # validate and raise exception if terraform binary does not exist
        if self.terraform_binary is not None:
            if not shutil.which(self.terraform_binary):
                raise TerraformInventoryError(
                    f"Path for terraform_binary '{self.terraform_binary}' does not exist"
                )
        else:
            self.terraform_binary = process.get_bin_path("terraform", required=True)

        my_filter = filter_function(self.type_list, self.address_list, self.tag_list)

        for item in self.project_path:
            tempdir = None
            tdir = None
            try:
                if "git" in item:
                    tempdir = tempfile.mkdtemp()
                    tdir = tempdir
                    self._clone_gitrepo(tdir, item['git'])
                else:
                    tdir = item['path']

                init_cmd = self._build_tf_command(tdir, item)
                self.run_subprocess(init_cmd, tdir)
                show_cmd = self._build_tf_command(tdir, item, cmd_type="show")
                json_data = json.loads(self.run_subprocess(show_cmd, tdir)[1])
                if not "values" in json_data:
                    raise TerraformInventoryError(
                      f"Invalid result from show.  Project may be missing remote state: {json_data}"
                    )
                filtered_list = list(
                    filter(
                        my_filter,
                        json_data['values']['root_module']['resources']
                    )
                )
                self.inventory_from_show(inventory, filtered_list)
            finally:
                if tempdir is not None:
                    shutil.rmtree(tempdir, ignore_errors=True)

    def inventory_from_show(self, inventory, filtered_show_result):
        for resource in filtered_show_result:
            if "values" in resource:
                address = resource['address']

                for key in self.ip_param:
                    if not key in resource["values"]:
                        continue
                    inventory.add_host(address)
                    inventory.set_variable(
                        address, "ansible_host", resource['values'][key]
                    )
                    flattened_values = flatten_json(resource['values'])
                    for key, val in flattened_values.items():
                        if val is not None:
                            inventory.set_variable(address, key, val)

                    if "tags_all" in resource["values"]:
                        for tag_key, tag_val in resource['values']['tags_all'].items():
                            inventory.add_group(_clean(f"tag_{tag_key}_{tag_val}"))
                            inventory.add_child(_clean(f"tag_{tag_key}_{tag_val}"), address)
                    break

    def raise_for_status(self, cmd_result, cmd):
        if cmd_result[0] != 0:
            raise TerraformInventoryError(
                f"Command returned non-zero return code: {cmd_result[0]} " +
                f"from {cmd} - stderr:{cmd_result[1]} stdout:{cmd_result[2]}")

    def _clone_gitrepo(self, cwd, repo):
        return self.run_subprocess(["git", "clone", repo], cwd)

    def _build_backend(self, backend_dir, backend_type):
        backend_config = f'''
terraform {{
    backend "{backend_type}" {{}}
}}
'''
        with open(f"{backend_dir}/backend_{backend_type}.tf", "w", encoding="utf-8") as file:
            file.write(backend_config)

    def _build_tf_command(self, cwd, item, cmd_type="init"):
        cmd = [self.terraform_binary]
        if cmd_type == "init":
            cmd.append("init")
        elif cmd_type == "show":
            cmd.extend(["show", "-json"])
            return cmd
        else:
            raise TerraformInventoryError(
                f"Unexpected command type {cmd_type}, expected on 'init' or 'show'")
        if "remote_state" in item:
            self._build_backend(cwd, item['remote_state']['type'])
            for key,val in item['remote_state'].items():
                if key != "type":
                    cmd.extend(["-backend-config", f"{key}={val}"])

        return cmd

    def run_subprocess(self, cmd, cwd, check=False, raise_for_status=True):
        cmd_result = None
        cmd_result = subprocess.run(cmd, capture_output=True, check=check, cwd=cwd)
        if cmd_result.returncode != 0 and raise_for_status:
            raise TerraformInventoryError(
                f"Error running {cmd}: {cmd_result.returncode}\n" +
                f" -- {cmd_result.stderr.decode('utf-8')}\n"
                f" -- {cmd_result.stdout.decode('utf-8')}"
            )
        return (
            cmd_result.returncode,
            cmd_result.stdout.decode("utf-8"),
            cmd_result.stderr.decode("utf-8")
        )
