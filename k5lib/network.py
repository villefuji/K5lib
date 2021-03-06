"""
network module.

 Functions related networks, routers, network connectors, vpn  etc are here.

"""
import requests
import json
import logging
import ipaddress

log = logging.getLogger(__name__)


def _rest_create_network_connector(project_token, project_id, region, connector_name):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'network_connector': {
        'name': connector_name,
        'tenant_id': project_id}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_network_connector(project_token, project_id, region, connector_name):
    """
    Create a network connector.

    :param project_token: A valid K5 project token
    :param project_id: K5 project ID
    :param region: K5 region name.
    :param connector_name: Connector name.
    :return: Network connector ID or error from requests library

    """
    request = _rest_create_network_connector(project_token, project_id, region, connector_name)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network_connector']['id']


def _rest_create_network_connector_endpoint(project_token, project_id, region, az, endpoint_name, networkconnector_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"network_connector_endpoint": {
        "name": endpoint_name,
        "network_connector_id": networkconnector_id,
        "endpoint_type": "availability_zone",
        "location": az,
        "tenant_id": project_id
    }
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_network_connector_endpoint(project_token, project_id, region, az, endpoint_name, networkconnector_id):
    """

    Create a endpoint into specified network connector.

    :param project_token: A valid K5 project token.
    :param project_id: Valid K5 project ID
    :param region: K5 region name.
    :param az: K5 availability zone name.
    :param endpoint_name: Name of endpoint
    :param networkconnector_id: network connector ID
    :return: ID of connector if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_network_connector_endpoint(project_token, project_id, region, az, endpoint_name,
                                                      networkconnector_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network_connector_endpoint']['id']


def _rest_list_network_connector_endpoints(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_network_connector_endpoints(project_token, region):
    """

    List network connector endpoints.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_network_connector_endpoints(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_network_connector_endpoint_id(project_token, region, endpoint_name):
    """

    Get an ID for network connector endpoint.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param endpoint_name: Endpoint name.
    :return: ID if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_network_connector_endpoints(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        # Get ID of our connector endpoint from info
        outputList = []
        outputDict = request['network_connector_endpoints']

        counter = 0
        for i in outputDict:
            if str(i['name']) == endpoint_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_get_network_connector_endpoint_info(project_token, region, network_connector_endpoint_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + network_connector_endpoint_id

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def get_network_connector_endpoint_info(project_token, region, network_connector_endpoint_id):
    """

    Get detailed info of network connector endpoint.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param network_connector_endpoint_id: ID of network connection
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_get_network_connector_endpoint_info(project_token, region, network_connector_endpoint_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_list_network_connector_endpoint_interfaces(project_token, region, network_connector_endpoint_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' \
          + network_connector_endpoint_id + '/interfaces'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_network_connector_endpoint_interfaces(project_token, region, network_connector_endpoint_id):
    """

    List network connector endpoint interfaces.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param network_connector_endpoint_id: ID of network connection
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_network_connector_endpoint_interfaces(project_token, region, network_connector_endpoint_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_create_inter_project_connection(project_token, region, router_id, port_id):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"port_id": port_id}

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id + '/add_cross_project_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def create_inter_project_connection(project_token, region, router_id, port_id):
    """

    Add an interface from a subnet (source project) in a different project to the router (target project).

    :param project_token: A valid K5 project token for target project.
    :param region: Region of target project
    :param router_id: ID of the router at target project
    :param port_id: ID of port at source project
    :return: ID of inter project connection if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_inter_project_connection(project_token, region, router_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_delete_inter_project_connection(project_token, region, router_id, port_id):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"port_id": port_id}

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id + '/remove_cross_project_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def delete_inter_project_connection(project_token, region, router_id, port_id):
    """

    Delete an interface from a subnet in a different project to the router in the project.

    :param project_token: A valid K5 project token.
    :param region: Region of target project.
    :param router_id: ID of the router at target project.
    :param port_id: ID of port at source project.
    :return: ID of inter project connection if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_inter_project_connection(project_token, region, router_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_update_inter_project_connection(project_token, region, router_id, routes):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"router": {
        "routes": routes}
    }

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def update_inter_project_connection(project_token, region, router_id, routes):
    """

     Update the routing information between different tenants within the same domain.

    :param project_token: A valid K5 project token
    :param region: K5 region name
    :param router_id: Router ID.
    :param routes: List of dictionaries in format:
                    {"nexthop":"IPADDRESS",
                     "destination":"CIDR"}
    :return: ID of connection if succesfull. Otherwise error from requests library.

    """
    request = _rest_update_inter_project_connection(project_token, region, router_id, routes)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['router']['id']


def _rest_create_port_on_network(project_token, region, az, network_id, port_name, securitygroup_id, subnet_id, ip_address):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    if securitygroup_id is None:
        securitygroup_id_list = None
    else:
        securitygroup_id_list = [securitygroup_id]

    if ip_address is None:
        fixed_ips_list = None
    else: fixed_ips_list = [{"ip_address": ip_address,
                             "subnet_id": subnet_id}]

    configData = {"port": {
        "network_id": network_id,
        "name": port_name,
        "admin_state_up": True,
        "availability_zone": az,
        "fixed_ips": fixed_ips_list,
        "security_groups": securitygroup_id_list}
    }

    """
    if ip_address is None:
        configData = {"port": {
            "network_id": network_id,
            "name": port_name,
            "admin_state_up": True,
            "availability_zone": az,
            "security_groups":
                securitygroup_id_list}
        }
    else:
        configData = {"port": {
            "network_id": network_id,
            "name": port_name,
            "admin_state_up": True,
            "availability_zone": az,
            "fixed_ips": [{
                "ip_address": ip_address,
                "subnet_id": subnet_id}],
            "security_groups":
                securitygroup_id_list}
        }
    """

    # Remove optional variables that are empty. This prevents 400 errors from api.
    # loop trough copy of configdata and evaluate value, remove if None
    for key in configData['port'].copy().keys():
        log.info('Evaluate key: ' + key)
        log.info('Evaluate value: ' + str(configData['port'][key]))
        if configData['port'][key] is None:
            log.info('Remove null value ' + str(configData['port'][key]))
            del configData['port'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_port_on_network(project_token, region, az, network_id, port_name='Port', securitygroup_id=None, subnet_id=None,
                           ip_address=None):
    """
    Create a port on network.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: K5 availability zone name.
    :param network_id: Network ID.
    :param port_name: (Optional) Port name.
    :param securitygroup_id: (Optional) Security group ID.
    :param subnet_id: (Optional) Subnet ID.
    :param ip_address: (Optional) IP address for the port.

    :return: ID of port if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_port_on_network(project_token, region, az, network_id, port_name, securitygroup_id, subnet_id,
                                           ip_address)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['port'].get('id')


def _rest_list_ports(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_ports(project_token, region):
    """
    List ports.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_ports(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_port_id(project_token, region, port_name):
    """

    Get ID of the port.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param port_name: Port name.

    :return: ID if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_ports(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['ports']

        counter = 0
        for i in outputDict:
            if str(i['name']) == port_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter > 0:
            return outputList[0]
        else:
            return 'Error: Not found'



def _rest_delete_port(project_token, region, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports/' + port_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_port(project_token, region, port_id):
    """

    Delete port.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param port_id: Port ID.
    :return: Http 204 if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_port(project_token, region, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request

def _rest_attach_floating_ip_to_port(project_token, region, az, network_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/floatingips'

    configData = {"floatingip": {
            "floating_network_id": network_id,
            "port_id": port_id,
            "availability_zone": az
        },
    }

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def attach_floating_ip_to_port(project_token, region, az, network_id, port_id):
    """
    Attach floating IP onto port.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Valid K5 availability zone.
    :param network_id: ID of floating IP network.
    :param port_id: Port ID.

    :return: JSON if succesfull. Otherwise error code from requests library.
    """
    request = _rest_attach_floating_ip_to_port(project_token, region, az, network_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request



def _rest_list_network_connectors(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_network_connectors(project_token, region):
    """
    List network connectors visible for project in region.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains network connectors if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_network_connectors(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_network_connector_id(project_token, region, connector_name):
    """
    Get ID of network connector.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param connector_name: Connector name.
    :return: ID of the connector if succesfull. Otherwise error from requests library

    """
    request = _rest_list_network_connectors(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['network_connectors']

        counter = 0
        for i in outputDict:
            if str(i['name']) == connector_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter > 0:
            return outputList[0]
        else:
            return 'Error: Not found'


def _rest_delete_network_connector(project_token, region, networkConnector_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors' + '/' + networkConnector_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network_connector(project_token, region, networkConnector_id):
    """
    Delete network connector.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param networkConnector_id: Network connector ID
    :return:  Http 204 if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_network_connector(project_token, region, networkConnector_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def _rest_connect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"interface": {
        "port_id": port_id}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpoint_id + '/connect'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        log.error(json.dumps(request.json(), indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def connect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    """
    Connect networkc connector with endpoint.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param endpoint_id: Endpoint ID.
    :param port_id: Port ID.
    :return: JSON if succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_connect_network_connector_endpoint(project_token, region, endpoint_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_disconnect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"interface": {
        "port_id": port_id}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpoint_id + '/disconnect'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        log.error(json.dumps(request.json(), indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def disconnect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    """

    Disconnect network connector from endpoint.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param endpoint_id: Endpoint ID.
    :param port_id: Port ID.
    :return: JSON if succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_disconnect_network_connector_endpoint(project_token, region, endpoint_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_delete_network_connector_endpoint(project_token, region, connector_endpoint_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints' + '/' + connector_endpoint_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network_connector_endpoint(project_token, region, connector_endpoint_id):
    """

    Delete network connector endpoint.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param connector_endpoint_id: Network connecto ID.
    :return: Http result code 204 succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_delete_network_connector_endpoint(project_token, region, connector_endpoint_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def _rest_create_network(project_token, region, az, network_name):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"network": {
                  "name": network_name,
                  "admin_state_up": True,
                  "availability_zone": az}
                  }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/networks'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_network(project_token, region, az, network_name):
    """

    Create a network into project.

    :param project_token: A valid K5 project token.
    :param region: Region
    :param az: AZ for example fi-1a
    :param network_name: Name of the network.
    :return: ID of network if suucesfull, otherwise error from requests lib

    """
    request = _rest_create_network(project_token, region, az, network_name)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network']['id']


def _rest_list_networks(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/networks'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def _rest_delete_network(project_token, region, network_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/networks/' + network_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network(project_token, region, network_id):
    """
    Delete subnet.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param network_id: ID for network to delete.
    :return: Http returncode 204 if succesful. otherwise error code from requests library.

    """
    request = _rest_delete_network(project_token, region, network_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def list_networks(project_token, region):
    """
    List networks visible for project in region.

    :param project_token: A valid K5 project token
    :param region: K5 region name.

    :return: JSON that contains networks if succesfull. Otherwise error from requests library.
    """
    request = _rest_list_networks(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_network_id(project_token, region, network_name):
    """
    Get ID of network.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param network_name: Network name.

    :return: ID of the connector if successful. Otherwise error from requests library

    """
    request = _rest_list_networks(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['networks']

        counter = 0
        for i in outputDict:
            if str(i['name']) == network_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter > 0:
            return outputList[0]
        else:
            return 'Error: Not found'

def _rest_create_subnet(project_token, region,  network_id, cidr, subnet_name, version, az,
                        enable_dhcp, allocation_pools, dns_nameservers, host_routes, gateway_ip):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"subnet": {
                  "name": subnet_name,
                  "network_id": network_id,
                  "ip_version": version,
                  "cidr": cidr,
                  "availability_zone": az,
                  "enable_dhcp": enable_dhcp,
                  "allocation_pools": allocation_pools,
                  "dns_nameservers": dns_nameservers,
                  "host_routes": host_routes,
                  "gateway_ip": gateway_ip}
                  }

    # Remove optional variables that are empty. This prevents 400 errors from api.
    # loop trough copy of configdata and evaluate value, remove if None
    for key in configData['subnet'].copy().keys():
        if configData['subnet'][key] is None:
            log.info('Remove null value ' + str(configData['subnet'][key]))
            del configData['subnet'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/subnets'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_subnet(project_token, region, network_id, cidr, subnet_name='subnet', version='4', az=None,
                  enable_dhcp=True, allocation_pools=None, dns_nameservers=None, host_routes=None, gateway_ip=None):
    """

    Create a subnet.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param network_id: ID for network
    :param cidr: (string). For example:'192.168.199.0/24'
    :param subnet_name: (optional) Name of the subnet. Dfaults 'subnet'
    :param version: IP version '4' or '6'. Defaults 4.
    :param az: (optional) AZ name eg f1-1a. If omitted defaults to regions default az.
    :param enable_dhcp: (optional) Boolean to enable / disable DHCP in subnet. Defaults True.
    :param allocation_pools: (optional)
      ::
                            (Dict) The start and end addresses for the allocation pools.
                             For example [{"start": "192.168.199.2", "end": "192.168.199.254"}]
    :param dns_nameservers: (optional)
      ::
                            A list of DNS name servers for the subnet.
                            For example: ["8.8.8.7", "8.8.8.8"].
                            The specified IP addresses are displayed in sorted order in ascending order.
                            The lowest IP address will be the primary DNS address.
    :param host_routes: (optional)
                      ::
                        A list of host route dictionaries for the subnet.
                        For example: [{"destination":"0.0.0.0/0", "nexthop":"172.16.1.254"},
                                      {"destination":"192.168.0.0/24", "nexthop":"192.168.0.1"}]
    :param gateway_ip: (optional). IP address of network default gateway.

    :return: Subnet ID if successful, otherwise error from request library

    """
    request = _rest_create_subnet(project_token, region,  network_id, cidr, subnet_name, version, az,
                                  enable_dhcp, allocation_pools, dns_nameservers, host_routes, gateway_ip)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['subnet']['id']


def _rest_delete_subnet(project_token, region, subnet_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/subnets/' + subnet_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_subnet(project_token, region, subnet_id):
    """
    Delete subnet.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param subnet_id: ID for subnet to delete.
    :return: Http returncode 204 if succesful. otherwise error code from requests library.

    """
    request = _rest_delete_subnet(project_token, region, subnet_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def _rest_list_subnets(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/subnets'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_subnets(project_token, region):
    """
    List subnets visible for project in region.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains subnets if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_subnets(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_subnet_id(project_token, region, subnet_name):
    """
        Returns subnet ID.

        :param project_token: A valid K5 project token
        :param region: K5 region name.
        :param subnet_name: Name of the subnet

        :return: ID of subnet if succesfull. Otherwise Error: Not Found string.

        """
    request = _rest_list_subnets(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our subnet from info
        outputList = []
        outputDict = request['subnets']

        counter = 0
        for i in outputDict:
            if str(i['name']) == subnet_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter > 0:
            return outputList[0]
        else:
            return 'Error: Not found'


def find_first_free_ip(project_token, region, subnet_id=None, subnet_name=None, offset=None):
    """

    :param project_token: Valid K5 project token.
    :param subnet_id: ID of the subnet. (optional)
    :param subnet_name: Name of the subnet.(optional)
    :param offset: Starting point from start of network adresses. Default 0.

    :return: ipaddress object if succesfull. Otherwise Error

    ..Note::
        You need to provide either subnet_id or subnet_name parameter
    """

    ip_list = []

    # Verify offset
    if not offset:
        offset = 0

    #print('Offset: ', offset)

    # Verify we have proper subnet info available
    if subnet_name:
        subnet_id = get_subnet_id(project_token, region, subnet_name)
        # print('subnet_id: ', subnet_id)

    if not subnet_id:
        # print('Error: no  subnet ID available')
        return 'Error: no subnet ID available'

    # Loop trough subnets and find our subnet
    subnet_list = list_subnets(project_token, region)

    dict_subnets = subnet_list['subnets']
    for i in dict_subnets:
        if i['id'] in subnet_id:
            cidr = i['cidr']
            #print('cidr: ', cidr)
            network = ipaddress.IPv4Network(cidr)

            # Loop ports and collect subnet IP adresses
            port_list = list_ports(project_token, region)
            dict_ports = port_list['ports']
            for j in dict_ports:
                for k in j.get('fixed_ips'):
                    if k['subnet_id'] in subnet_id:
                        ip_list.append(ipaddress.IPv4Address(k['ip_address']))
                        # print('Reserved IP: ', ipaddress.IPv4Address(k['ip_address']))

            # Loop network adresses and check if address is on subnet ip list
            # return first free IP
            for l in network.hosts():
                if ipaddress.IPv4Address(l) > network.network_address + offset:
                    if ipaddress.IPv4Address(l) not in ip_list:
                        # print('free IP: ',l)
                        return ipaddress.IPv4Address(l)


def _rest_create_security_group(project_token, region, name, description):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'security_group': {
                     'name': name,
                     'description': description
                      }
                  }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/security-groups'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_security_group(project_token, region, name, description):
    """
    Create a security group.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param name: Name of security group
    :param description: Description for security group.
    :return: Security group ID if succesfull, otherwise error from request library.

    """
    request = _rest_create_security_group(project_token, region, name, description)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['security_group']['id']


def _rest_delete_security_group(project_token, region, security_group_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/security-groups/' + security_group_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_security_group(project_token, region, security_group_id):
    """
    Delete a security group.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param security_group_id: ID of security group to be deleted

    :return: Security group ID if succesfull, otherwise error from request library.

    """
    request = _rest_delete_security_group(project_token, region, security_group_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.status_code


def _rest_list_security_groups(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}


    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/security-groups'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_security_groups(project_token, region):
    """
    List security groups visible to project

    :param project_token:
    :param region:

    :return: JSON if succesfull, otherwise error from request library.
    """

    request = _rest_list_security_groups(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_security_group_id(project_token, region, sg_name):
    """
    Get ID of the security group.

    :param project_token:
    :param region:
    :param sg_name:
    :return: ID of security group if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_security_groups(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['security_groups']

        counter = 0
        for i in outputDict:
            if str(i['name']) == sg_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter != 0:
          return outputList[0]
        else:
            return '0'

def _rest_create_security_group_rule(project_token, region, security_group_id, direction, ethertype, protocol,
                                     port_range_min, port_range_max, remote_ip_prefix, remote_group_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'security_group_rule': {
                     'direction': direction,
                     'port_range_min': port_range_min,
                     'ethertype': ethertype,
                     'port_range_max': port_range_max,
                     'protocol': protocol,
                     'remote_group_id': remote_group_id,
                     'security_group_id': security_group_id,
                     'remote_ip_prefix': remote_ip_prefix
    }
    }

    # Remove optional variables that are empty. This prevents 400 errors from api.
    # loop trough copy of configdata and evaluate value, remove if None
    for key in configData['security_group_rule'].copy().keys():
        if configData['security_group_rule'][key] is None:
            log.info('Remove null value ' + str(configData['security_group_rule'][key]))
            del configData['security_group_rule'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/security-group-rules'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request



def create_security_group_rule(project_token, region, security_group_id, direction, ethertype='IPv4', protocol=None,
                               port_range_min=None, port_range_max=None, remote_ip_prefix=None, remote_group_id=None):
    """
    Create security group rule.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param security_group_id: ID of the security group.
    :param direction: Ingress or egress: The direction in which the security group rule is applied.
                      For a compute instance, an ingress security group rule is applied to incoming (ingress)
                      traffic for that instance. An egress rule is applied to traffic leaving the instance.
    :param ethertype: Must be IPv4, and addresses represented in CIDR must match the ingress or egress rules. If this
                      values is not specified, IPv4 is set.
    :param protocol: The protocol that is matched by the security group rule. Valid values are null, tcp, udp, icmp,
                     and digits between 0-and 255.
    :param port_range_min: The minimum port number in the range that is matched by the security group rule.
                           When the protocol is TCP or UDP, this value must be less than or equal to the value of
                           the port_range_max attribute. If this value is not specified, the security group rule
                           matches all numbers of port. If port_range_min is 0, all port numbers are allowed regardless
                           of port_range_max.
                           When the protocol is ICMP, this value must be an ICMP type. If this value is not specified,
                           the security group rule matches all ICMP types.
    :param port_range_max: The maximum port number in the range that is matched by the security group rule.
                           When the protocol is TCP or UDP , the port_range_min attribute constrains the port_range_max
                           attribute.
                           When the protocol is ICMP, this value must be an ICMP code. If this value is not specified,
                           the security group rule matches all ICMP codes.
    :param remote_ip_prefix: The remote IP prefix to be associated with this security group rule. You can specify
                             either remote_group_id or remote_ip_prefix in the request body. This attribute matches the
                             specified IP prefix as the source or destination IP address of the IP packet.
                             If direction is ingress matches source, otherwise matches destination.
    :param remote_group_id: The remote group ID to be associated with this security group rule. You can specify either
                            remote_group_id or remote_ip_prefix.
    :return: Security group ID if succesfull, otherwise error from request library.

    """
    request = _rest_create_security_group_rule(project_token, region, security_group_id, direction, ethertype, protocol,
                                               port_range_min, port_range_max,  remote_ip_prefix, remote_group_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['security_group_rule']['id']


def _rest_create_router(project_token, region, name, az, admin_state_up):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'router': {
                     'name': name,
                     'availability_zone': az,
                     'admin_state_up': admin_state_up
                      }
                  }

    # Remove optional variables that are empty. This prevents 400 errors from api.
    # loop trough copy of configdata and evaluate value, remove if None
    for key in configData['router'].copy().keys():
        if configData['router'][key] is None:
            log.info('Remove null value ' + str(configData['router'][key]))
            del configData['router'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_router(project_token, region, name=None, az=None, admin_state_up=None):
    """
    Create router.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param name: Name of the router.
    :param az: AZ name eg f1-1a.
    :param admin_state_up: The administrative state of the
                           router, which is up (true) or down (false).
    :return: Router ID if succesfull, otherwise error from request library.

    """
    request = _rest_create_router(project_token, region, name, az, admin_state_up)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['router']['id']


def _rest_delete_router(project_token, region, router_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}


    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_router(project_token, region, router_id):
    """
    Delete router.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param router_id: ID of the router to be deleted

    :return: HTTP 204 if succesfull, otherwise HTTP error.

    """
    request = _rest_delete_router(project_token, region, router_id)
    if 'Error' in str(request):
        return 'Error: ' + str(request)
    else:
        return request.status_code



def _rest_list_routers(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_routers(project_token, region):
    """
    List routers in project.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'

    :return:JSON if succesfull, otherwise error from request library.

    """

    request = _rest_list_routers(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_router_id(project_token, region, router_name):
    """
    Get router ID.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'.
    :param router_name: Name of the router.

    :return: Router ID if succesfull, otherwise error.
    """

    request = _rest_list_routers(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        # Get ID of our router from info
        outputList = []
        outputDict = request['routers']

        counter = 0
        for i in outputDict:
            if str(i['name']) == router_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter > 0:
            return outputList[0]
        else:
            return 'Error: Not found'

def _rest_update_router(project_token, region, router_id, name, az, admin_state_up, network_id, route_table):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'router': {
                     'name': name,
                     'availability_zone': az,
                     'admin_state_up': admin_state_up,
                     'external_gateway_info': {
                         'network_id': network_id
                      },
                     'routes': route_table
                      }
                  }
    # Remove optional variables that are empty. This prevents 400 errors from api.
    if configData['router']['external_gateway_info']['network_id']is None:
        del configData['router']['external_gateway_info']['network_id']
        del configData['router']['external_gateway_info']

    for key in configData['router'].copy().keys():
        if configData['router'][key] is None:
            log.info('Remove null value' + str(configData['router'][key]))
            del configData['router'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def update_router(project_token, region, router_id, name=None, az=None, admin_state_up=None, network_id=None, route_table=None):
    """
    Update router.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param router_id: ID of the router
    :param name: (optional) Name of the router.
    :param az: (optional) AZ name eg f1-1a.
    :param admin_state_up: (optional) The administrative state of the
                           router, which is up (true) or down (false).
    :param network_id: (optional) ID of external network.
    :param route_table: (optional) [{"nexthop":"10.1.0.10", "destination":"40.0.1.0/24"}]

    :return: JSON if succesfull otherwise error from reguests library.

    """
    request = _rest_update_router(project_token, region, router_id, name, az, admin_state_up, network_id, route_table)

    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_add_router_interface(project_token, region, router_id, subnet_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {
        'subnet_id': subnet_id,
        'port_id': port_id
    }

    # Delete Null values from config data this prevents 400 errosrs from api
    if configData['subnet_id'] is None:
            del configData['subnet_id']
    if configData['port_id'] is None:
            del configData['port_id']

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id + '/add_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request

def add_router_interface(project_token, region, router_id, subnet_id=None, port_id=None):
    """
    Add an interface into router.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param router_id: ID of the router

    :param subnet_id:(optional) ID of the subnet which interface is connected
    :param port_id: (Optional) ID of port which interface is connected

    :return: ID of interface if succesful, otehrwise error from requests library

    Submit only subnet_id OR port_id. If both are declared result is an error.
    """

    request = _rest_add_router_interface(project_token, region, router_id, subnet_id, port_id )

    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_remove_router_interface(project_token, region, router_id, subnet_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {
        'subnet_id': subnet_id,
        'port_id': port_id
    }

    # Delete Null values from config data this prevents 400 errosrs from api
    if configData['subnet_id'] is None:
            del configData['subnet_id']
    if configData['port_id'] is None:
            del configData['port_id']

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id + '/remove_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request

def remove_router_interface(project_token, region, router_id, subnet_id=None, port_id=None):
    """
    Remove an interface from router.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param router_id: ID of the router
    :param subnet_id: ID of the subnet which interface is connected
    :param port_id: ID of port which interface is connected

    :return: ID of interface if succesful, otherwise error from requests library

    Submit only subnet_id OR port_id. If both are declared result is an error.
    """

    request = _rest_remove_router_interface(project_token, region, router_id, subnet_id, port_id )

    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_list_floating_ips(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/floatingips'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_floating_ips(project_token, region):

    request = _rest_list_floating_ips(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()