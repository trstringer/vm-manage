"""Virtual machine handler module"""

from enum import Enum, auto
from typing import List, Dict, Any

class VirtualMachineSize(Enum):
    """Virtual machine size enum"""

    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()

class VirtualMachine:
    """Virtual machine object"""

    def __init__(self, vm_id: int, name: str, size: VirtualMachineSize):
        """Initialize the vm object"""

        self.vm_id = vm_id
        self.name = name
        self.size = size

    def events(self) -> List[Dict[str, Any]]:
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

    pass

def list_virtual_machines() -> List[VirtualMachine]:
    """
    List all VMs.

    Args:
        None

    Returns:
        List[VirtualMachine]: Environment virtual machines.
    """

    pass

def get_virtual_machine(vm_id: int) -> VirtualMachine:
    """
    Get a virtual machine instance.

    Args:
        vm_id (int): Virtual machine ID.

    Returns:
        VirtualMachine: Requested virtual machine.
    """

    pass
