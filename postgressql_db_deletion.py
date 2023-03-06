from databases.postgresql_database import delete_postgresql_database
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

resource_group_name=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'resource_group_name')
server_name=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'postgresql_server_name')
database_name=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'postgresql_database_name')
subscription_id=get_parameter("C:\\Users\\Public\\azure_sdk_temp\\azure_sdk\\parameter.dev",'subscription_id')

delete_postgresql_database(subscription_id,resource_group_name,server_name,database_name)