# Copyright (c) 2026 VEXXHOST, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from types import SimpleNamespace
from unittest import mock

from magnum_cluster_api.integrations import common


def test_is_service_enabled_openstacksdk(mocker):
    services = mock.Mock(return_value=iter([{"enabled": True}]))
    keystone = SimpleNamespace(
        client=SimpleNamespace(services=lambda **kwargs: services(**kwargs))
    )
    osc = mock.Mock()
    osc.keystone.return_value = keystone
    mocker.patch("magnum_cluster_api.clients.get_openstack_api").return_value = osc

    assert common.is_service_enabled("sharev2") is True
    services.assert_called_once_with(type="sharev2")


def test_is_service_enabled_openstacksdk_is_enabled_field(mocker):
    services = mock.Mock(return_value=iter([SimpleNamespace(is_enabled=True)]))
    keystone = SimpleNamespace(
        client=SimpleNamespace(services=lambda **kwargs: services(**kwargs))
    )
    osc = mock.Mock()
    osc.keystone.return_value = keystone
    mocker.patch("magnum_cluster_api.clients.get_openstack_api").return_value = osc

    assert common.is_service_enabled("sharev2") is True
    services.assert_called_once_with(type="sharev2")


def test_is_service_enabled_openstacksdk_disabled(mocker):
    services = mock.Mock(return_value=iter([SimpleNamespace(enabled=False)]))
    keystone = SimpleNamespace(
        client=SimpleNamespace(services=lambda **kwargs: services(**kwargs))
    )
    osc = mock.Mock()
    osc.keystone.return_value = keystone
    mocker.patch("magnum_cluster_api.clients.get_openstack_api").return_value = osc

    assert common.is_service_enabled("sharev2") is False
    services.assert_called_once_with(type="sharev2")
