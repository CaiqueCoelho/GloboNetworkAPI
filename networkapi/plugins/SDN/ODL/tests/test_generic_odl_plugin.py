# -*- coding: utf-8 -*-

from nose.tools import assert_raises_regexp
from nose.tools import assert_raises
from requests.exceptions import HTTPError
from requests.models import Response
import mock
from mock import MagicMock


import random
from json import dumps

#from django.test.utils import override_settings
#

from networkapi.equipamento.models import Equipamento
from networkapi.equipamento.models import EquipamentoAcesso
from networkapi.plugins.SDN.ODL.Generic import ODLPlugin
from networkapi.plugins.SDN.ODL.tests.utils import OpenDaylightTestUtils
from networkapi.plugins.factory import PluginFactory
from networkapi.test.test_case import NetworkApiTestCase


class GenericOpenDayLightTestCaseSuccess(NetworkApiTestCase):
    """Class for testing the generic OpenDayLight plugin for success cases."""
    fixtures = [
        'networkapi/system/fixtures/initial_variables.json',
        'networkapi/usuario/fixtures/initial_usuario.json',
        'networkapi/grupo/fixtures/initial_ugrupo.json',
        'networkapi/usuario/fixtures/initial_usuariogrupo.json',
        'networkapi/api_ogp/fixtures/initial_objecttype.json',
        'networkapi/api_ogp/fixtures/initial_objectgrouppermissiongeneral.json',
        'networkapi/grupo/fixtures/initial_permissions.json',
        'networkapi/grupo/fixtures/initial_permissoes_administrativas.json',
        'networkapi/api_rack/fixtures/initial_datacenter.json',
        'networkapi/api_rack/fixtures/initial_fabric.json',
        'networkapi/api_environment/fixtures/initial_base_pre_environment.json',
        'networkapi/api_environment/fixtures/initial_base_environment.json',
        'networkapi/api_environment/fixtures/initial_environment.json',
        'networkapi/api_environment/fixtures/initial_base.json',
        'networkapi/plugins/SDN/ODL/fixtures/initial_equipments.json',
    ]

    utils = OpenDaylightTestUtils()
    json_aclapi_input_path = 'plugins/SDN/ODL/json/aclapi_input/%s'
    json_odl_output_path = 'plugins/SDN/ODL/json/odl_output/%s'

    def setUp(self):
        # Must chose the equipment with the right version running on docker
        # Beryllium
        self.equipment = Equipamento.objects.filter(id=10).uniqueResult()
        # Nitrogen
        #self.equipment = Equipamento.objects.filter(id=11).uniqueResult()

        self.equipment_access = EquipamentoAcesso.objects.filter(id=1).uniqueResult()
        self.utils.set_controller_endpoint(self.equipment_access)

        self.odl = PluginFactory.factory(self.equipment)

        self.flow_key = "flow-node-inventory:flow"

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_checking_if_persisted_in_all_ovss(self, mock_request):
        """Test add flow checking if ACL was persisted at all OVS's."""

        input = self.json_aclapi_input_path % 'acl_id_83000.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        flow_id = data['rules'][0]['id']

        flows = self.odl.get_flow(flow_id)

        for flow in flows:

            output = self.json_odl_output_path % 'odl_id_83000.json'
            self.compare_json_lists(output, flow[self.flow_key])

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_tcp_protocol_dest_eq_l4(self, mock_request):
        """Test add flow with tcp protocol and dest eq in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_82338.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_82338.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_tcp_protocol_flags_rst_l4(self, mock_request):
        """Test add flow with tcp protocol and flags RST in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_101301.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        if self.odl.version == "BERYLLIUM":
            output = self.json_odl_output_path % 'odl_id_101301_beryllium.json'
        elif self.odl.version in ["BORON", "CARBON", "NITROGEN"]:
            output = self.json_odl_output_path % 'odl_id_101301_carbon_boron_nitrogen.json'

        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_tcp_protocol_flags_ack_l4(self, mock_request):
        """Test add flow with tcp protocol and flags ACK in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_101302.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        if self.odl.version == "BERYLLIUM":
            output = self.json_odl_output_path % 'odl_id_101302_beryllium.json'
        elif self.odl.version in ["BORON", "CARBON", "NITROGEN"]:
            output = self.json_odl_output_path % 'odl_id_101302_carbon_boron_nitrogen.json'

        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_tcp_protocol(self, mock_request):
        """Test add flow with tcp protocol."""

        input = self.json_aclapi_input_path % 'acl_id_106966.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_106966.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_with_tcp_protocol_dest_eq_l4_and_sequence(self, mock_request):
        """Test add flow with tcp protocol and dest eq in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_107480.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_107480.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_tcp_protocol_and_sequence(self, mock_request):
        """Test add flow with tcp protocol and sequence."""

        input = self.json_aclapi_input_path % 'acl_id_110886.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_110886.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_with_udp_protocol_src_eq_and_dest_eq_l4(self, mock_request):
        """Test add flow with udp protocol and src eq, dest eq in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_82324.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_82324.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_udp_protocol_dest_eq_l4(self, mock_request):
        """Test add flow with udp protocol and dest eq in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_82337.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_82337.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_udp_protocol_src_eq_l4(self, mock_request):
        """Test add flow with udp protocol and src eq in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_112140.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_112140.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_ip_protocol(self, mock_request):
        """Test add flow with ip protocol."""

        input = self.json_aclapi_input_path % 'acl_id_82332.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_82332.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_ip_protocol_and_sequence(self, mock_request):
        """Test add flow with ip protocol and sequence."""

        input = self.json_aclapi_input_path % 'acl_id_107200.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()
        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_107200.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_icmp_protocol(self, mock_request):
        """Test add flow with icmp protocol."""

        input = self.json_aclapi_input_path % 'acl_id_82325.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

        output = self.json_odl_output_path % 'odl_id_82325.json'
        self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_a_list_of_acls_in_one_request(self, mock_request):
        """ Should insert many flows with one request """

        input = self.json_aclapi_input_path % 'acl_id_83000.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        returns_list = [
            {
                "nodes": {
                    "node": [
                        {
                            "id": "openflow:"
                        }
                    ]
                }
            },
            {
                "topology": [
                    {
                        "node": [
                            {
                                "node-id": "openflow:"
                            }
                        ]
                    }
                ]
            },
            {
                "topology": [
                    {
                        "node": [
                            {
                                "node-id": "openflow:"
                            }
                        ]
                    }
                ]
            }
        ]
        mock_request = MagicMock(side_effect = returns_list)
        nodes_ids = self.odl._get_nodes_ids()
        # nodes_ids = [1,2]

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']
        flow = self.odl.get_flow(flow_id)[random_idx][self.flow_key]

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_remove_flow(self, mock_request):
        """Test of success to remove flow."""

        input = self.json_aclapi_input_path % 'acl_id_80000.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        id_flow = data['rules'][0]['id']
        self.odl.del_flow(id_flow)

        assert_raises(HTTPError, self.odl.get_flow, id_flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_udp_protocol_dest_range_l4(self, mock_request):
        """Test add flow with udp protocol and dest range in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_141880.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']

        for id_ in xrange(1024, 1027+1):

            flow = self.odl.get_flow(flow_id + '_%s' % id_)[random_idx][self.flow_key]
            output = self.json_odl_output_path % 'odl_id_141880_%s.json' % id_
            self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_add_flow_one_acl_rule_with_tcp_protocol_dest_range_l4(self, mock_request):
        """Test add flow with tcp protocol and dest range in l4 options."""

        input = self.json_aclapi_input_path % 'acl_id_141239.json'
        data = self.load_json_file(input)

        self.odl.add_flow(data)

        nodes_ids = self.odl._get_nodes_ids()

        random_idx = random.randint(0, len(nodes_ids) - 1)

        flow_id = data['rules'][0]['id']

        for id_ in xrange(161, 162+1):

            flow = self.odl.get_flow(flow_id + '_%s' % id_)[random_idx][self.flow_key]
            output = self.json_odl_output_path % 'odl_id_141239_%s.json' % id_
            self.compare_json_lists(output, flow)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_flush_flows(self, mock_request):
        """test delete all flows"""

        self.odl.flush_flows()
        flows = self.odl.get_flows()
        for k in flows:
            self.assertEqual(flows[k], [])

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_get_nodes_ids(self, mock_request):
        """Test get nodes ids"""

        self.assertEqual(type(self.odl._get_nodes_ids()), type([]))
        self.assertEqual(len(self.odl._get_nodes_ids()), 3)

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_update_all_flows(self, mock_request):
        """Test update_all_flows"""

        # clean the table
        self.odl.flush_flows()

        # add a fist json with 4 flows
        input = self.json_aclapi_input_path % 'acl_id_150001.json'
        data = self.load_json_file(input)
        self.odl.add_flow(data)

        # try to update with another json
        # at the end:
        # flow 150001 should be updated
        # flow 150002 should remain untouched
        # flow 150003 should be updated
        # flow 150004 should be deleted
        # flow 150005 should be inserted
        # flow 150006 should remain untouched
        # flow 150007 should be deleted
        # flow 150008 should be deleted
        # flow 150009 should be updated
        # flow 1500010 should be updated

        input = self.json_aclapi_input_path % 'acl_id_150002.json'
        data = self.load_json_file(input)
        self.odl.update_all_flows(data=data)

        # assert
        output = self.json_odl_output_path % 'odl_id_150000.json'
        all_flows = self.odl.get_flows()
        for node in all_flows:
            self.compare_json_lists(output, all_flows[node][0]['flow'])

    @mock.patch('networkapi.plugins.SDN.ODL.Generic.ODLPlugin._request')
    def test_get_nodes_ids_empty(self, mock_request):
        """Test get nodes with a empty result"""

        def fake_method(**kwargs):
            e = HTTPError('Fake 404')
            e.response = Response()
            setattr(e.response, 'status_code', 404)
            raise e
        original = self.odl._request
        self.odl._request = fake_method

        self.assertEqual(self.odl._get_nodes_ids(), [])
        self.odl._request = original


