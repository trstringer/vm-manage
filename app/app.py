"""Management VM web app"""

from flask import Flask, jsonify

# pylint: disable=invalid-name
app = Flask(__name__)

@app.route('/')
def default_route():
    """Default root route"""

    return jsonify(dict(application='vm-manage'))

@app.route('/vm', methods=['POST'])
def create_vm():
    """Create a VM"""

    return 'Creating a VM!'

@app.route('/vm/')
@app.route('/vm/<vm_id>')
def get_vm(vm_id: int = None):
    """List all VMs or a single one"""

    if vm_id is None:
        return 'Get all VMs!'

    return f'Getting VM {vm_id}!'
