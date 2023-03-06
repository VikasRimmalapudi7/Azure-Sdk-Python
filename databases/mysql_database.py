from azure.identity import DefaultAzureCredential
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.rdbms.mysql.models import (
    ServerForCreate, 
     ServerPropertiesForDefaultCreate,
    StorageProfile)
import mysql.connector

def create_mysql_database(subscription_id,resource_group_name,location,server_name,admin_login,admin_password,database_name,sku_name):
# Azure subscription ID

    credential = DefaultAzureCredential()

# Infrastructure encryption configuration
    resource_client = ResourceManagementClient(credential, subscription_id)

    # Constants we need in multiple places: the resource group name and
    # the region in which we provision resources. You can change these
    # values however you want.
    

    # Provision the resource group.
    rg_result = resource_client.resource_groups.create_or_update(
        resource_group_name, {"location": location})

    print(
        f"Provisioned resource group {rg_result.name} in the \
    {rg_result.location} region")

# Create storage profile for the server
    print("creating storage profile for the server")
    storage_profile = StorageProfile(
    storage_mb=5120, 
    backup_retention_days=7, 
    geo_redundant_backup="Disabled",
    storage_autogrow="Disabled",
    storage_iops=None, 
    storage_mb_shared=None, 
    storage_encryption="Enabled"
     )

# Create server properties for default create 
    print("creating server properties")
    server_properties = ServerPropertiesForDefaultCreate(
    administrator_login=admin_login,
    administrator_login_password=admin_password,
    version="5.7",
    storage_profile=storage_profile)

# Create server for creation
    print("creating server")
    server = ServerForCreate(
    name=server_name, 
    location=location, 
    properties=server_properties)

# Create MySQL client
    print("creating mysql client")
    credential = DefaultAzureCredential()
    mysql_client = MySQLManagementClient(credential, subscription_id)

# Create MySQL server
    print("creating mysql server")
    result = mysql_client.servers.begin_create(
    resource_group_name=resource_group_name,
    server_name=server_name,
    parameters=server)
    result.result()
    print("created azure database for mysql server")
    hostname = server_name+".mysql.database.azure.com"
    username = admin_login+"@"+server_name

# Connect to the server
    cnx = mysql.connector.connect(
    host=hostname,
    user=username,
    password=password
)

# Create the database
    cursor = cnx.cursor()
    create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
    cursor.execute(create_db_query)
    cnx.commit()

    print(f"MySQL database '{database_name}' created successfully!")




def delete_mysql_database(subscription_id,resource_group_name,server_name,database_name):
 
# Authenticate with the Azure management API
    credential = DefaultAzureCredential()
    mysql_client = MySQLManagementClient(credential, subscription_id)

# Delete the database
    print("started deleting !!!!!!!!")
    mysql_client.databases.begin_delete(resource_group_name, server_name, database_name).result()
    print("successfully deleted")
