from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
import time

def create_vm(subscription_id,
              resource_group_name,
              LOCATION,
              VNET_NAME,
              SUBNET_NAME,
              IP_NAME,
              IP_CONFIG_NAME,
              NIC_NAME,
              address_space,
              sub_address_prefix,
              ip_sku,
              public_ip_allocation_method,
              public_ip_address_version,
              VM_NAME,
              VM_USERNAME,
              VM_PASSWORD,
              vm_publisher,
              vm_offer,
              vm_sku,
              vm_version,
              vm_size):
    


    # Acquire a credential object using CLI-based authentication.
    credential = DefaultAzureCredential()

    # Retrieve subscription ID from environment variable.
    #subscription_id = subscription_id


    # Step 1: Provision a resource group

    # Obtain the management object for resources, using the credentials
    # from the CLI login.
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Constants we need in multiple places: the resource group name and
    # the region in which we provision resources. You can change these
    # values however you want.
    

    # Provision the resource group.
    rg_result = resource_client.resource_groups.create_or_update(
        resource_group_name, {"location": LOCATION}
    )

    print(
        f"Provisioned resource group {rg_result.name} in the \
    {rg_result.location} region"
    )

    # For details on the previous code, see Example: Provision a resource
    # group at https://learn.microsoft.com/azure/developer/python/
    # azure-sdk-example-resource-group

    # Step 2: provision a virtual network
    # A virtual machine requires a network interface client (NIC). A NIC
    # requires a virtual network and subnet along with an IP address.
    # Therefore we must provision these downstream components first, then
    # provision the NIC, after which we can provision the VM.

    # Network and IP address names
    

    # Obtain the management object for networks
    network_client = NetworkManagementClient(credential, subscription_id)
    time.sleep(15)
    # Provision the virtual network and wait for completion
    poller = network_client.virtual_networks.begin_create_or_update(
        resource_group_name,
        VNET_NAME,
        {
            "location": LOCATION,
            "address_space": {"address_prefixes": [address_space]},
        },
    )

    vnet_result = poller.result()

    print(
        f"Provisioned virtual network {vnet_result.name} with address \
    prefixes {vnet_result.address_space.address_prefixes}"
    )
    # Step 3: Provision the subnet and wait for completion
    time.sleep(15)
    poller = network_client.subnets.begin_create_or_update(
        resource_group_name,
        VNET_NAME,
        SUBNET_NAME,
        {"address_prefix": sub_address_prefix},
    )
    subnet_result = poller.result()

    print(
        f"Provisioned virtual subnet {subnet_result.name} with address \
    prefix {subnet_result.address_prefix}"
    )
    #time.sleep(20)
    # Step 4: Provision an IP address and wait for completion
    poller = network_client.public_ip_addresses.begin_create_or_update(
        resource_group_name,
        IP_NAME,
        {
            "location": LOCATION,
            "sku": {"name": ip_sku},
            "public_ip_allocation_method": public_ip_allocation_method,
            "public_ip_address_version": public_ip_address_version,
        },
    )

    ip_address_result = poller.result()

    print(
        f"Provisioned public IP address {ip_address_result.name} \
    with address {ip_address_result.ip_address}"
    )
    #time.sleep(15)
    # Step 5: Provision the network interface client
    poller = network_client.network_interfaces.begin_create_or_update(
        resource_group_name,
        NIC_NAME,
        {
            "location": LOCATION,
            "ip_configurations": [
                {
                    "name": IP_CONFIG_NAME,
                    "subnet": {"id": subnet_result.id},
                    "public_ip_address": {"id": ip_address_result.id},
                }
            ],
        },
    )

    nic_result = poller.result()

    print(f"Provisioned network interface client {nic_result.name}")

    # Step 6: Provision the virtual machine

    # Obtain the management object for virtual machines
    compute_client = ComputeManagementClient(credential, subscription_id)

   

    print(
        f"Provisioning virtual machine {VM_NAME}; this operation might \
    take a few minutes."
    )

    # Provision the VM specifying only minimal arguments, which defaults
    # to an Ubuntu 18.04 VM on a Standard DS1 v2 plan with a public IP address
    # and a default virtual network/subnet.

    poller = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name,
        VM_NAME,
        {
            "location": LOCATION,
            "storage_profile": {
                "image_reference": {
                    "publisher": vm_publisher,
                    "offer": vm_offer,
                    "sku": vm_sku,
                    "version": vm_version,
                }
            },
            "hardware_profile": {"vm_size": vm_size},
            "os_profile": {
                "computer_name": VM_NAME,
                "admin_username": VM_USERNAME,
                "admin_password": VM_PASSWORD,
            },
            "network_profile": {
                "network_interfaces": [
                    {
                        "id": nic_result.id,
                    }
                ]
            },
        },
    )

    vm_result = poller.result()
    print(f"Provisioned virtual machine {vm_result.name}")


