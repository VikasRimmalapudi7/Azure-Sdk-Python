from virtual_machine.vm import create_vm
# runner file
# function to get user values of parameters from parameter.dev file
def get_parameter(filename, required_parameter):
    with open(filename, 'r') as file:
        for line in file:
            words = line.split()
            try:
                index = words.index(required_parameter)
            except ValueError:
                # search word not found in this line, try the next line
                continue
            #  return the next word
            return words[index + 1]
    # search word not found in file
    return None

# Create Virtual Machine
subscription_id = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'subscription_id')
resource_group_name = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'resource_group_name')
location = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'location')
vnet_name = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vnet_name')
subnet_name = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'subnet_name')
ip_name = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'ip_name')
ip_config_name = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'ip_config_name')
nic_name = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'nic_name')
address_space = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'address_space')
sub_address_prefix = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'sub_address_prefix')
ip_sku = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'ip_sku')
public_ip_allocation_method = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'public_ip_allocation_method')
public_ip_address_version = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'public_ip_address_version')
vm_name = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_name')
vm_username = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_username')
vm_password = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_password')
vm_publisher = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_publisher')
vm_offer = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_offer')
vm_sku = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_sku' )
vm_version = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_version')
vm_size = get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'vm_size')

# Create VM
create_vm(subscription_id,
              resource_group_name,
              location,
              vnet_name,
              subnet_name,
              ip_name,
              ip_config_name,
              nic_name,
              address_space,
              sub_address_prefix,
              ip_sku,
              public_ip_allocation_method,
              public_ip_address_version,
              vm_name,
              vm_username,
              vm_password,
              vm_publisher,
              vm_offer,
              vm_sku,
              vm_version,
              vm_size)

