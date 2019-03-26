"""Management VM web app"""

from flask import Flask, jsonify, abort

# pylint: disable=invalid-name
app = Flask(__name__)

@app.route('/')
def default_route():
    """Default root route"""

    return jsonify(dict(application='vm-manage'))

@app.route('/vm/<size>', methods=['POST'])
def create_vm(size: str):
    """Create a VM"""

    if size not in ['small', 'medium', 'large']:
        abort(400, f'Size {size} does not exist')

    return 'Creating VM!'

@app.route('/vm/')
@app.route('/vm/<int:vm_id>')
def get_vm(vm_id: int = None):
    """List all VMs or a single one"""

    if vm_id is None:
        return 'Get all VMs!'

    return f'Getting VM {vm_id}!'

@app.route('/vm/<int:vm_id>/boot')
def get_vm_boot(vm_id: int):
    """Get VM boot events"""

    return f'Getting boot events for VM {vm_id}!'