# deletion of Virtual Machine
def delete_vm(subscription_id,resource_group_name,vm_name):





# Instantiate Azure SDK clients with DefaultAzureCredential
    credential = DefaultAzureCredential()

    compute_client = ComputeManagementClient(
    credential=credential,
    subscription_id=subscription_id
    )

    network_client = NetworkManagementClient(
    credential=credential,
    subscription_id=subscription_id
    )

    resource_client = ResourceManagementClient(
    credential=credential,
    subscription_id=subscription_id
     )

    storage_client = StorageManagementClient(
    credential=credential,
    subscription_id=subscription_id
     )

# Get the virtual machine resource ID
    vm = compute_client.virtual_machines.get(resource_group_name, vm_name)
    vm_id = vm.id

# Delete the virtual machine
    print("Deleting virtual machine {}...".format(vm_name))
    async_vm_delete = compute_client.virtual_machines.begin_delete(resource_group_name, vm_name)
    async_vm_delete.wait() 

# Delete the virtual machine's associated resources
    print("Deleting associated resources for virtual machine {}...".format(vm_name))

# Delete the network interface
    for nic_reference in vm.network_profile.network_interfaces:
        nic_id = nic_reference.id
        nic_name = nic_id.split("/")[-1]
        print("Deleting network interface {}...".format(nic_name))
        async_nic_delete = network_client.network_interfaces.begin_delete(resource_group_name, nic_name)
        async_nic_delete.wait()
    

# Delete the disks
    for disk_reference in vm.storage_profile.data_disks:
        disk_id = disk_reference.managed_disk.id
        disk_name = disk_id.split("/")[-1]
        print("Deleting disk {}...".format(disk_name))
        async_disk_delete = compute_client.disks.begin_delete(resource_group_name, disk_name)
        async_disk_delete.wait()
    os_disk_name = vm.storage_profile.os_disk.name
    print("Deleting OS disk {}...".format(os_disk_name))
    async_os_disk_delete = compute_client.disks.begin_delete(resource_group_name, os_disk_name)
    async_os_disk_delete.wait()
# Delete the boot diagnostics storage account if it exists
    if vm.diagnostics_profile.boot_diagnostics is not None:
        storage_uri = vm.diagnostics_profile.boot_diagnostics.storage_uri
        storage_account_name = storage_uri.split("/")[-1].split(".")[0]
        print("Deleting boot diagnostics storage account {}...".format(storage_account_name))
        async_storage_account_delete = storage_client.storage_accounts.begin_delete(resource_group_name, storage_account_name)
        async_storage_account_delete.wait()

# Delete the virtual machine's availability set if it exists
    if vm.availability_set is not None:
        availability_set_id = vm.availability_set.id
        availability_set_name = availability_set_id.split("/")[-1]
        print("Deleting availability set {}...".format(availability_set_name))
        async_availability_set_delete = compute_client.availability_sets.begin_delete(resource_group_name, availability_set_name)
        async_availability_set_delete.wait()

# Delete the virtual machine's managed identity if it exists
    if vm.identity is not None:
       identity_id = vm.identity.principal_id
       identity_name = identity_id.split("/")[-1]
       print("Deleting managed identity {}...".format(identity_name))
       async_identity_delete = resource_client.deployments.begin_delete(resource_group_name, identity_name)
       async_identity_delete.wait()

    print("Done.")

    