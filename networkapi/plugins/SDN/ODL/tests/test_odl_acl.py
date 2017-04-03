# -*- coding: utf-8 -*-


from django.test.client import Client
from nose.tools import assert_raises
from nose.tools import assert_equal
from nose.tools import assert_in

from networkapi.test.test_case import NetworkApiTestCase
from networkapi.plugins.SDN.ODL.flows.acl import AclFlowBuilder


class OpenDayLightACLTestCase(NetworkApiTestCase):
    """ Opendaylight controller Access Control List test class """

    def setUp(self):
        self.client = Client()

    def test_acl_flow_bulder_raising_type_error(self):
        """ Should rise TypeError when flows variable is not a dict """
        flows = AclFlowBuilder({})
        flows.flows = None

        assert_raises(TypeError, flows.dump)

    def test_acl_flow_builder_empty_json(self):
        """ Should return a json with empty data """
        data = {"kind": "default#acl", "rules": []}
        flows = AclFlowBuilder(data)
        assert_equal(flows.dump(), '{"flow": []}')

    def test_acl_flow_builder_malformed_json(self):
        """ Should return a ValueError """

        acl = AclFlowBuilder({})
        assert_raises(ValueError, acl.dump)

    def test_acl_flow_builder_missing_destination_data(self):
        """ Should have description on flow """

        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "protocol": "tcp",
                "description": "simple flow",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
            }]
        }

        acl = AclFlowBuilder(data)
        acl.build()

        assert_in("flow-name", acl.flows["flow"][0])
        assert_equal(acl.flows["flow"][0]["flow-name"],
                data["rules"][0]["description"])

    def test_acl_should_raise_value_error_when_no_destination_is_passed(self):
        """ Should raise ValueError when no destination is passed """
        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "protocol": "tcp",
                "description": "simple flow",
                "source": "10.0.0.1/32",
            }]
        }

        acl = AclFlowBuilder(data)
        assert_raises(ValueError, acl.build)

    def test_acl_should_raise_value_error_when_no_source_is_passed(self):
        """ Should raise ValueError when no source is passed """
        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "protocol": "tcp",
                "description": "simple flow",
                "destination": "10.0.0.2/32",
            }]
        }

        acl = AclFlowBuilder(data)
        assert_raises(ValueError, acl.build)

    def test_acl_should_have_ethernet_type(self):
        """ Should have ethernet type as match field """
        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "protocol": "tcp",
                "description": "simple flow",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
            }]
        }
        acl = AclFlowBuilder(data)
        acl.build()

        assert_equal(
            2048,
            acl.flows["flow"][0]["match"]["ethernet-match"]\
                    ["ethernet-type"]["type"])

    def test_acl_should_raise_exception_when_there_is_no_protocol_field(self):
        """ Should raise an exception when there is no protocol field """
        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "description": "simple flow",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
            }]
        }
        acl = AclFlowBuilder(data)
        assert_raises(ValueError, acl.build)

    def test_acl_should_raise_exception_when_protocol_is_invalid(self):
        """ Should raise an exception when there is no protocol field """
        data = {
            "kind": "default#acl",
            "rules": [{
                "id": 1,
                "protocol": "invalid",
                "description": "simple flow",
                "source": "10.0.0.1/32",
                "destination": "10.0.0.2/32",
            }]
        }
        acl = AclFlowBuilder(data)
        assert_raises(ValueError, acl.build)
