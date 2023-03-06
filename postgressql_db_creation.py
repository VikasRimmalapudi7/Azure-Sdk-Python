from databases.postgresql_database import create_postgresql_database
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
subscription_id=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'subscription_id')
resource_group_name=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'resource_group_name')
location=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'location')
server_name=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'postgresql_server_name')
administrator_login=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'postgresql_administrator_login')
administrator_login_password=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'postgresql_administrator_login_password')
database_name=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'postgresql_database_name')
sku_name=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'postgresql_sku_name')


create_postgresql_database(subscription_id,resource_group_name,location,server_name,administrator_login,administrator_login_password,database_name)


