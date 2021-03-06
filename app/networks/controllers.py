from flask import Blueprint, flash, request, render_template, redirect, url_for
from .. import cli
from models import Network

networks = Blueprint('networks', __name__, url_prefix='/networks')

@networks.route('/list', methods=['GET'])
def list():
    networks = [Network(network) for network in cli.networks()]
    return networks_list('networks/list.html', networks)

@networks.route('/<string:network_id>/delete', methods=['POST'])
def remove_network(network_id):
    try:
        cli.remove_network(network_id)
        flash('Network "%s" has been deleted successfully.' % network_id, 'success')
    except Exception as err:
        print err
        flash(str(err), 'warning')
    return redirect(url_for('networks.list'))

def networks_list(template, network_list):
    search = request.args.get('q')
    networks_filtered = network_list
    if search:
        networks_filtered = []
        for network in network_list:
            if (search in network.name()
                or search in network.id()):
                networks_filtered.append(network)
    return render_template(template, networks=networks_filtered, network_active="active")