class GenericOpenDayLightTestCaseError(NetworkApiTestCase):
    """Class for testing the generic OpenDayLight plugin for error cases."""

    fixtures = [
        'networkapi/plugins/SDN/ODL/fixtures/initial_equipments.json'
    ]

    utils = OpenDaylightTestUtils()

    def setUp(self):
        self.equipment = Equipamento.objects.filter(id=10)[0]
        self.equipment_access = EquipamentoAcesso.objects.filter(id=1)[0]
        self.utils.set_controller_endpoint(self.equipment_access)

        self.odl = PluginFactory.factory(self.equipment)

    def test_add_flow_without_icmp_options(self):
        """Test plugin deny add flow without ICMP options."""

        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "protocol": "icmp",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
            }]
        }

        assert_raises_regexp(
            ValueError,
            'Error building ACL Json. Malformed input data: \n'
            'Missing icmp-options for icmp protocol',
            self.odl.add_flow,
            data
        )

    def test_add_flow_with_only_icmp_code(self):
        """Test plugin deny add flow with only icmp-code."""

        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "protocol": "icmp",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
                "icmp-options": {
                    "icmp-code": "0"
                }
            }]
        }

        rule = dumps(data['rules'][0], sort_keys=True)

        assert_raises_regexp(
            ValueError,
            "Error building ACL Json. Malformed input data: \n"
            "Missing icmp-code or icmp-type icmp options:\n%s" %
            rule,
            self.odl.add_flow,
            data
        )

    def test_add_flow_with_only_icmp_type(self):
        """Test plugin deny add flow with only icmp-type."""

        data = {
            "kind": "Access Control List",
            "rules": [{
                "id": 1,
                "protocol": "icmp",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
                "icmp-options": {
                    "icmp-type": "8"
                }
            }]
        }

        rule = dumps(data['rules'][0], sort_keys=True)

        assert_raises_regexp(
            ValueError,
            "Error building ACL Json. Malformed input data: \n"
            "Missing icmp-code or icmp-type icmp options:\n%s" %
            rule,
            self.odl.add_flow,
            data
        )

    def test_add_flow_without_icmp_code_and_icmp_type(self):
        """Test plugin deny add flow without icmp-code and icmp-type."""

        data = {
            "kind": "Access Control List",
            "rules": [{
                "id": 1,
                "protocol": "icmp",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
                "icmp-options": {
                }
            }]
        }

        rule = dumps(data['rules'][0], sort_keys=True)

        assert_raises_regexp(
            ValueError,
            "Error building ACL Json. Malformed input data: \n"
            "Missing icmp-code or icmp-type icmp options:\n%s" %
            rule,
            self.odl.add_flow,
            data
        )

    def test_add_flow_with_only_source(self):
        """Test plugin deny add flow with only source."""

        data = {
            "kind": "Access Control List",
            "rules": [{
                "action": "permit",
                "description": "Restrict environment",
                "icmp-options": {
                    "icmp-code": "0",
                    "icmp-type": "8"
                },
                "id": "82325",
                "owner": "networkapi",
                "protocol": "icmp",
                "source": "0.0.0.0/0"
            }]
        }

        rule = dumps(data['rules'][0], sort_keys=True)

        assert_raises_regexp(
            ValueError,
            "Error building ACL Json. Malformed input data: \n%s" %
            rule,
            self.odl.add_flow,
            data
        )

    def test_add_flow_with_only_destination(self):
        """Test plugin deny add flow with only destination."""

        data = {
            "kind": "default#acl",
            "rules": [{
                "action": "permit",
                "description": "generic",
                "destination": "10.0.0.0/8",
                "icmp-options": {
                    "icmp-code": "0",
                    "icmp-type": "8"
                },
                "id": "82325",
                "owner": "networkapi",
                "protocol": "icmp"
            }]
        }

        rule = dumps(data['rules'][0], sort_keys=True)

        assert_raises_regexp(
            ValueError,
            "Error building ACL Json. Malformed input data: \n%s" %
            rule,
            self.odl.add_flow,
            data
        )

    def test_add_flow_without_source_and_destination(self):
        """Test plugin deny add flow without source and destination."""

        data = {
            "kind": "default#acl",
            "rules": [{
                "action": "permit",
                "description": "generic",
                "icmp-options": {
                    "icmp-code": "0",
                    "icmp-type": "8"
                },
                "id": "82325",
                "owner": "networkapi",
                "protocol": "icmp"
            }]
        }

        rule = dumps(data['rules'][0], sort_keys=True)

        assert_raises_regexp(
            ValueError,
            "Error building ACL Json. Malformed input data: \n%s" %
            rule,
            self.odl.add_flow,
            data
        )
