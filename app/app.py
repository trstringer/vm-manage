"""Management VM web app"""

from flask import Flask, jsonify, abort, request, Response
from .virtual_machine import (
    create_virtual_machine,
    list_virtual_machines,
    get_virtual_machine,
    VirtualMachineSize,
    _insert_virtual_machine,
    _insert_virtual_machine_boot_event
)

# pylint: disable=invalid-name
app = Flask(__name__)

@app.route('/')
def default_route():
    """Default root route"""

    return jsonify(dict(application='vm-manage'))

@app.route('/testscript/<message>', methods=['POST'])
def test_script(message: str):
    """Test the script extension"""

    _insert_virtual_machine(name=f'test_{message}', size=VirtualMachineSize.MEDIUM)

@app.route('/vm/<name>/<size>', methods=['POST'])
def create_vm(name: str, size: str):
    """Create a VM"""

    possible_sizes = [vm_size.name.lower() for vm_size in VirtualMachineSize]

    if size.lower() not in possible_sizes:
        abort(400, f'Size {size} does not exist. Possible: {possible_sizes}')

    create_virtual_machine(
        name=name,
        size=VirtualMachineSize.SMALL
    )

    return Response(status=200)

@app.route('/vm/')
@app.route('/vm/<name>')
def get_vm(name: str = None):
    """List all VMs or a single one"""

    if name is None:
        return jsonify([
            vm.to_dict()
            for vm
            in list_virtual_machines()
        ])

    return jsonify(get_virtual_machine(name=name).to_dict())

@app.route('/vm/<name>/boot/')
@app.route('/vm/<name>/boot/<unit>')
def get_vm_boot(name: str, unit: str = None):
    """Get VM boot events"""

    vm = get_virtual_machine(name=name)

    if not vm:
        return Response(status=400)

    return jsonify(vm.events(unit=unit))

@app.route('/vm/<name>/boot', methods=['POST'])
def add_vm_boot_event(name: str):
    """Add a boot event for the specified VM"""

    event_data = request.get_json(force=True, silent=True)

    if event_data and 'UNIT' in event_data and 'MESSAGE' in event_data:
        _insert_virtual_machine_boot_event(
            name=name,
            unit=event_data['UNIT'],
            message=event_data['MESSAGE']
        )

    return Response(status=200)
