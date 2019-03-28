"""Virtual machine handler module"""

from enum import Enum, auto
import os
from typing import List, Dict, Any
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
import psycopg2

class VirtualMachineSize(Enum):
    """Virtual machine size enum"""

    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()

# pylint: disable=too-few-public-methods
class VirtualMachine:
    """Virtual machine object"""

    def __init__(self, vm_id: int, name: str, size: VirtualMachineSize):
        """Initialize the vm object"""

        self.vm_id = vm_id
        self.name = name
        self.size = size

    def events(self) -> List[Dict[str, Any]]:
        """List all events for this virtual machine"""

        pass

def create_virtual_machine(name: str, size: VirtualMachineSize) -> VirtualMachine:
    """
    Create a virtual machine.

    Args:
        name (str): Requested name of the new VM.
        size (VirtualMachineSize): Requested size of the new VM.

    Returns:
        VirtualMachine: Instance of the created VM.
    """

    application_id = os.environ['AZURE_CLIENT_ID']
    client_secret = os.environ['AZURE_CLIENT_SECRET']
    tenant_id = os.environ['AZURE_TENANT_ID']
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']

    creds = ServicePrincipalCredentials(
        client_id=application_id,
        secret=client_secret,
        tenant=tenant_id
    )

    compute_client = ComputeManagementClient(
        credentials=creds,
        subscription_id=subscription_id
    )
    network_client = NetworkManagementClient(
        credentials=creds,
        subscription_id=subscription_id
    )
    resource_client = ResourceManagementClient(
        credentials=creds,
        subscription_id=subscription_id
    )

    resource_client.resource_groups.create_or_update(
        resource_group_name=f'{name}-rg',
        parameters=dict(
            location='eastus'
        )
    )

    network_client.virtual_networks.create_or_update(
        resource_group_name=f'{name}-rg',
        virtual_network_name=f'{name}vnet',
        parameters=dict(
            location='eastus',
            address_space=dict(
                address_prefixes=['10.0.0.0/16']
            )
        )
    ).wait()

    subnet = network_client.subnets.create_or_update(
        resource_group_name=f'{name}-rg',
        virtual_network_name=f'{name}vnet',
        subnet_name=f'{name}subnet',
        subnet_parameters=dict(
            address_prefix='10.0.0.0/24'
        )
    ).result()

    pip = network_client.public_ip_addresses.create_or_update(
        resource_group_name=f'{name}-rg',
        public_ip_address_name=f'{name}pip',
        parameters=dict(
            location='eastus',
            public_ip_allocation_method='Dynamic',
            sku=dict(
                name='Basic'
            )
        )
    ).result()

    nic = network_client.network_interfaces.create_or_update(
        resource_group_name=f'{name}-rg',
        network_interface_name=f'{name}nic',
        parameters=dict(
            location='eastus',
            ip_configurations=[
                dict(
                    name=f'{name}ipconfig',
                    subnet=dict(
                        id=subnet.id
                    ),
                    public_ip_address=dict(
                        id=pip.id
                    )
                )
            ]
        )
    ).result()

    vm_params = dict(
        location='eastus',
        os_profile=dict(
            computer_name=name,
            admin_username=f'{name}admin',
            admin_password=f'{name}{os.environ["PASSWORD_SEED"]}'
        ),
        hardware_profile=dict(
            vm_size='Standard_DS1_v2'
        ),
        storage_profile=dict(
            image_reference=dict(
                publisher='Canonical',
                offer='UbuntuServer',
                sku='16.04.0-LTS',
                version='latest'
            )
        ),
        network_profile=dict(
            network_interfaces=[
                dict(
                    id=nic.id
                )
            ]
        )
    )

    compute_client.virtual_machines.create_or_update(
        resource_group_name=f'{name}-rg',
        vm_name=name,
        parameters=vm_params
    )

    _insert_virtual_machine(name=name, size=size)

def list_virtual_machines() -> List[VirtualMachine]:
    """
    List all VMs.

    Args:
        None

    Returns:
        List[VirtualMachine]: Environment virtual machines.
    """

    db_name = os.environ['POSTGRES_DB_NAME']
    username = os.environ['POSTGRES_USER_NAME']
    hostname = os.environ['POSTGRES_HOST_NAME']
    password = os.environ['POSTGRES_PASSWORD']
    port = os.environ['POSTGRES_PORT']

    # pylint: disable=line-too-long
    db_connection = psycopg2.connect(f"dbname='{db_name}' user='{username}' host='{hostname}' password='{password}' port='{port}'")
    cursor = db_connection.cursor()

    query = '''
        SELECT
            vm_id,
            name,
            size
        FROM public.virtual_machine;
    '''

    cursor.execute(query)
    output = cursor.fetchall()
    db_connection.commit()

    cursor.close()
    db_connection.close()

    return [
        VirtualMachine(
            vm_id=row[0],
            name=row[1],
            size=VirtualMachineSize[row[2]]
        )
        for row
        in output
    ]

def get_virtual_machine(name: str) -> VirtualMachine:
    """
    Get a virtual machine instance.

    Args:
        vm_id (int): Virtual machine ID.

    Returns:
        VirtualMachine: Requested virtual machine.
    """

    db_name = os.environ['POSTGRES_DB_NAME']
    username = os.environ['POSTGRES_USER_NAME']
    hostname = os.environ['POSTGRES_HOST_NAME']
    password = os.environ['POSTGRES_PASSWORD']
    port = os.environ['POSTGRES_PORT']

    # pylint: disable=line-too-long
    db_connection = psycopg2.connect(f"dbname='{db_name}' user='{username}' host='{hostname}' password='{password}' port='{port}'")
    cursor = db_connection.cursor()

    query = '''
        SELECT
            vm_id,
            name,
            size
        FROM public.virtual_machine
        WHERE name = %s;
    '''
    params = (name,)

    cursor.execute(query, params)
    output = cursor.fetchone()
    print(output)
    db_connection.commit()

    cursor.close()
    db_connection.close()

    return VirtualMachine(
        vm_id=output[0],
        name=output[1],
        size=VirtualMachineSize[output[2]]
    ) if output else None

def _insert_virtual_machine(name: str, size: VirtualMachineSize) -> None:
    """
    Insert the virtual machine into the database after it is created.

    Args:
        name (str): Name of the new VM.
        size (VirtualMachineSize): Size of the new VM.

    Returns:
        None
    """

    db_name = os.environ['POSTGRES_DB_NAME']
    username = os.environ['POSTGRES_USER_NAME']
    hostname = os.environ['POSTGRES_HOST_NAME']
    password = os.environ['POSTGRES_PASSWORD']
    port = os.environ['POSTGRES_PORT']

    # pylint: disable=line-too-long
    db_connection = psycopg2.connect(f"dbname='{db_name}' user='{username}' host='{hostname}' password='{password}' port='{port}'")
    cursor = db_connection.cursor()

    query = '''
        INSERT INTO public.virtual_machine
        (
            name,
            size
        )
        VALUES
        (
            %s,
            %s
        )
    '''
    params = (name, size.name)

    cursor.execute(query, params)
    db_connection.commit()

    cursor.close()
    db_connection.close()
